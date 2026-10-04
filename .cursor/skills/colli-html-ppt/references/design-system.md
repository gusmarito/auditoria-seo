# Colli&Co presentation design system

## Contents

1. Brand assets
2. Color tokens
3. Typography
4. Backgrounds
5. Liquid Glass
6. Cards and controls
7. Iconography
8. Slide geometry
9. Motion

## 1. Brand assets

Use the bundled assets:

- `assets/colli-red.png` on light backgrounds;
- `assets/colli-white.png` on red and dark backgrounds.

Footer logo:

- width: 155px;
- height: 48px;
- object fit: contain;
- align to the left safe margin;
- hide on cover and final hero slides when the large logo is already present.

Never redraw, recolor, distort, crop, or typeset the Colli&Co logo.

## 2. Color tokens

```css
:root {
  --v4-red: #e50914;
  --v4-red-hover: #c40712;
  --v4-orange: #ff481f;
  --v4-flame: #f0141e;
  --v4-dark: #280001;
  --v4-darker: #280000;
  --v4-grey: #e1dcdc;
  --v4-white: #ffffff;
  --v4-cream: #ffebc8;
  --v4-salmon: #ffb4a0;
  --ink: #141414;
  --ink-soft: #5a5a5a;
  --line: rgba(20, 20, 20, .12);
  --radius: 22px;
  --radius-pill: 999px;
}
```

Primary color is always V4 red. Orange is a heat and transition accent, not a replacement primary.

## 3. Typography

Use:

- IBM Plex Sans for all presentation text;
- IBM Plex Mono for slide numbers, periods, captions, and compact data labels.

Recommended 1600x900 scale:

```css
h1 { font-size: 88px; line-height: .98; letter-spacing: -.055em; font-weight: 600; }
h2 { font-size: 60px; line-height: 1.02; letter-spacing: -.045em; font-weight: 600; }
h3 { font-size: 26px; line-height: 1.1; letter-spacing: -.025em; font-weight: 600; }
.lede { font-size: 27px; line-height: 1.42; font-weight: 300; }
.eyebrow { font-size: 12px; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; }
```

Use large type confidently. Reduce font size only after adjusting width, line breaks, card geometry, or layout.

Avoid:

- headings below 48px;
- card titles below 20px;
- body copy below 17px;
- long all-caps text;
- centered paragraphs wider than 900px.

## 4. Backgrounds

Institutional hero:

```css
background: radial-gradient(
  120% 130% at 50% -10%,
  #ff5a2c 0%,
  #e50914 30%,
  #b00610 62%,
  #280001 100%
);
```

Dark depth:

```css
background:
  radial-gradient(circle at 78% 15%, rgba(229,9,20,.5), transparent 32%),
  linear-gradient(145deg, #280001 0%, #130001 100%);
```

Light editorial:

```css
background:
  radial-gradient(circle at 92% 8%, rgba(229,9,20,.055), transparent 24%),
  #f5f4f2;
```

White product:

```css
background: #fff;
```

Use top accent lines on light slides. Use glass spheres sparingly on red hero slides.

## 5. Liquid Glass

```css
.glass {
  position: relative;
  background: rgba(255,255,255,.06);
  backdrop-filter: blur(14px) saturate(140%);
  border: 1px solid rgba(255,255,255,.35);
  border-radius: 22px;
  box-shadow:
    inset 0 0 150px rgba(255,255,255,.13),
    inset 0 1px 10px rgba(255,255,255,.38),
    inset 0 -2px 10px rgba(255,255,255,.22),
    inset 0 0 100px rgba(255,255,255,.08),
    -5px 5px 20px rgba(0,0,0,.10);
}
```

Add a warm lower highlight with a pseudo-element. Glass is a depth treatment, not a substitute for readable contrast.

## 6. Cards and controls

Cards:

- white fill;
- 1px `rgba(20,20,20,.12)` border;
- 22px radius;
- internal padding from 22px to 38px;
- subtle shadows only on emphasis cards.

Badges:

- pill radius;
- compact uppercase label;
- light red tint on light slides;
- translucent white glass on dark slides.

Navigation:

- 48px circular buttons;
- bottom right;
- previous and next outline arrows;
- disabled state at 30% opacity.

Progress:

- 7px bottom track;
- fill is `linear-gradient(90deg, #e50914, #ff481f)`;
- width follows current slide divided by total slides.

## 7. Iconography

Use only:

- outline SVG icons;
- 24x24 viewBox;
- 2px to 2.3px stroke;
- round caps and joins;
- no fill unless the component intentionally uses a solid status mark.

Place icons inside 50px to 68px rounded containers with a light red background. On dark slides, use translucent white containers.

Never use emojis, stock icon screenshots, or mismatched icon families.

## 8. Slide geometry

Native slide:

- width: 1600px;
- height: 900px;
- safe padding: 76px top, 96px sides, 108px bottom;
- footer logo baseline: 32px from bottom;
- controls: 25px from bottom and 52px from right.

Keep content above the footer and navigation region. Intentionally distribute content through the usable vertical area.

## 9. Motion

Use calm motion:

```css
@keyframes node-float {
  0%, 100% { transform: var(--node-base, translate(0,0)) translateY(0) rotate(0deg); }
  25% { transform: var(--node-base, translate(0,0)) translateY(-9px) rotate(-1.5deg); }
  50% { transform: var(--node-base, translate(0,0)) translateY(3px) rotate(1deg); }
  75% { transform: var(--node-base, translate(0,0)) translateY(-5px) rotate(.5deg); }
}
```

Use different negative delays so nodes do not move in sync. Provide a `prefers-reduced-motion` override.
