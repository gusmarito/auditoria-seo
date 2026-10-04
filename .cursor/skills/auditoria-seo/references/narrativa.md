# Narrativa do deck

A entrega é um deck HTML 1600x900 no Design System V4, no mesmo gênero das auditorias da Axsis, da Mold Systems e da Tawa: diagnóstico com prova, leitura de marca contra categoria, GEO e plano. A Tawa saiu em página longa; aqui a mesma lógica vira slide, que é o formato da Axsis e da Mold.

Não encha slide sem evidência. O miolo abaixo é obrigatório. O restante entra só quando a coleta tiver o fato.

## Obrigatório

1. Capa. Cliente, domínio, mês da coleta, uma frase do diagnóstico. Fundo vermelho institucional.
2. Percurso. Três blocos: técnico, busca e GEO, plano. Lista a stack que de fato rodou.
3. Método. O que entrou e o que falhou. Páginas rastreadas, SEMrush, PageSpeed. Search Console e GA4 só se existirem.
4. Leitura de negócio. Por que a busca importa neste cliente, em uma tela. Ciclo, comitê ou balcão, e se hoje o Google entrega marca ou categoria. Sem texto genérico de "SEO é importante".
5. Placar. H1, meta description, Open Graph, schema, formulário, medição, keywords, tráfego estimado.
6. Palavras-chave. Keywords, tráfego estimado, top 3, top 10, fatia de marca. Fonte com banco e data.
7. Demanda na mesa. Termos com volume em que o domínio está mal ou ausente. Sem receita inventada.
8. Fundação. robots, sitemap, llms.txt, última atualização se o sitemap trouxer lastmod.
9. On-page. Tabela curta: title, H1, meta, canonical, schema. Destaque o pior padrão, não a lista inteira se passar de uma tela.
10. PageSpeed. Desktop e mobile, LCP, CLS e bloqueio, só com os valores medidos.
11. Impacto. Quatro achados no máximo, cada um ligando número a consequência comercial.
12. Projeção 12 meses. Atual e faixa, com a regra de [guardrails.md](guardrails.md).
13. Plano 30, 60 e 90 dias. Mais o contínuo de 4 posts por mês quando a proposta for SEO Growth.
14. Próximo passo. O que a V4 faz e o que precisa do cliente.

## Quando a evidência existir

- Intenção de busca, se `--frases` ou a amostra orgânica permitir separar marca, categoria e dúvida.
- Concorrentes, no máximo três, mesma métrica dos dois lados. Sugestão automática do SEMrush só entra se o domínio for do mesmo mercado. Outro setor, ou tráfego irrelevante, fica de fora.
- Captura e medição, no peso da Tawa, quando não houver formulário, GA4, GTM ou pixel.
- Erro concreto de credibilidade (dado de template, data impossível, e-mail inválido), com a citação do HTML.
- Conteúdo parado ou página de oferta inexistente.
- GEO. Primeiro o que é, no negócio deste cliente. Depois o que foi medido. Se o score de IA não veio, diga isso e limite a leitura a llms.txt e páginas citáveis.
- Snippet atual contra snippet proposto, marcado como proposta.
- Backlinks e autoridade, se a API devolveu.
- Cases KCE e Marine, com os números de [cases.md](cases.md), numa tela ou duas.
- Proposta. SEO Growth. Site N1 só na condição do guardrail. Preço padrão só se o usuário não passou outro.

## Cadência visual

Alterne fundo claro, branco, escuro e vermelho. Não repita o mesmo grid três vezes. Números viram card grande. Comparação vira tabela. Onda de 30, 60 e 90 vira sequência. A produção visual segue a skill `colli-html-ppt` deste repositório: starter, design system, composição e QA.

## Como um achado é escrito

```text
Título: a consequência, não o nome da tag
Número: 0 de 6 páginas com meta description
Prova: a home entra no Google como "Home | Marca", sem texto de apoio
Efeito: quem pesquisa o serviço não lê a oferta
Fonte: crawl HTML · dominio · mês/ano · N páginas
```

A Mold abre pelo que trava (redirect, velocidade, erro). A Axsis abre pelo comprador B2B e pela marca contra a categoria. A Tawa abre pelos pontos que o cliente já tinha levantado, confirmados ou piores. Escolha a porta de entrada conforme o material do usuário. Se ele não trouxe pauta, abra pela marca contra a categoria, que é o eixo das três.
