#!/usr/bin/env python3
"""Rastreia todas as URLs do sitemap de um domínio e resume o on-page.

Uso:
  py -3 scripts/crawl_sitemap.py --dominio cliente.com.br
  py -3 scripts/crawl_sitemap.py --dominio cliente.com.br --incluir-idiomas

Saída em entregas/<dominio>/extra/:
  crawl.jsonl        uma linha por URL (retomável: rode de novo e ele continua)
  crawl.json         consolidado
  crawl_stats.json   placar por grupo (paginas, posts, categorias, todas)
  crawl_resumo.md    leitura rápida: páginas, títulos, H1, descrições duplicadas, anos

Busca com curl, não com urllib: o Wix e outros CDNs devolvem 429 para o
cliente HTTP do Python e 200 para o curl.
"""
import argparse
import collections
import html
import json
import os
import re
import subprocess
import sys
import time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
LANG_PREFIX = re.compile(r"^https?://[^/]+/(en|es|fr|de|it|en-us|es-es|pt-pt)(/|$)", re.I)


def fetch(url, timeout=60):
    cp = subprocess.run(
        ["curl", "-s", "-L", "--compressed", "--max-time", str(timeout), "-A", UA,
         "-w", "__CODE__%{http_code}__URL__%{url_effective}", url],
        capture_output=True,
    )
    raw = cp.stdout.decode("utf-8", "ignore")
    if "__CODE__" not in raw:
        return 0, url, ""
    body, meta = raw.rsplit("__CODE__", 1)
    code, final = meta.split("__URL__", 1)
    return int(code), final, body


def sitemap_urls(dominio):
    base = f"https://{dominio}"
    code, _, robots = fetch(f"{base}/robots.txt")
    maps = re.findall(r"(?im)^sitemap:\s*(\S+)", robots) if code == 200 else []
    if not maps:
        maps = [f"{base}/sitemap.xml"]
    seen, out, queue = set(), [], list(maps)
    while queue:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        code, _, xml = fetch(sm)
        if code != 200:
            continue
        if "<sitemapindex" in xml:
            queue += re.findall(r"<loc>\s*(.*?)\s*</loc>", xml)
            continue
        name = sm.rsplit("/", 1)[-1]
        for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
            loc = re.search(r"<loc>\s*(.*?)\s*</loc>", block).group(1)
            lm = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", block)
            out.append((name, html.unescape(loc), lm.group(1) if lm else ""))
    return out


def strip(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def meta(h, n):
    m = (re.search(r'<meta[^>]+(?:name|property)="' + n + r'"[^>]*content="([^"]*)"', h, re.I)
         or re.search(r'<meta[^>]+content="([^"]*)"[^>]*(?:name|property)="' + n + '"', h, re.I))
    return html.unescape(m.group(1)) if m else ""


def analyze_page(src, url, lastmod, dominio):
    t0 = time.time()
    code, final, h = fetch(url)
    if code != 200:
        return {"src": src, "url": url, "error": f"HTTP {code}"}
    body = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", h)
    title = re.search(r"(?is)<title[^>]*>(.*?)</title>", h)
    can = re.search(r'<link[^>]+rel="canonical"[^>]*href="([^"]*)"', h)
    imgs = re.findall(r"<img[^>]*>", h)
    host = re.escape(dominio.replace("www.", ""))
    return {
        "src": src, "url": url, "final": final, "status": code, "lastmod": lastmod,
        "secs": round(time.time() - t0, 2), "bytes": len(h),
        "title": strip(title.group(1)) if title else "",
        "desc": meta(h, "description"), "robots": meta(h, "robots"),
        "og_image": bool(meta(h, "og:image")),
        "h1": [strip(x) for x in re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", h)],
        "h2n": len(re.findall(r"(?i)<h2[\s>]", h)),
        "canonical": can.group(1) if can else "",
        "hreflang": re.findall(r'<link[^>]+hreflang="([^"]*)"', h),
        "schema": sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', h))),
        "imgs": len(imgs),
        "imgs_noalt": sum(1 for i in imgs if not re.search(r'alt="[^"]+"', i)),
        "words": len(strip(body).split()),
        "forms": len(re.findall(r"(?i)<form[\s>]", h)),
        "links_internos": sorted(set(re.findall(r'href="(https?://(?:www\.)?' + host + r'[^"#?]*)"', h))),
    }


def group(src):
    s = src.lower()
    if "post" in s or ("blog" in s and "categor" not in s):
        return "posts"
    if "categor" in s or "tag" in s:
        return "categorias"
    return "paginas"


def stats(rows):
    out = {}
    G = collections.defaultdict(list)
    for x in rows:
        G[group(x["src"])].append(x)
    G["todas"] = rows
    for g, xs in G.items():
        n = len(xs)
        descs = collections.Counter(x["desc"] for x in xs if x["desc"])
        titles = collections.Counter(x["title"] for x in xs)
        out[g] = {
            "n": n,
            "sem_h1": sum(1 for x in xs if not x["h1"]),
            "multi_h1": sum(1 for x in xs if len(x["h1"]) > 1),
            "sem_desc": sum(1 for x in xs if not x["desc"]),
            "desc_dup_paginas": sum(c for d, c in descs.items() if c > 1),
            "desc_longa_160": sum(1 for x in xs if len(x["desc"]) > 160),
            "title_dup_paginas": sum(c for t, c in titles.items() if c > 1),
            "title_longo_60": sum(1 for x in xs if len(x["title"]) > 60),
            "title_char_quebrado": sum(1 for x in xs if "￼" in x["title"] or "�" in x["title"]),
            "sem_og_image": sum(1 for x in xs if not x["og_image"]),
            "sem_schema": sum(1 for x in xs if not x["schema"]),
            "noindex": sum(1 for x in xs if "noindex" in x["robots"].lower()),
            "imgs": sum(x["imgs"] for x in xs),
            "imgs_noalt": sum(x["imgs_noalt"] for x in xs),
            "fino_300": sum(1 for x in xs if x["words"] < 300),
            "com_form": sum(1 for x in xs if x["forms"]),
            "schema_types": collections.Counter(t for x in xs for t in x["schema"]).most_common(12),
            "anos_lastmod": sorted(collections.Counter(x["lastmod"][:4] for x in xs if x["lastmod"]).items()),
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dominio", required=True)
    ap.add_argument("--incluir-idiomas", action="store_true", help="não descarta /en/, /es/ etc.")
    ap.add_argument("--pausa", type=float, default=0.8)
    ap.add_argument("--max", type=int, default=2000)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    dom = a.dominio.replace("https://", "").replace("http://", "").strip("/")
    code, final, _ = fetch(f"https://{dom}/")
    host = final.split("/")[2] if code == 200 else dom
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "entregas", dom.replace("www.", ""), "extra")
    os.makedirs(out, exist_ok=True)

    urls = sitemap_urls(host)
    if not a.incluir_idiomas:
        urls = [u for u in urls if not LANG_PREFIX.match(u[1])]
    urls = list({u[1]: u for u in urls}.values())[: a.max]
    print(f"{len(urls)} URLs no sitemap ({host})", flush=True)

    jp = os.path.join(out, "crawl.jsonl")
    done = set()
    if os.path.exists(jp):
        for line in open(jp, encoding="utf-8"):
            d = json.loads(line)
            if "error" not in d:
                done.add(d["url"])
    with open(jp, "a", encoding="utf-8") as fh:
        for i, (src, url, lm) in enumerate(urls):
            if url in done:
                continue
            r = None
            for k in range(4):
                r = analyze_page(src, url, lm, host)
                if "error" in r and r["error"] in ("HTTP 429", "HTTP 0"):
                    time.sleep(15 * (k + 1))
                    continue
                break
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            fh.flush()
            if i % 25 == 0:
                print(i, "erro" if "error" in r else "ok", flush=True)
            time.sleep(a.pausa)

    res = {}
    for line in open(jp, encoding="utf-8"):
        d = json.loads(line)
        if d["url"] not in res or "error" in res[d["url"]]:
            res[d["url"]] = d
    rows = list(res.values())
    ok = [x for x in rows if "error" not in x]
    json.dump(rows, open(os.path.join(out, "crawl.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    st = stats(ok)
    json.dump(st, open(os.path.join(out, "crawl_stats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    dd = collections.Counter(x["desc"] for x in ok if x["desc"])
    tt = collections.Counter(x["title"] for x in ok)
    md = [f"# Crawl {host}", "", f"URLs: {len(rows)} · ok: {len(ok)} · erro: {len(rows) - len(ok)}", ""]
    for g, s in st.items():
        md.append(f"## {g} ({s['n']})")
        md += [f"- {k}: {v}" for k, v in s.items() if k != "n"]
        md.append("")
    md.append("## Páginas (exceto posts)")
    md.append("| URL | title | H1 | desc | palavras | schema |")
    md.append("|---|---|---|---|---|---|")
    for x in sorted((x for x in ok if group(x["src"]) == "paginas"), key=lambda x: x["url"]):
        md.append(f"| {x['url']} | {x['title'][:70]} | {(x['h1'] or [''])[0][:40]} | {len(x['desc'])} | {x['words']} | {','.join(x['schema'][:3])} |")
    md += ["", "## Descrições repetidas"] + [f"- {c}x {d[:120]}" for d, c in dd.most_common(10) if c > 1]
    md += ["", "## Títulos repetidos"] + [f"- {c}x {t[:120]}" for t, c in tt.most_common(10) if c > 1]
    open(os.path.join(out, "crawl_resumo.md"), "w", encoding="utf-8").write("\n".join(md))
    print("FIM", len(rows), "erros", len(rows) - len(ok), flush=True)


if __name__ == "__main__":
    main()
