---
name: auditoria-seo
description: >-
  Gera auditoria de SEO e visibilidade em IAs (GEO) no padrão Colli&Co das
  auditorias Tawa, Axsis e Mold Systems. Coleta SEMrush, crawl e PageSpeed e
  entrega deck HTML 1600x900 no Design System V4. Use quando pedirem auditoria
  de SEO, diagnóstico de site, GEO, visibilidade em IA, funil orgânico ou deck
  de SEO de um domínio.
---

# Auditoria de SEO

Entrega o diagnóstico que a Colli&Co já fez para Tawa, Axsis e Mold Systems: prova coletada, leitura de marca contra categoria, GEO e plano. A peça final é um deck 1600x900 no Design System V4, skill `colli-html-ppt` nesta mesma pasta.

Quem clonou o repositório não configura nada. Não peça token, não peça para abrir Settings, não peça para instalar Node ou Python, não peça para copiar skill para outro projeto. Faça você.

## Ambiente

A raiz do workspace é este repositório. A chave do SEMrush já está em `.cursor/mcp.json`. O script lê essa chave mesmo se o MCP não aparecer conectado na interface.

Antes da coleta, confira as ferramentas. Se faltar, instale e siga. Não pare para pedir autorização.

No Windows:

```bash
node -v
py -3 --version
```

Node precisa ser 18 ou mais novo. Se `node` não existir:

```bash
winget install --id OpenJS.NodeJS.LTS -e --scope user --accept-package-agreements --accept-source-agreements --disable-interactivity
```

Se `py` e `python3` não existirem:

```bash
winget install --id Python.Python.3.12 -e --scope user --accept-package-agreements --accept-source-agreements --disable-interactivity
```

Feche e reabra o terminal se o comando novo não entrar no PATH. Não há `npm install`.

Não commite a pasta `entregas/`. Ela está no `.gitignore`.

## Antes de coletar

Confirme o domínio. Banco padrão: Brasil. Se o usuário não disser o mercado, use `br` e escreva isso na fonte.

Não bloqueie a auditoria por falta de concorrente, frase ou preço. Concorrente e frase de categoria saem do site e do SEMrush. Preço segue [references/guardrails.md](references/guardrails.md) quando o usuário não passar outro.

Se o usuário colar Search Console, GA4 ou uma pauta de check-in, isso entra como fonte nomeada.

## Fluxo

```text
- [ ] 1. Coletar
- [ ] 2. Frases de categoria, se o orgânico for só marca
- [ ] 3. Narrativa com fonte em cada número
- [ ] 4. Deck no design system
- [ ] 5. QA visual
```

### 1. Coletar

Na raiz deste repositório:

```bash
node scripts/coletar.mjs --dominio dominio.com.br
```

Com marca e concorrentes, quando o usuário tiver passado:

```bash
node scripts/coletar.mjs --dominio dominio.com.br --marca "marca,apelido" --concorrentes "a.com.br,b.com.br"
```

Leia [references/coleta.md](references/coleta.md) e [references/semrush.md](references/semrush.md). Leia `entregas/<dominio>/resumo.json` por completo. Não invente número ausente.

### 2. Frases de categoria

Se a participação de marca passar de 70%, ou se não houver termo de serviço no top 20, escolha até 8 frases que o comprador usaria. Baseie-se no que o site vende, não numa lista genérica. Rode de novo com `--frases` e os mesmos `--dominio`, `--marca` e `--concorrentes`.

### 3. Narrativa

Escreva `entregas/<dominio>/narrativa.md` na ordem de [references/narrativa.md](references/narrativa.md). Cada número cita a chave do resumo ou o arquivo em `_raw/`. Aplique [references/guardrails.md](references/guardrails.md). Cases só com [references/cases.md](references/cases.md).

Captura visual do site do cliente: se houver browser, abra a home em 1440 e em 390, mais a página de contato e a home de um concorrente. Salve em `entregas/<dominio>/evidencias/`. Sem captura, não afirme defeito de layout.

### 4. Deck

A narrativa deste fluxo é o copy aprovado. Não pare para pedir slides de novo.

Leia e siga, nesta ordem, a skill visual do repositório:

1. `.cursor/skills/colli-html-ppt/SKILL.md`
2. `.cursor/skills/colli-html-ppt/references/design-system.md`
3. `.cursor/skills/colli-html-ppt/references/composition-patterns.md`

No Windows, `python3` costuma ser `py -3`.

```bash
py -3 .cursor/skills/colli-html-ppt/scripts/new_deck.py --output entregas/<dominio>/deck
```

Componha `entregas/<dominio>/deck/index.html` a partir do starter. Logos da Colli&Co vêm da pasta copiada pelo script. Não troque a paleta.

### 5. QA

```bash
py -3 .cursor/skills/colli-html-ppt/scripts/validate_deck.py entregas/<dominio>/deck/index.html
```

Corrija todo erro. Siga `.cursor/skills/colli-html-ppt/references/visual-qa.md` no browser: cada slide em 1600x900, navegação, e a abertura em 1024x768, 1366x768, 1600x900 e 1920x1080. Não entregue com erro de console nem slide estourando o quadro.

## Fechamento

Diga ao usuário:

- caminho do `index.html`;
- domínio, data e banco;
- o que não entrou (fonte falha, GEO sem score, Search Console ausente);
- que tráfego do deck é estimativa do SEMrush, não clique do Search Console.

Não faça deploy, salvo pedido explícito.
