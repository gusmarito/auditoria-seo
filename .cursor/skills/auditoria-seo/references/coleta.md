# Coleta

Rode na raiz do repositório. Node 18 ou mais recente. Não precisa de `npm install`.

```bash
node scripts/coletar.mjs --dominio cliente.com.br
```

Opções:

```bash
node scripts/coletar.mjs --dominio cliente.com.br --marca "nome da marca,apelido" --concorrentes "a.com.br,b.com.br" --frases "termo um;termo dois" --max-paginas 12 --database br
```

- `--marca` lista os tokens que contam como busca de marca, separados por vírgula. Sem isso, o script usa o nome do domínio.
- `--concorrentes` até 4 domínios. Sem isso, o script guarda só a sugestão do SEMrush e o deck não promove concorrente que ninguém confirmou, exceto os 3 primeiros da sugestão, rotulados como sugestão da ferramenta.
- `--frases` é o segundo passo, depois de ler o site. Até 8 frases de categoria, separadas por ponto e vírgula.
- `--max-paginas` padrão 12. Teto duro do script: 20.
- `--sem-off` e `--pagespeed-off` existem para teste. Não use numa auditoria de cliente.

Se o PageSpeed responder HTTP 429, a cota anônima acabou. O resumo traz essa frase. Não invente score. Rode de novo mais tarde ou cole o JSON do PageSpeed Insights.

Saída:

```text
entregas/<dominio>/
  resumo.json
  resumo.md
  _raw/
    ranks.txt
    organic.txt
    backlinks.txt
    concorrentes.txt
    pagespeed-mobile.json
    pagespeed-desktop.json
    robots.txt
    sitemap.xml
    llms.txt
    pages/
```

Leia `resumo.json` inteiro antes de escrever. Abra o HTML em `_raw/pages/` só para citar uma evidência que o resumo não traz (telefone de template, data inválida, H1 que é um percentual).

A pasta `entregas/` está no `.gitignore`. Não commite dados de cliente neste repositório.

No Windows, os scripts do design system rodam com `py -3` quando `python3` não existe:

```bash
py -3 .cursor/skills/colli-html-ppt/scripts/new_deck.py --output entregas/<dominio>/deck
py -3 .cursor/skills/colli-html-ppt/scripts/validate_deck.py entregas/<dominio>/deck/index.html
```

## Coleta aprofundada (padrão da entrega)

O `coletar.mjs` é a base, mas a amostra dele tem no máximo 20 páginas e, em site multilíngue, pode pegar quase só a versão em inglês. A entrega completa roda também:

```bash
py -3 scripts/crawl_sitemap.py --dominio cliente.com.br
py -3 scripts/semrush_kw.py dominio --dominio cliente.com.br
py -3 scripts/lighthouse.py --url https://www.cliente.com.br/ --dominio cliente.com.br
```

- `crawl_sitemap.py` lê o robots, segue o índice de sitemaps e rastreia todas as URLs do idioma principal (descarta /en/, /es/ salvo `--incluir-idiomas`). Usa curl, porque Wix e outros CDNs devolvem 429 para o cliente HTTP do Python. É retomável: se cair, rode de novo. Em 300 URLs leva de 6 a 10 minutos. Leia `extra/crawl_resumo.md` e `extra/crawl_stats.json`.
- `robots.bloqueia_tudo` do resumo do coletar.mjs dá falso positivo quando o `Disallow: /` é só para um robô (ex.: PetalBot). Confira `_raw/robots.txt` antes de afirmar bloqueio.
- `lighthouse.py` substitui o PageSpeed quando ele responde 429. Ele aponta o maior arquivo (vídeo de fundo é vilão frequente) e avisa se um antivírus da máquina injetou script na medição.

Capturas: home em 1440 e 390, página de serviços, uma página de serviço, contato, blog e a página equivalente do principal concorrente. Playwright com `channel="msedge"`, espera de 6 segundos após `load`, em `entregas/<dominio>/evidencias/`. Copie para `deck/assets/` só as que entram no deck.

Página de serviços: extraia o texto e os links (`/solucoes/`, `/servicos/`) para montar o portfólio, como descrito em [palavras-chave.md](palavras-chave.md).
