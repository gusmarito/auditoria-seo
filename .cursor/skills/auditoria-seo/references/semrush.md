# SEMrush

A chave já está no repositório. Não peça chave ao usuário.

## Conexão no Cursor

Arquivo `.cursor/mcp.json` na raiz deste repositório:

```json
{
  "mcpServers": {
    "semrush": {
      "url": "https://mcp.semrush.com/v2/mcp",
      "headers": {
        "Authorization": "Apikey 8160c93e6c32708a48b3a9905339c077"
      }
    }
  }
}
```

O header é `Authorization: Apikey <chave>`, que é o formato do SEMrush. Se o time copiar a skill para outro projeto, cole este bloco dentro do `mcpServers` que já existir. Não apague os outros servidores.

Depois de abrir a pasta, em Settings, Tools & MCP, o servidor `semrush` precisa aparecer conectado. Se não aparecer, recarregue a janela. A coleta por script não depende do MCP: `scripts/coletar.mjs` lê a mesma chave.

Cada consulta gasta unidades da conta. A auditoria padrão fica em poucas chamadas (ranks, orgânico, backlinks, concorrentes e, se preciso, um lote de frases). Não rode dezenas de SERPs à toa.

## O que a coleta pede

Banco padrão: `br`. Só mude com `--database` se o mercado do cliente não for Brasil.

| Chamada | Para que serve no deck |
| --- | --- |
| `domain_ranks` colunas Dn, Rk, Or, Ot, Oc | Rank, keywords, tráfego estimado, custo |
| `domain_organic` colunas Ph, Po, Nq, Cp, Ur, Tr, Td, limite 25, ordem tr_desc | Termos que já trazem tráfego |
| `backlinks_overview` ascore, total, domains_num, urls_num, follows_num, nofollows_num | Autoridade e backlinks |
| `domain_organic_organic` Dn, Cr, Np, Or, Ot, Oc, limite 5 | Concorrentes sugeridos |
| `domain_ranks` de cada concorrente citado | Tabela comparativa |
| `phrase_these` Ph, Nq, Cp, Co, Nr | Volume das frases de categoria |
| `phrase_organic` Dn, Ur, Po, limite 5 | Quem ocupa a SERP da frase |

## Estudo aprofundado

`scripts/semrush_kw.py` usa a mesma chave pela API REST e cobre o estudo de palavras-chave e concorrência. Fluxo e regras em [palavras-chave.md](palavras-chave.md).

| Subcomando | Chamadas | Uso no deck |
| --- | --- | --- |
| `dominio` | domain_organic (100, Url e Kd), domain_rank_history (36 meses), domain_ranks em todos os bancos, backlinks_refdomains, backlinks_ascore_profile, backlinks_tld | problema macro, série histórica, autoridade, versão em outro idioma |
| `descobrir` | phrase_fullsearch por semente | ampliar a lista curada |
| `volumes` | phrase_these em lotes de 100 | estudo por linha de produto e demanda na mesa |
| `serp` | phrase_organic top 10 | quem ocupa a busca e concorrentes reais |
| `concorrentes` | domain_ranks e backlinks_overview | comparativo e Authority Score |

Uma entrega completa gasta da ordem de alguns milhares de unidades. Não repita chamadas sem necessidade: os JSON ficam em `entregas/<dominio>/extra/`.

O MCP do SEMrush (`mcp.semrush.com/v2/mcp`) responde `no_subscription` no plano atual: não traz AI Visibility, Traffic Analytics nem Site Audit. Tudo do deck sai da API REST.

## Como ler o número

- `Organic Traffic` de `domain_ranks` é visita estimada por mês. No slide, chame de tráfego estimado. Nunca chame de clique do Search Console.
- `Traffic (%)` em `domain_organic` é a fatia desse tráfego estimado. Não some essa coluna e chame o resultado de visitas.
- Rank do SEMrush não é posição no Google. Posição é a coluna Position de cada keyword.
- Se a resposta começar com `ERROR`, registre o erro em fonte e lacuna. Não preencha com zero, salvo quando o erro for NOTHING FOUND: aí o indicador é zero e a fonte diz que a API não achou o domínio.
- Participação de marca é a soma de `Traffic (%)` dos termos cuja grafia, sem espaço, contém o token. `mold systems` entra em `moldsystems`. `msys` não entra se ninguém passou `--marca msys`. A lista `keywords_marca` mostra o que entrou na conta. Confira antes de escrever "100% marca". Termo curto e ambíguo, como `mold` sozinho, fica de fora até alguém incluir o token.

## GEO e Semrush One

As auditorias da Axsis e da Mold citam Semrush One (AI Visibility): score, menções, ChatGPT, Gemini, AI Overviews, Modo IA. A API usada pelo script não devolve esse score.

Se o MCP `semrush` estiver conectado e expuser ferramenta de AI Visibility, use o retorno e cite a ferramenta. Se não expuser, o slide de GEO diz que o score de IA não foi coletado. Nesse caso a leitura fica restrita ao que o crawl viu: `llms.txt`, schema, clareza das páginas de serviço. Rotule como leitura do site, não como menção medida.

Não invente menção, share ou variação de 6 meses.
