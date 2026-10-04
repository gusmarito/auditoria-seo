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
