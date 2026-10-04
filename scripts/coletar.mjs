// Coleta da auditoria de SEO: crawl, PageSpeed e SEMrush.
// A chave sai de .cursor/mcp.json. Não recebe token pela linha de comando.
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36";

function arg(name, fallback = undefined) {
  const i = process.argv.indexOf(name);
  if (i === -1 || i === process.argv.length - 1) return fallback;
  return process.argv[i + 1];
}

function has(name) {
  return process.argv.includes(name);
}

function fold(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toLowerCase();
}

function decode(value) {
  return String(value || "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)))
    .replace(/\s+/g, " ")
    .trim();
}

function hostKey(hostname) {
  return String(hostname || "").replace(/^www\./i, "").toLowerCase();
}

function loadKey() {
  const file = path.join(root, ".cursor", "mcp.json");
  const json = JSON.parse(fs.readFileSync(file, "utf8"));
  const auth = json?.mcpServers?.semrush?.headers?.Authorization || "";
  const key = auth.replace(/^Apikey\s+/i, "").trim();
  if (!key) throw new Error("Chave SEMrush ausente em .cursor/mcp.json");
  return key;
}

async function get(url, { redirect = "follow", timeout = 25000 } = {}) {
  const res = await fetch(url, {
    redirect,
    headers: { "User-Agent": UA, Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" },
    signal: AbortSignal.timeout(timeout),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  return {
    status: res.status,
    url: res.url,
    location: res.headers.get("location"),
    contentType: res.headers.get("content-type") || "",
    body: buf.subarray(0, 1_500_000).toString("utf8"),
  };
}

async function redirectChain(start) {
  const hops = [];
  let current = start;
  for (let i = 0; i < 6; i += 1) {
    const res = await get(current, { redirect: "manual", timeout: 20000 });
    hops.push({ url: current, status: res.status });
    if (res.status >= 300 && res.status < 400 && res.location) {
      current = new URL(res.location, current).href;
      continue;
    }
    return { hops, finalUrl: res.status ? current : start, status: res.status };
  }
  return { hops, finalUrl: current, status: hops.at(-1)?.status || 0 };
}

function locs(xml) {
  return [...String(xml).matchAll(/<loc>\s*([^<]+)\s*<\/loc>/gi)].map((m) => decode(m[1]));
}

function htmlUrl(url) {
  try {
    const u = new URL(url);
    if (/\.(xml|jpg|jpeg|png|gif|webp|svg|pdf|zip|css|js|mp4|webp)$/i.test(u.pathname)) return false;
    return true;
  } catch {
    return false;
  }
}

function metaContent(html, test) {
  const tag = [...html.matchAll(/<meta\b[^>]*>/gi)].map((m) => m[0]).find(test);
  if (!tag) return "";
  const content = tag.match(/content\s*=\s*["']([^"']*)["']/i);
  return content ? decode(content[1]) : "";
}

function extract(url, status, html) {
  const title = decode((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || "");
  const description = metaContent(html, (tag) => /name\s*=\s*["']description["']/i.test(tag));
  const robots = metaContent(html, (tag) => /name\s*=\s*["']robots["']/i.test(tag));
  const ogImage = metaContent(html, (tag) => /property\s*=\s*["']og:image["']/i.test(tag));
  const canonicalTag = (html.match(/<link[^>]+rel=["']canonical["'][^>]*>/i) || [])[0] || "";
  const canonicalHref = (canonicalTag.match(/href\s*=\s*["']([^"']+)["']/i) || [])[1] || "";
  const h1 = [...html.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi)].map((m) => decode(m[1])).filter(Boolean);
  const h2count = [...html.matchAll(/<h2\b/gi)].length;
  const schemas = [...html.matchAll(/<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)];
  const schemaTypes = [...new Set(schemas.flatMap((m) => [...m[1].matchAll(/"@type"\s*:\s*"([^"]+)"/g)].map((x) => x[1])))];
  const text = decode(html.replace(/<script[\s\S]*?<\/script>/gi, " ").replace(/<style[\s\S]*?<\/style>/gi, " "));
  const words = text.split(" ").filter(Boolean).length;
  const imgs = [...html.matchAll(/<img\b[^>]*>/gi)].map((m) => m[0]);
  const imagesWithoutAlt = imgs.filter((tag) => !/\balt\s*=\s*["'][^"']+["']/i.test(tag)).length;
  return {
    url,
    status,
    title,
    title_chars: title.length,
    description,
    description_chars: description.length,
    h1,
    h1_count: h1.length,
    h2_count: h2count,
    canonical: canonicalHref,
    robots,
    og_image: Boolean(ogImage),
    schema_types: schemaTypes,
    forms: (html.match(/<form\b/gi) || []).length,
    words,
    images: imgs.length,
    images_without_alt: imagesWithoutAlt,
    gtm: [...new Set(html.match(/GTM-[A-Z0-9]+/g) || [])],
    ga4: /googletagmanager|gtag\(|google-analytics/i.test(html)
      ? [...new Set(html.match(/G-[A-Z0-9]{4,}/g) || [])]
      : [],
    pixel_meta: /fbq\(|fbevents\.js|connect\.facebook/i.test(html),
    whatsapp: /wa\.me|api\.whatsapp|whatsapp/i.test(html),
    text_start: text.slice(0, 700),
  };
}

function parseSemi(text) {
  const raw = String(text || "").trim();
  if (!raw) return { error: "resposta vazia", rows: [] };
  if (raw.startsWith("ERROR")) return { error: raw.split(/\r?\n/)[0], rows: [] };
  const lines = raw.split(/\r?\n/).filter(Boolean);
  const headers = lines[0].split(";");
  const rows = lines.slice(1).map((line) => {
    const cols = line.split(";");
    const row = {};
    headers.forEach((header, i) => {
      row[header] = cols[i] ?? "";
    });
    return row;
  });
  return { error: null, rows };
}

async function semrush(key, base, params) {
  const url = new URL(base);
  url.searchParams.set("key", key);
  for (const [name, value] of Object.entries(params)) url.searchParams.set(name, String(value));
  const res = await fetch(url, { signal: AbortSignal.timeout(45000) });
  const text = await res.text();
  return { status: res.status, text };
}

function num(value) {
  if (value === undefined || value === null || String(value).trim() === "") return null;
  const n = Number(String(value).replace(",", "."));
  return Number.isFinite(n) ? n : null;
}

function compact(value) {
  return fold(value).replace(/[^a-z0-9]+/g, "");
}

function isBrandKeyword(keyword, tokens) {
  const compactKeyword = compact(keyword);
  return tokens.some((token) => {
    const compactToken = compact(token);
    if (compactToken.length < 4 || compactKeyword.length < 4) return false;
    return compactKeyword.includes(compactToken);
  });
}

function brandShare(rows, tokens) {
  let brand = 0;
  let total = 0;
  const keywordsMarca = [];
  for (const row of rows) {
    const share = num(row["Traffic (%)"]) || 0;
    total += share;
    if (isBrandKeyword(row.Keyword, tokens)) {
      brand += share;
      keywordsMarca.push(row.Keyword);
    }
  }
  return {
    amostra: rows.length,
    keywords_marca: keywordsMarca,
    participacao_marca_pct: total > 0 ? Math.round((brand / total) * 1000) / 10 : null,
  };
}

function psiSummary(payload) {
  const lr = payload?.lighthouseResult;
  if (!lr) return { error: "sem lighthouseResult" };
  const audit = (id) => lr.audits?.[id]?.displayValue || null;
  const score = lr.categories?.performance?.score;
  return {
    score: typeof score === "number" ? Math.round(score * 100) : null,
    lcp: audit("largest-contentful-paint"),
    cls: audit("cumulative-layout-shift"),
    tbt: audit("total-blocking-time"),
    inp: audit("interaction-to-next-paint"),
    fcp: audit("first-contentful-paint"),
  };
}

async function pagespeed(pageUrl, strategy) {
  const endpoint = new URL("https://www.googleapis.com/pagespeedonline/v5/runPagespeed");
  endpoint.searchParams.set("url", pageUrl);
  endpoint.searchParams.set("strategy", strategy);
  endpoint.searchParams.set("category", "performance");
  const res = await fetch(endpoint, { signal: AbortSignal.timeout(90000) });
  const text = await res.text();
  if (!res.ok) {
    if (res.status === 429) {
      return {
        error:
          "PageSpeed sem cota agora (HTTP 429). Nao invente a nota. Registre a lacuna ou meça de novo mais tarde no PageSpeed Insights.",
      };
    }
    return { error: `HTTP ${res.status}: ${text.slice(0, 240)}` };
  }
  return psiSummary(JSON.parse(text));
}

function internalLinks(html, baseHost) {
  const hrefs = [...html.matchAll(/<a\b[^>]*href=["']([^"'#]+)["']/gi)].map((m) => m[1]);
  const urls = [];
  for (const href of hrefs) {
    try {
      const u = new URL(href, `https://${baseHost}/`);
      if (hostKey(u.hostname) !== hostKey(baseHost)) continue;
      if (!htmlUrl(u.href)) continue;
      u.hash = "";
      urls.push(u.href);
    } catch {
      /* ignora href inválido */
    }
  }
  return [...new Set(urls)];
}

function mdEsc(value) {
  return String(value ?? "n.d.").replace(/\|/g, "/");
}

function writeResumoMd(file, resumo) {
  const k = resumo.keywords_amostra.slice(0, 8);
  const lines = [
    `# Coleta ${resumo.dominio}`,
    "",
    `Coletado em ${resumo.coletado_em}. Banco SEMrush: ${resumo.database}.`,
    `URL final: ${resumo.url_final}`,
    "",
    "## Placar",
    "",
    `- Páginas: ${resumo.placar.paginas}`,
    `- Sem H1: ${resumo.placar.sem_h1}`,
    `- Sem meta description: ${resumo.placar.sem_meta_description}`,
    `- Sem og:image: ${resumo.placar.sem_og_image}`,
    `- Sem schema: ${resumo.placar.sem_schema}`,
    `- Sem formulário: ${resumo.placar.sem_formulario}`,
    `- GA4: ${resumo.placar.ga4.join(", ") || "não detectado"}`,
    `- GTM: ${resumo.placar.gtm.join(", ") || "não detectado"}`,
    "",
    "## SEMrush",
    "",
    `- Rank: ${resumo.semrush.rank ?? "n.d."}`,
    `- Keywords: ${resumo.semrush.keywords ?? "n.d."}`,
    `- Tráfego estimado (Organic Traffic): ${resumo.semrush.trafego ?? "n.d."}`,
    `- Participação de marca na amostra: ${resumo.semrush.participacao_marca_pct ?? "n.d."}%`,
    `- Autoridade: ${resumo.semrush.autoridade ?? "n.d."}`,
    `- Backlinks: ${resumo.semrush.backlinks ?? "n.d."} em ${resumo.semrush.dominios_ref ?? "n.d."} domínios`,
    "",
    "| Termo | Posição | Volume | Fatia do tráfego | URL |",
    "| --- | --- | --- | --- | --- |",
    ...k.map(
      (row) =>
        `| ${mdEsc(row.keyword)} | ${mdEsc(row.posicao)} | ${mdEsc(row.volume)} | ${mdEsc(row.trafego_pct)} | ${mdEsc(row.url)} |`
    ),
    "",
    "Tráfego estimado não é clique do Search Console. Fatia do tráfego é a coluna Traffic (%) da amostra, não visita absoluta.",
    "",
    "## Erros",
    "",
    ...(resumo.erros.length ? resumo.erros.map((item) => `- ${item}`) : ["- nenhum"]),
    "",
  ];
  fs.writeFileSync(file, lines.join("\n"), "utf8");
}

async function main() {
  const dominio = arg("--dominio");
  if (!dominio) {
    console.error("Uso: node scripts/coletar.mjs --dominio cliente.com.br [--marca a,b] [--concorrentes a.com,b.com] [--frases a;b] [--database br] [--max-paginas 12]");
    process.exit(1);
  }

  const database = arg("--database", "br");
  const maxPaginas = Math.min(20, Math.max(1, Number(arg("--max-paginas", "12")) || 12));
  const marca = String(arg("--marca", ""))
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
  const concorrentes = String(arg("--concorrentes", ""))
    .split(",")
    .map((item) => hostKey(item.trim()))
    .filter(Boolean)
    .slice(0, 4);
  const frases = String(arg("--frases", ""))
    .split(";")
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, 8);

  let input = dominio.trim();
  if (!/^https?:\/\//i.test(input)) input = `https://${input}`;
  const start = new URL(input);
  const dominioLimpo = hostKey(start.hostname);
  const tokens = [...new Set([dominioLimpo.split(".")[0], ...marca].map((item) => item.trim()).filter(Boolean))];

  const out = path.join(root, "entregas", dominioLimpo);
  const raw = path.join(out, "_raw");
  fs.mkdirSync(path.join(raw, "pages"), { recursive: true });

  const erros = [];
  const avisos = [
    "Trafego de domain_ranks e Organic Traffic estimado pelo SEMrush, nao clique do Search Console.",
    "Traffic (%) na amostra organica e fatia, nao visita absoluta.",
  ];

  console.log(`coletando ${dominioLimpo}`);
  const chain = await redirectChain(start.href).catch((error) => {
    erros.push(`redirect: ${error.message}`);
    return { hops: [], finalUrl: start.href, status: 0 };
  });

  const key = has("--sem-off") ? null : loadKey();
  const calls = [];

  async function pull(name, base, params) {
    calls.push(name);
    try {
      const result = await semrush(key, base, params);
      fs.writeFileSync(path.join(raw, `${name}.txt`), result.text, "utf8");
      return parseSemi(result.text);
    } catch (error) {
      erros.push(`${name}: ${error.message}`);
      return { error: error.message, rows: [] };
    }
  }

  const semrushJob = (async () => {
    if (!key) return {};
    const ranks = await pull("ranks", "https://api.semrush.com/", {
      type: "domain_ranks",
      export_columns: "Dn,Rk,Or,Ot,Oc",
      domain: dominioLimpo,
      database,
    });
    const organic = await pull("organic", "https://api.semrush.com/", {
      type: "domain_organic",
      display_limit: 25,
      display_sort: "tr_desc",
      export_columns: "Ph,Po,Nq,Cp,Ur,Tr,Td",
      domain: dominioLimpo,
      database,
    });
    const backlinks = await pull("backlinks", "https://api.semrush.com/analytics/v1/", {
      type: "backlinks_overview",
      target: dominioLimpo,
      target_type: "root_domain",
      export_columns: "ascore,total,domains_num,urls_num,follows_num,nofollows_num",
    });
    const suggested = await pull("concorrentes", "https://api.semrush.com/", {
      type: "domain_organic_organic",
      display_limit: 5,
      export_columns: "Dn,Cr,Np,Or,Ot,Oc",
      domain: dominioLimpo,
      database,
    });
    return { ranks, organic, backlinks, suggested };
  })();

  const speedJob = (async () => {
    if (has("--pagespeed-off")) return { mobile: { error: "desligado" }, desktop: { error: "desligado" } };
    const [mobile, desktop] = await Promise.all([
      pagespeed(chain.finalUrl, "mobile").catch((error) => ({ error: error.message })),
      pagespeed(chain.finalUrl, "desktop").catch((error) => ({ error: error.message })),
    ]);
    fs.writeFileSync(path.join(raw, "pagespeed-mobile.json"), JSON.stringify(mobile, null, 2));
    fs.writeFileSync(path.join(raw, "pagespeed-desktop.json"), JSON.stringify(desktop, null, 2));
    return { mobile, desktop };
  })();

  const siteJob = (async () => {
    const robots = await get(new URL("/robots.txt", chain.finalUrl).href).catch((error) => {
      erros.push(`robots: ${error.message}`);
      return { status: 0, body: "" };
    });
    const llms = await get(new URL("/llms.txt", chain.finalUrl).href).catch((error) => {
      erros.push(`llms: ${error.message}`);
      return { status: 0, body: "" };
    });
    const robotsOk = robots.status >= 200 && robots.status < 300;
    const llmsOk = llms.status >= 200 && llms.status < 300 && !/^\s*<(!doctype|html)/i.test(llms.body || "");
    fs.writeFileSync(path.join(raw, "robots.txt"), robotsOk ? robots.body || "" : "", "utf8");
    fs.writeFileSync(path.join(raw, "llms.txt"), llmsOk ? (llms.body || "").slice(0, 20000) : "", "utf8");

    const sitemapDeclared = robotsOk
      ? [...(robots.body || "").matchAll(/^Sitemap:\s*(\S+)/gim)].map((m) => m[1])
      : [];
    const sitemapCandidates = sitemapDeclared.length
      ? sitemapDeclared
      : [new URL("/sitemap.xml", chain.finalUrl).href];
    let sitemapStatus = 0;
    let sitemapBody = "";
    const pageUrls = [];
    for (const candidate of sitemapCandidates.slice(0, 3)) {
      const file = await get(candidate).catch(() => null);
      if (!file || file.status >= 400) continue;
      sitemapStatus = file.status;
      sitemapBody += `\n${file.body}`;
      if (/<sitemapindex[\s>]/i.test(file.body)) {
        for (const child of locs(file.body).slice(0, 4)) {
          const nested = await get(child).catch(() => null);
          if (nested && nested.status < 400) sitemapBody += `\n${nested.body}`;
        }
      }
    }
    fs.writeFileSync(path.join(raw, "sitemap.xml"), sitemapBody.slice(0, 200000), "utf8");
    for (const loc of locs(sitemapBody)) {
      try {
        const u = new URL(loc);
        if (hostKey(u.hostname) !== dominioLimpo) continue;
        if (!htmlUrl(u.href)) continue;
        pageUrls.push(u.href);
      } catch {
        /* loc inválida */
      }
    }

    const home = await get(chain.finalUrl).catch((error) => {
      erros.push(`home: ${error.message}`);
      return { status: 0, url: chain.finalUrl, body: "", contentType: "" };
    });
    if (!pageUrls.length) pageUrls.push(...internalLinks(home.body || "", dominioLimpo));
    const unique = [];
    const seen = new Set();
    for (const url of [home.url || chain.finalUrl, ...pageUrls]) {
      const clean = url.split("#")[0];
      if (seen.has(clean)) continue;
      seen.add(clean);
      unique.push(clean);
      if (unique.length >= maxPaginas) break;
    }

    const pages = [];
    for (const url of unique) {
      const page = url === (home.url || chain.finalUrl) && home.body
        ? home
        : await get(url).catch((error) => ({ status: 0, url, body: "", contentType: "", error: error.message }));
      if (page.error) erros.push(`pagina ${url}: ${page.error}`);
      const html = page.body || "";
      const isHtml = /html|xml/i.test(page.contentType || "") || /<html[\s>]/i.test(html);
      if (!isHtml) continue;
      const data = extract(page.url || url, page.status, html);
      pages.push(data);
      const safe = String(pages.length).padStart(2, "0");
      fs.writeFileSync(path.join(raw, "pages", `${safe}.json`), JSON.stringify(data, null, 2));
      fs.writeFileSync(path.join(raw, "pages", `${safe}.html`), html);
    }

    return {
      robots: {
        status: robots.status,
        tem_sitemap: sitemapDeclared.length > 0 || sitemapStatus > 0,
        bloqueia_tudo: robotsOk && /Disallow:\s*\/\s*$/im.test(robots.body || ""),
      },
      sitemap: { status: sitemapStatus, urls: locs(sitemapBody).filter(htmlUrl).length },
      llms: { status: llmsOk ? llms.status : llms.status || 0, amostra: llmsOk ? decode(llms.body || "").slice(0, 400) : "" },
      pages,
    };
  })();

  const [sem, speed, site] = await Promise.all([semrushJob, speedJob, siteJob]);

  const rankRow = sem.ranks?.rows?.[0] || {};
  const organicRows = sem.organic?.rows || [];
  const share = brandShare(organicRows, tokens);
  const backRow = sem.backlinks?.rows?.[0] || {};
  const rankAusente = /NOTHING FOUND/i.test(sem.ranks?.error || "");
  const backAusente = /NOTHING FOUND/i.test(sem.backlinks?.error || "");
  if (sem.ranks?.error) erros.push(`ranks: ${sem.ranks.error}`);
  if (sem.organic?.error) erros.push(`organic: ${sem.organic.error}`);
  if (sem.backlinks?.error) erros.push(`backlinks: ${sem.backlinks.error}`);

  const sugeridos = (sem.suggested?.rows || [])
    .map((row) => ({
      dominio: row.Domain,
      keywords: num(row["Organic Keywords"]),
      trafego: num(row["Organic Traffic"]),
      relevancia: num(row["Competitor Relevance"]),
    }))
    .filter((row) => row.dominio);

  const alvos = concorrentes.length ? concorrentes : sugeridos.slice(0, 3).map((row) => hostKey(row.dominio));
  const concorrentesMedidos = [];
  if (key) {
    for (const alvo of alvos) {
      if (!alvo || alvo === dominioLimpo) continue;
      const item = await pull(`ranks_${alvo}`, "https://api.semrush.com/", {
        type: "domain_ranks",
        export_columns: "Dn,Rk,Or,Ot,Oc",
        domain: alvo,
        database,
      });
      const row = item.rows[0] || {};
      if (item.error) erros.push(`concorrente ${alvo}: ${item.error}`);
      concorrentesMedidos.push({
        dominio: alvo,
        origem: concorrentes.includes(alvo) ? "informado" : "sugestao_semrush",
        rank: num(row.Rank),
        keywords: num(row["Organic Keywords"]),
        trafego: num(row["Organic Traffic"]),
      });
    }
  }

  let frasesMedidas = [];
  const serps = {};
  if (key && frases.length) {
    const pack = await pull("frases", "https://api.semrush.com/", {
      type: "phrase_these",
      phrase: frases.join(";"),
      export_columns: "Ph,Nq,Cp,Co,Nr",
      database,
    });
    if (pack.error) erros.push(`frases: ${pack.error}`);
    frasesMedidas = pack.rows.map((row) => ({
      frase: row.Keyword,
      volume: num(row["Search Volume"]),
      cpc: num(row.CPC),
      concorrencia: num(row.Competition),
    }));
    for (const frase of frases.slice(0, 6)) {
      const safe = fold(frase).replace(/[^a-z0-9]+/g, "_").slice(0, 40);
      const serp = await pull(`serp_${safe}`, "https://api.semrush.com/", {
        type: "phrase_organic",
        phrase: frase,
        display_limit: 5,
        export_columns: "Dn,Ur,Po",
        database,
      });
      if (serp.error) erros.push(`serp ${frase}: ${serp.error}`);
      serps[frase] = serp.rows.map((row) => ({
        dominio: row.Domain,
        url: row.Url,
        posicao: num(row.Position),
      }));
    }
  }

  const pages = site.pages || [];
  const placar = {
    paginas: pages.length,
    sem_h1: pages.filter((page) => page.h1_count === 0).length,
    sem_title: pages.filter((page) => !page.title).length,
    sem_meta_description: pages.filter((page) => !page.description).length,
    sem_og_image: pages.filter((page) => !page.og_image).length,
    sem_schema: pages.filter((page) => page.schema_types.length === 0).length,
    sem_canonical: pages.filter((page) => !page.canonical).length,
    sem_formulario: pages.filter((page) => page.forms === 0).length,
    imagens: pages.reduce((sum, page) => sum + page.images, 0),
    imagens_sem_alt: pages.reduce((sum, page) => sum + page.images_without_alt, 0),
    palavras_home: pages[0]?.words ?? null,
    gtm: [...new Set(pages.flatMap((page) => page.gtm))],
    ga4: [...new Set(pages.flatMap((page) => page.ga4))],
    pixel_meta: pages.some((page) => page.pixel_meta),
    whatsapp: pages.some((page) => page.whatsapp),
  };

  const resumo = {
    dominio: dominioLimpo,
    url_inicial: start.href,
    url_final: chain.finalUrl,
    redirecionamentos: chain.hops,
    database,
    coletado_em: new Date().toISOString(),
    marca_tokens: tokens,
    fontes: {
      robots: site.robots,
      sitemap: site.sitemap,
      llms: site.llms,
      semrush: {
        ranks: sem.ranks?.error || (key ? "ok" : "desligado"),
        organic: sem.organic?.error || (key ? "ok" : "desligado"),
        backlinks: sem.backlinks?.error || (key ? "ok" : "desligado"),
      },
      pagespeed: {
        mobile: speed.mobile?.error || "ok",
        desktop: speed.desktop?.error || "ok",
      },
      chamadas_semrush: calls,
    },
    placar,
    semrush: {
      rank: rankAusente ? 0 : num(rankRow.Rank),
      keywords: rankAusente ? 0 : num(rankRow["Organic Keywords"]),
      trafego: rankAusente ? 0 : num(rankRow["Organic Traffic"]),
      custo: rankAusente ? 0 : num(rankRow["Organic Cost"]),
      autoridade: backAusente ? 0 : num(backRow.ascore),
      backlinks: backAusente ? 0 : num(backRow.total),
      dominios_ref: backAusente ? 0 : num(backRow.domains_num),
      follows: num(backRow.follows_num),
      nofollows: num(backRow.nofollows_num),
      ...share,
      participacao_marca_pct: share.participacao_marca_pct,
      top_keywords: organicRows.map((row) => ({
        keyword: row.Keyword,
        posicao: num(row.Position),
        volume: num(row["Search Volume"]),
        cpc: num(row.CPC),
        url: row.Url,
        trafego_pct: num(row["Traffic (%)"]),
      })),
      concorrentes_sugeridos: sugeridos,
      concorrentes: concorrentesMedidos,
    },
    pagespeed: { mobile: speed.mobile, desktop: speed.desktop },
    paginas: pages,
    frases: frasesMedidas,
    serps,
    erros,
    avisos,
  };

  fs.writeFileSync(path.join(out, "resumo.json"), JSON.stringify(resumo, null, 2));
  writeResumoMd(path.join(out, "resumo.md"), { ...resumo, keywords_amostra: resumo.semrush.top_keywords });
  console.log(`pronto: ${path.join(out, "resumo.json")}`);
  console.log(`paginas: ${pages.length} | chamadas semrush: ${calls.length} | erros: ${erros.length}`);
  if (erros.length) console.log(erros.join("\n"));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
