---
name: auditoria-seo
description: >-
  Gera o diagnóstico de SEO técnico e de conteúdo da Colli&Co: crawl completo do
  sitemap, estudo de palavras-chave levantado pela própria skill a partir do
  portfólio do site, concorrência por SERP, autoridade, velocidade e GEO, com
  storytelling Falconi (problema macro, estratificação, causa raiz, GUT, meta,
  5W1H e backlog). Entrega deck HTML 1600x900 no Design System V4. Use quando
  pedirem auditoria de SEO, diagnóstico de site, estudo de palavras-chave, GEO,
  visibilidade em IA, funil orgânico ou deck de SEO de um domínio.
---

# Auditoria de SEO

Entrega o diagnóstico de SEO no padrão Colli&Co: 34 a 38 slides, divididos em **SEO técnico** e **SEO de conteúdo**, com **estudo de palavras-chave feito pela skill**, plano de ação **5W1H** com backlog e fechamento que mostra a necessidade de **SEO recorrente com especialista sênior da V4**. A referência de qualidade é a auditoria de engenharia ambiental de outubro de 2026: toda chamada deve chegar nesse nível.

Quem clonou o repositório não configura nada. Não peça token, não peça para abrir Settings, não peça para instalar Node ou Python, não peça para copiar skill para outro projeto. Faça você.

## O que a skill não espera receber

O usuário passa só o domínio. A skill levanta sozinha:

- o portfólio de produtos e serviços, lendo o site ([references/palavras-chave.md](references/palavras-chave.md));
- as palavras-chave de cada linha de produto, validadas no Semrush;
- os concorrentes reais, pelos domínios que ocupam o top 10 das buscas de serviço.

Se o usuário mandar planilha de produtos, Search Console, GA4 ou pauta, isso entra como fonte nomeada e complementa a coleta. Não bloqueie a auditoria por falta de nada disso.

## Ambiente

A raiz do workspace é este repositório. A chave do Semrush está em `.cursor/mcp.json` e os scripts leem de lá.

No Windows:

```bash
node -v
py -3 --version
py -3 -c "import playwright, PIL"
```

Node 18 ou mais novo. Se faltar:

```bash
winget install --id OpenJS.NodeJS.LTS -e --scope user --accept-package-agreements --accept-source-agreements --disable-interactivity
winget install --id Python.Python.3.12 -e --scope user --accept-package-agreements --accept-source-agreements --disable-interactivity
py -3 -m pip install playwright pillow
```

O Playwright usa o Edge instalado (`channel="msedge"`), sem baixar navegador. Não commite `entregas/`: está no `.gitignore` e o repositório é público.

## Fluxo

```text
- [ ] 1. Coleta base
- [ ] 2. Crawl completo e capturas
- [ ] 3. Portfólio pelo site
- [ ] 4. Estudo de palavras-chave e SERP
- [ ] 5. Concorrentes e autoridade
- [ ] 6. Velocidade
- [ ] 7. Narrativa Falconi
- [ ] 8. Deck
- [ ] 9. QA visual
```

### 1. Coleta base

```bash
node scripts/coletar.mjs --dominio cliente.com.br --marca "marca,apelido" --max-paginas 20
```

Leia `entregas/<dominio>/resumo.json` por completo. Banco padrão `br`. Detalhes em [references/coleta.md](references/coleta.md) e [references/semrush.md](references/semrush.md).

### 2. Crawl completo e capturas

```bash
py -3 scripts/crawl_sitemap.py --dominio cliente.com.br
```

Rastreia todas as URLs do idioma principal do sitemap. Leia `extra/crawl_resumo.md`. Faça as capturas de tela listadas em [references/coleta.md](references/coleta.md). Sem captura, não afirme defeito visual.

### 3. Portfólio pelo site

Monte `extra/portfolio.md` com linhas de produto, produtos e status (página própria, parcial, sem página), seguindo [references/palavras-chave.md](references/palavras-chave.md).

### 4. Estudo de palavras-chave e SERP

```bash
py -3 scripts/semrush_kw.py dominio --dominio cliente.com.br
py -3 scripts/semrush_kw.py descobrir --dominio cliente.com.br --sementes "s1;s2;..."
py -3 scripts/semrush_kw.py serp --dominio cliente.com.br --termos "t1;t2;..."
py -3 scripts/semrush_kw.py volumes --dominio cliente.com.br --arquivo entregas/cliente.com.br/extra/kw.txt
```

A lista `kw.txt` é escrita pela skill: 100 a 160 termos, pelo menos 8 de serviço por linha de produto. Regras em [references/palavras-chave.md](references/palavras-chave.md).

### 5. Concorrentes e autoridade

```bash
py -3 scripts/semrush_kw.py concorrentes --dominio cliente.com.br --lista "a.com.br,b.com.br"
```

Concorrentes são os domínios privados do mesmo mercado que aparecem nas SERPs de serviço. A sugestão automática do Semrush só entra se for do mesmo mercado.

### 6. Velocidade

PageSpeed Insights primeiro. Se responder 429:

```bash
py -3 scripts/lighthouse.py --url https://www.cliente.com.br/ --dominio cliente.com.br
```

### 7. Narrativa Falconi

Escreva `entregas/<dominio>/narrativa.md` na sequência de [references/narrativa.md](references/narrativa.md): problema macro, lacuna, árvore A e B, evidências, Ishikawa, GUT, meta, 5W1H, backlog, modelo de execução. Cada número cita o arquivo de origem. Aplique [references/guardrails.md](references/guardrails.md). Sem preço, salvo pedido. Cases só de [references/cases.md](references/cases.md).

A narrativa é o copy aprovado. Não pare para pedir aprovação de slides.

### 8. Deck

Leia `.cursor/skills/colli-html-ppt/SKILL.md`, `references/design-system.md` e `references/composition-patterns.md` dessa skill. Depois [references/estrutura-deck.md](references/estrutura-deck.md) desta skill.

```bash
py -3 .cursor/skills/colli-html-ppt/scripts/new_deck.py --output entregas/<dominio>/deck
```

Cole `assets/componentes.css` e `assets/icones-extra.svg` desta skill no starter e componha com os blocos de [references/estrutura-deck.md](references/estrutura-deck.md). Não troque a paleta.

### 9. QA visual

```bash
py -3 .cursor/skills/colli-html-ppt/scripts/validate_deck.py entregas/<dominio>/deck/index.html
py -3 scripts/qa_deck.py entregas/<dominio>/deck/index.html entregas/<dominio>/qa
py -3 .cursor/skills/colli-html-ppt/scripts/make_contact_sheet.py entregas/<dominio>/qa/slides --output entregas/<dominio>/qa/sheets
```

Corrija todo erro. Abra cada folha de contato e, em resolução cheia, cada slide denso (tabelas, palavras-chave, 5W1H, backlog). Reprove sobra grande no rodapé, palavra sozinha na última linha de título, colisão com a linha de fonte. Não entregue com erro de console nem slide estourando o quadro.

Empacote `index.html` e `assets/` em `entregas/<dominio>/entrega/` e num ZIP.

## Fechamento

Diga ao usuário:

- caminho do `index.html` e do ZIP;
- domínio, data e banco;
- o que não entrou (fonte falha, GEO sem score, Search Console ausente, PageSpeed sem cota);
- que tráfego do deck é estimativa do Semrush, não clique do Search Console;
- que GUT e metas são leitura da V4.

Deploy na Vercel só com pedido explícito: `vercel deploy --prod --yes` dentro de `entregas/<dominio>/entrega/`, com nome de projeto do cliente.
