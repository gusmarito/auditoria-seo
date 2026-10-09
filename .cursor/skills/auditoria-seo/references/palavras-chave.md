# Estudo de palavras-chave

A skill levanta o portfólio e as palavras-chave sozinha. Não espere lista de produtos nem de termos. Se o usuário mandar uma planilha de produtos, use como complemento e cite como fonte; se não mandar, o site é a fonte.

## 1. Levantar o portfólio pelo site

Fontes, nesta ordem:

1. Menu e rodapé da home (links de serviços, soluções, produtos, áreas).
2. Página índice de serviços ou soluções: liste todo serviço citado, com link ou só em texto.
3. URLs do sitemap com `/servicos/`, `/solucoes/`, `/produtos/`, `/areas/` e similares (`crawl_resumo.md`).
4. Texto das páginas de serviço: produtos com nome próprio (plataformas, marcas) e mercados atendidos.

Monte `entregas/<dominio>/extra/portfolio.md`: linha de produto, produto, URL própria (ou "sem página"), status:

- **página própria**: URL dedicada ao produto;
- **parcial**: citado dentro de outra página ou coberto por página genérica;
- **sem página**: só em lista de texto ou ausente do site.

Agrupe em 3 a 6 linhas de produto. Elas viram as colunas do slide B1 e os slides B2.

## 2. Sementes e lista curada

Para cada produto, escreva os termos que o **comprador** digitaria. Use o vocabulário do mercado brasileiro, não o nome interno do produto:

- nome do serviço e sinônimos ("dam break", "estudo de ruptura de barragem", "rompimento de barragem");
- forma de contratação: "estudo de", "projeto de", "consultoria em", "laudo", "empresa de";
- norma ou exigência que gera a compra ("outorga de lançamento de efluentes", "resolução conjunta ANA ANEEL 127");
- problema que o serviço resolve ("risco de inundação", "descaracterização de barragem");
- marca própria de plataforma, mesmo com volume baixo.

Separe cada termo como `servico` (fundo de funil, intenção de contratar) ou `conteudo` (topo de funil técnico, que atrai o mesmo público e serve de ponte para a página de serviço).

Rode a descoberta com 8 a 12 sementes curtas, uma por linha ou tema:

```bash
py -3 scripts/semrush_kw.py descobrir --dominio cliente.com.br --sementes "barragem;drenagem;outorga;autodepuração"
```

Leia `sem_descoberta.json` e aproveite só o que for do mercado. Correspondência ampla traz muito ruído de consumidor ("drenagem linfática", "barragem de Brumadinho", "previsão do tempo SP"). Descarte.

Grave `entregas/<dominio>/extra/kw.txt` no formato `LINHA|tipo|termo`, de 100 a 160 termos, com pelo menos 8 de serviço por linha de produto:

```text
Hidrologia|servico|estudo hidrológico
Hidrologia|conteudo|hidrograma
```

## 3. Volumes, dificuldade e posição

```bash
py -3 scripts/semrush_kw.py dominio --dominio cliente.com.br
py -3 scripts/semrush_kw.py serp --dominio cliente.com.br --termos "termo1;termo2;..."
py -3 scripts/semrush_kw.py volumes --dominio cliente.com.br --arquivo entregas/cliente.com.br/extra/kw.txt
```

Rode `dominio` e `serp` antes de `volumes`: o `kw_study.json` cruza a posição do cliente vinda de `sem_organic_full.json` e de `sem_serps.json`.

Para a SERP, escolha 15 a 20 termos de serviço com volume, pelo menos 2 por linha. Leia `_contagem_dominios`: os domínios privados do mesmo mercado que aparecem com página de serviço são os concorrentes reais. Governo, universidade, Wikipedia, YouTube e portais de notícia não são concorrentes; são espaço que uma página técnica disputa.

```bash
py -3 scripts/semrush_kw.py concorrentes --dominio cliente.com.br --lista "a.com.br,b.com.br,c.com"
```

Deixe fora do comparativo o concorrente cujo tráfego vem de outro público (ex.: consultoria de clima com portal de previsão do tempo ao consumidor) e diga isso na fonte.

## 4. Leitura para o deck

- **Problema macro**: fatia do tráfego por marca, por conteúdo e por produto, somando `Traffic (%)` de `sem_organic_full.json`.
- **Lacuna**: termos de serviço no top 10 sobre o total de termos de serviço; soma do volume de serviço.
- **B2 por linha**: até 10 termos de serviço por volume, com dificuldade (baixa abaixo de 15, média de 15 a 29, alta de 30 para cima) e posição do cliente ("fora do top 100" quando não aparece). Até 4 tags de conteúdo de topo. Uma página destino sugerida e um insight que cite número.
- **Demanda na mesa**: soma por linha e quantos termos no top 10.
- Termo genérico demais ("peer review", "ETA", "geotecnia" sozinho) não entra na soma, ou entra com a ressalva no insight.

Volume abaixo de 20 buscas não é medido pelo Semrush. Em engenharia e B2B técnico isso é normal; o argumento é valor por contrato, não volume. Escreva isso no slide de demanda.
