# Auditoria de SEO · Colli&Co

Skill do Cursor para o time fazer, sozinho, a auditoria de SEO no padrão da Tawa, da Axsis e da Mold Systems. A entrega é um deck HTML 1600x900 no Design System V4. A chave do SEMrush já está no projeto.

## Como usar

1. Clone este repositório.
2. Abra **esta pasta** no Cursor, não a pasta pai.
3. Em Settings, Tools & MCP, confira se `semrush` conectou. Se não aparecer, recarregue a janela. Não precisa colar chave.
4. No chat, peça por exemplo: `Faz a auditoria de SEO de cliente.com.br`.

O deck sai em `entregas/<dominio>/deck/index.html`.

Precisa de Node 18+ e Python 3 (no Windows, o lançador `py`). Não tem `npm install`.

## O que já vem configurado

- Skill `auditoria-seo`, com o roteiro das três auditorias de referência.
- Skill `colli-html-ppt`, o Design System V4 (tokens, starter, logos, QA).
- SEMrush em `.cursor/mcp.json`, no formato `Authorization: Apikey`.
- `scripts/coletar.mjs`, que lê essa mesma chave e grava crawl, PageSpeed e SEMrush.

Se a skill for copiada para outro projeto, copie as duas pastas em `.cursor/skills/` , o script `scripts/coletar.mjs` e o bloco `semrush` do `mcp.json`. O bloco completo está em `.cursor/skills/auditoria-seo/references/semrush.md`.

## Repositório privado

A chave da conta SEMrush está no arquivo de MCP. Mantenha este repositório privado. Cada consulta gasta unidades da conta. Não commite a pasta `entregas/`: ela fica de fora pelo `.gitignore` e mistura dado de cliente.
