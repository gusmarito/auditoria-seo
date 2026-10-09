# Estrutura visual do deck

Parte do starter da skill `colli-html-ppt`. Antes de compor:

1. `py -3 .cursor/skills/colli-html-ppt/scripts/new_deck.py --output entregas/<dominio>/deck`
2. Cole `assets/componentes.css` desta skill dentro do `<style>` do starter, antes de `</style>`.
3. Cole `assets/icones-extra.svg` dentro do `<svg>` de símbolos do starter (adiciona `i-settings`, `i-globe`, `i-link`, `i-x`, `i-drop`, `i-cloud`, `i-mountain`, `i-sat`).
4. Troque as seções de exemplo pelos slides abaixo. Mantenha rodapé, contador, navegação e script do starter.
5. Capturas de tela do cliente vão em `deck/assets/`.

A sequência e o fundo de cada slide estão em [narrativa.md](narrativa.md). Os blocos abaixo são os componentes já aprovados. `{{...}}` é dado da coleta; nada fica sem fonte.

## Linha de fonte (todo slide com número)

```html
<p class="src">Fonte: {{ferramenta e endpoint}}, banco BR, {{mês de ano}}. {{ressalva}}</p>
<!-- em fundo vermelho ou escuro: class="src light" -->
```

## Capa

```html
<section class="slide red active" data-title="Diagnóstico de SEO {{Cliente}}">
  <div class="sphere" style="width:430px;height:430px;right:-80px;top:-115px;opacity:.55"></div>
  <div class="sphere" style="width:245px;height:245px;right:285px;top:115px;opacity:.32"></div>
  <div class="cover-content">
    <div class="brand-lockup">
      <img src="assets/colli-white.png" alt="V4 Company Colli&Co">
      <span class="lockup-sep"></span><span class="client-name">{{cliente}}</span>
    </div>
    <div>
      <span class="eyebrow">Diagnóstico de SEO técnico e de conteúdo · {{domínio}} · {{mês de ano}}</span>
      <h1 class="cover-title" style="max-width:1250px">{{O que o Google conhece hoje.}}<br><span class="accent">{{O que ainda não conhece.}}</span></h1>
    </div>
  </div>
</section>
```

## Sumário

```html
<div class="split-head">
  <div><span class="eyebrow">Sumário</span>
    <h2 style="margin-top:24px;font-size:50px">Do problema macro<br>ao plano de ação</h2>
    <p class="lede" style="font-size:22px;max-width:430px">Partimos do resultado que o site entrega hoje, desdobramos em problemas menores e terminamos em ações com dono, prazo e método. A mesma lógica de gestão de Vicente Falconi.</p></div>
  <ol class="toc">
    <li><span class="toc-n mono">01</span><svg class="icon"><use href="#i-target"></use></svg><b>Problema macro</b><em>{{subtítulo}}</em></li>
    <!-- 02 Desdobramento, 03 SEO técnico, 04 SEO de conteúdo, 05 Causas e prioridades, 06 Plano 5W1H e backlog -->
    <li class="toc-wide"><span class="toc-n mono">07</span><svg class="icon"><use href="#i-users"></use></svg><b>Modelo de execução</b><em>SEO recorrente com especialista sênior V4</em></li>
  </ol>
</div>
```

## Problema macro: barra dividida

```html
<div class="split-bar">
  <div class="sb-seg" style="width:{{59.3}}%;background:rgba(255,255,255,.92);color:#280001"><b>{{59%}}</b><span>Busca pelo nome {{marca}}</span></div>
  <div class="sb-seg" style="width:{{36.8}}%;background:rgba(255,235,200,.55)"><b>{{37%}}</b><span>{{fonte de conteúdo}}</span></div>
  <div class="sb-seg sb-tiny" style="width:{{3.9}}%;background:#280001"></div>
</div>
<div class="sb-legend"><span><svg class="icon"><use href="#i-target"></use></svg>Termos de produto: <b>{{0,26%}} do tráfego</b></span></div>
<div class="glass statement-foot"><svg class="icon"><use href="#i-search"></use></svg><p>{{Quem já conhece encontra. Quem procura o serviço não encontra.}}</p></div>
```

## Lacuna: KPIs e série histórica

```html
<div class="kpi-row">
  <div class="card kpi"><div class="big-number">{{378}}</div><div class="metric-label">visitas estimadas por mês</div></div>
  <div class="card kpi hl"><div class="big-number">{{1 de 64}}</div><div class="metric-label">termos de serviço no top 10</div></div>
  <!-- 4 cards -->
</div>
<div class="card chart-card">
  <div class="chart-head"><b>Tráfego orgânico estimado por mês</b><span class="mono">{{período}} · Semrush BR</span></div>
  <svg class="line-chart" viewBox="0 0 1300 250" preserveAspectRatio="none">
    <line x1="0" y1="128" x2="1300" y2="128" class="gl"/>
    <path class="area" d="{{caminho}} L1290,250 L10,250 Z"/><path class="ln" d="{{caminho}}"/>
  </svg>
  <div class="chart-axis mono"><span>{{mês · valor}}</span><!-- 4 marcos --></div>
</div>
```

Caminho do gráfico: 36 pontos de `sem_history.json` (mais antigo primeiro), x = 10 + i × 1280/35, y = 240 − valor/teto × 230, teto um pouco acima do máximo.

## Árvore do problema

```html
<div class="tree">
  <div class="tree-root"><svg class="icon"><use href="#i-target"></use></svg><span>{{problema macro em uma linha}}</span></div>
  <div class="tree-branches">
    <div class="branch">
      <div class="branch-head"><span class="mono">A</span>SEO técnico<em>O Google consegue ler e confiar no site?</em></div>
      <ul class="leafs"><li><svg class="icon"><use href="#i-page"></use></svg>A1 · {{folha}}</li><!-- 5 folhas --></ul>
    </div>
    <div class="branch"><!-- B · SEO de conteúdo · O Google sabe o que {{cliente}} vende? --></div>
  </div>
</div>
```

## Divisor de parte

```html
<section class="slide dark"><div class="divider"><span class="div-n mono">A</span><div>
  <span class="eyebrow">03 · SEO técnico</span><h2 style="margin-top:24px;font-size:76px">{{pergunta}}</h2><p class="lede" style="max-width:900px">{{frentes}}</p>
</div></div></section>
```

## Placar (n de total)

```html
<div class="score-grid">
  <div class="card sc hl"><div class="sc-n">{{25}}<small>/{{31}}</small></div><div class="sc-bar"><i style="width:{{81}}%"></i></div><div class="metric-label">{{páginas sem título principal (H1)}}</div></div>
  <!-- 6 cards -->
</div>
```

## Evidência com captura

```html
<div class="evid">
  <div><span class="eyebrow">A1 · A porta de entrada</span><h2 style="margin-top:22px;font-size:52px">{{título}}</h2>
    <ul class="mini-list big"><li><svg class="icon"><use href="#i-page"></use></svg><span><b>{{achado}}</b> {{detalhe}}</span></li></ul>
    <div class="effect"><svg class="icon"><use href="#i-target"></use></svg><span>Efeito: {{consequência}}</span></div></div>
  <div class="shots">
    <figure class="shot desk"><img src="assets/home_1440.png" alt=""><figcaption class="mono">Home · 1440 px</figcaption></figure>
    <figure class="shot mob"><img src="assets/home_390.png" alt=""><figcaption class="mono">Home · 390 px</figcaption></figure>
  </div>
</div>
```

## Tabelas

Classe base `tbl`. Variantes: `onp` (on-page), `compact` (velocidade), `kw` (palavras-chave), `serp`, `bench`, `gut`, `w5` (5W1H). Células: `td.bad`, `td.warn`, `td.good`; linha do cliente `tr.hl`. Títulos de página com " - " devem virar " | " (o validador bloqueia hífen separador).

## Velocidade

```html
<div class="speed">
  <div class="gauges">
    <div class="gauge-card card"><div class="ring" style="--p:{{26}}"><span>{{26}}</span></div><b>Mobile</b><span class="mono">performance</span></div>
    <div class="gauge-card card"><div class="ring" style="--p:{{33}}"><span>{{33}}</span></div><b>Desktop</b><span class="mono">performance</span></div>
  </div>
  <table class="tbl compact"><!-- LCP, FCP, TBT, CLS, peso, maior arquivo; colunas Mobile, Desktop, Referência Google --></table>
</div>
```

## Arquitetura: barra empilhada

```html
<div class="stack-bar">
  <div style="flex:{{275}}" class="sbk s1"><b>{{275}}</b><span>posts do blog</span></div>
  <div style="flex:{{31}}" class="sbk s2"><b>{{31}}</b><span>páginas</span></div>
  <!-- s3, s4 -->
</div>
<div class="grid-3" style="margin-top:28px"><div class="card fcard"><div class="icon-box"><svg class="icon"><use href="#i-page"></use></svg></div><h3>{{título}}</h3><p>{{texto}}</p></div></div>
<div class="okline"><svg class="icon"><use href="#i-check"></use></svg><span><b>O que já funciona:</b> {{itens}}</span></div>
```

## Autoridade: barras horizontais

```html
<div class="auth">
  <div class="card"><div class="chart-head"><b>Authority Score do domínio</b><span class="mono">Semrush · 0 a 100</span></div>
    <div class="hbars">
      <div class="hb"><span>{{concorrente}}</span><i style="width:{{AS*2}}%"></i><b>{{AS}}</b></div>
      <div class="hb me"><span>{{cliente}}</span><i style="width:{{AS*2}}%"></i><b>{{AS}}</b></div>
    </div></div>
  <div class="auth-side"><div class="card kpi">...</div><div class="okline">...</div></div>
</div>
```

## Portfólio contra site

```html
<div class="pf-legend"><span class="st ok"><svg class="icon"><use href="#i-check"></use></svg>Página própria · {{n}}</span><span class="st part"><svg class="icon"><use href="#i-expand"></use></svg>Parcial ou citado · {{n}}</span><span class="st no"><svg class="icon"><use href="#i-x"></use></svg>Sem página · {{n}}</span></div>
<div class="pf-grid"> <!-- grid-template-columns: repeat(N linhas, 1fr) -->
  <div class="pf-col"><h3>{{Linha}}</h3>
    <div class="pf ok"><svg class="icon"><use href="#i-check"></use></svg>{{produto}}</div>
    <div class="pf part"><svg class="icon"><use href="#i-expand"></use></svg>{{produto}}</div>
    <div class="pf no"><svg class="icon"><use href="#i-x"></use></svg>{{produto}}</div>
  </div>
</div>
```

## Estudo de palavras-chave (uma linha por slide)

```html
<div class="kw-one"><div class="kwb">
  <div class="kwb-head"><h3>{{Linha}}</h3><span class="mono">{{n}} termos de serviço · {{volume}} buscas por mês</span></div>
  <table class="tbl kw"><thead><tr><th>Termo de serviço</th><th>Volume</th><th>Dificuldade</th><th>{{Cliente}}</th></tr></thead>
    <tbody><tr><td>{{termo}}</td><td>{{volume}}</td><td><span class="kd lo">{{kd}} baixa</span></td><td class="bad">fora do top 100</td></tr></tbody></table>
  <div class="kw-foot">
    <div class="tags"><span class="mono tl">Conteúdo de topo</span><span class="tag">{{termo}} <b>{{volume}}</b></span></div>
    <div class="kw-notes"><p><svg class="icon"><use href="#i-route"></use></svg><span>{{página destino sugerida}}</span></p><p><svg class="icon"><use href="#i-lightbulb"></use></svg><span>{{insight com número}}</span></p></div>
  </div>
</div></div>
<!-- duas linhas pequenas no mesmo slide: <div class="kw-two"> com dois .kwb -->
```

Dificuldade: `kd lo` abaixo de 15, `kd md` de 15 a 29, `kd hi` 30 ou mais, `kd n` sem dado. Até 10 linhas em `kw-one`, 7 em `kw-two`.

## Demanda na mesa (fundo vermelho)

```html
<div class="demand">
  <div class="db"><span class="db-l">{{Linha}}</span><div class="db-t"><i style="width:{{% do maior}}%"></i></div><b>{{volume}}</b><em>{{n no top 10}}</em></div>
</div>
```

## Blog: barras verticais

```html
<div class="blog-grid">
  <div class="card"><div class="chart-head"><b>Posts por ano da última atualização</b><span class="mono">sitemap · lastmod</span></div>
    <div class="vbars"><div class="vb"><b>{{n}}</b><i style="height:{{%}}%"></i><span>{{faixa de anos}}</span></div><!-- 6 faixas --></div></div>
  <ul class="mini-list big">...</ul>
</div>
```

## GEO (fundo escuro)

```html
<div class="grid-3" style="margin-top:40px">
  <div class="glass gcard"><div class="icon-box"><svg class="icon"><use href="#i-check"></use></svg></div><h3>Já existe</h3><p>...</p></div>
  <div class="glass gcard"><div class="icon-box"><svg class="icon"><use href="#i-x"></use></svg></div><h3>Falta</h3><p>...</p></div>
  <div class="glass gcard"><div class="icon-box"><svg class="icon"><use href="#i-dashboard"></use></svg></div><h3>Não medido</h3><p>...</p></div>
</div>
```

## Ishikawa

```html
<div class="ishi">
  <div class="ishi-grid"><div class="ic"><b>Método</b><span>{{causa}}</span></div><!-- Máquina, Medida, Material, Mão de obra, Meio --></div>
  <div class="ishi-spine"><svg class="icon"><use href="#i-arrow-right"></use></svg></div>
  <div class="ishi-head">{{problema macro}}</div>
</div>
```

## Meta (fundo vermelho)

```html
<div class="goals">
  <div class="glass goal"><span class="mono">{{indicador}}</span><div class="g-row"><b>{{atual}}</b><svg class="icon"><use href="#i-arrow-right"></use></svg><b class="to">{{faixa}}</b></div></div>
  <!-- 4 metas -->
</div>
```

## 5W1H

```html
<table class="tbl w5"><thead><tr><th>O quê</th><th>Por quê</th><th>Quem</th><th>Onde</th><th>Quando</th><th>Como</th></tr></thead>
<tbody><tr><td>{{ação}}</td><td>{{A1: evidência}}</td><td>SEO sênior V4; {{cliente}} publica</td><td>{{páginas}}</td><td>Dias 1 a 30</td><td>{{método}}</td></tr></tbody></table>
```

## Backlog em ondas

```html
<div class="waves">
  <div class="wave card"><div class="w-head"><span class="mono">Onda 1</span><b>Dias 1 a 30</b><em>Fundação</em></div>
    <ul class="wl"><li><svg class="icon"><use href="#i-dashboard"></use></svg>{{item}}</li></ul></div>
  <!-- Onda 2 (31 a 60), Onda 3 (61 a 90) -->
  <div class="wave card hl"><div class="w-head"><span class="mono">Contínuo</span><b>Mês 4 em diante</b><em>Crescimento</em></div>...</div>
</div>
```

## Modelo de execução

```html
<div class="exec">
  <div class="exec-why"><div class="ew"><div class="icon-box"><svg class="icon"><use href="#i-layers"></use></svg></div><div><b>Volume</b><span>{{números do backlog}}</span></div></div><!-- Complexidade técnica, Tempo de resposta do Google, Concorrência em movimento --></div>
  <div class="exec-roles">
    <div class="role v4"><span class="mono">V4 · SEO recorrente com especialista sênior</span><ul class="wl">...</ul></div>
    <div class="role rh"><span class="mono">{{Cliente}}</span><ul class="wl">...</ul></div>
  </div>
</div>
```

## Cases, próximos passos e encerramento

Cases: `.grid-2` com `.card.case`, `.case-head` e `.case-grid` (4 números por case, só de [cases.md](cases.md)). Próximos passos: `.steps` com 4 `.step.card`, o último `hl`. Encerramento: `.slide.red` com `.closing`, logo branco e uma frase.
