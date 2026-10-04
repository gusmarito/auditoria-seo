# Guardrails da auditoria

## Número

- Todo número do deck sai de `resumo.json`, de `_raw/`, de um case deste repositório ou de um dado que o usuário colou na conversa.
- Se a fonte falhou, o slide registra a lacuna. Exemplo real das auditorias de referência: concorrente que bloqueia crawl; Search Console ausente porque o cliente ainda não é de SEO ativo.
- Tráfego estimado é Organic Traffic do SEMrush. A frase "não é clique do Search Console" entra no slide de tráfego e no slide de projeção.
- Projeção é faixa de 12 meses. Não é meta contratual. Não prometa posição no Google.
- Title e meta "como ficaria" são proposta. O slide diz isso.
- Não converta `Traffic (%)` em visitas multiplicando no escuro. Se precisar de visitas por termo e a API não trouxe a visita absoluta, mostre volume, posição e a fatia.

## Faixa de projeção

Use só quando houver tráfego atual medido e pelo menos um termo de categoria com volume.

- Tráfego atual abaixo de 500 e a categoria existe fora do top 10: piso = atual, teto = no máximo 3 vezes o atual, arredondado. A faixa da Axsis (200 para 400 a 700) e da Mold institucional (301 para 450 a 700) cabe nesse teto.
- Tráfego atual alto e mais de 70% em marca, login ou navegação: o total sobe no máximo cerca de 40%. O número que importa é termo de categoria, hoje em zero, indo para uma faixa curta (10 a 20 no top 20), sem garantir a posição de uma palavra. Foi a leitura da MSYS Imob.
- Sem volume de categoria medido: não projete tráfego. Escreva que falta base.
- PageSpeed mobile: faixa 70 a 85 só com score atual medido e vilão corrigível (redirect, imagem, fonte, tag). Não projete 100.

Premissa obrigatória: a V4 especifica e o cliente publica, salvo quando o usuário disser que a V4 também publica.

## Quando recomendar site novo

A frente Site N1 entra só se a evidência mostrar que o site atual não carrega a estratégia. Sinais usados na Tawa: sem página por oferta, sem formulário, template com dado falso, mobile quebrado na primeira dobra com captura de tela. Remendo de title e meta fica na onda de 30 dias mesmo assim.

Sem essa evidência, a proposta é só SEO Growth, como na Axsis.

## Preço padrão

Use somente se o usuário não passar outro valor.

| Frente | Condição | Valor |
| --- | --- | --- |
| SEO Growth | sempre que houver proposta | R$ 4.500 por mês, 12 meses, 4 posts por mês |
| Site novo N1 | só no caso acima | R$ 12.000, entrega única, 60 a 90 dias |
| As duas juntas | desconto de 20% só no SEO | SEO a R$ 3.600 por mês. Site diluído em 12 parcelas de R$ 1.000. Mês somado R$ 4.600. Ciclo R$ 55.200 |

Escopo do SEO Growth, igual nas auditorias de referência: auditoria técnica contínua, indexação, schema, titles, descriptions, headings, keywords e intenção, 4 posts por mês, linkagem interna, backlinks, SEO local, monitoramento, relatório e reunião mensal.

## Voz

Português do Brasil. Frase curta. Consequência de negócio na mesma tela do número.

Cada achado tem três partes: o número, a prova, o que isso faz no comercial.

Evite jargão sem tradução na mesma frase. Open Graph vira "imagem de compartilhamento". H1 vira "título principal" na primeira menção.

Não use travessão, til de aproximação nem hífen como separador de frase. Não fale de slide, prompt, IA que gerou o deck ou layout.

Não descreva defeito visual sem captura. Se o browser não abriu o site, o deck não afirma contraste, card quebrado ou botão por cima de texto.

## O que fica de fora

Search Console, GA4 e Bing não entram sem export ou acesso que o usuário entregou. O placar de medição (tag instalada ou não) vem do HTML e pode entrar. Clique e impressão reais não vêm da tag; vêm do export.
