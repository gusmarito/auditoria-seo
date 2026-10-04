# Mandatory visual QA

## Contents

1. Render setup
2. Slide-by-slide inspection
3. Copy guardrails
4. Layout and contrast
5. Motion and interaction
6. Responsive centering
7. Approval criteria

## 1. Render setup

Use the in-app Browser.

1. Start a local static server in the output folder.
2. Open `http://127.0.0.1:<port>/`.
3. Set the browser viewport to 1600x900.
4. Confirm fonts and all images are loaded.
5. Confirm exactly one slide is active.

## 2. Slide-by-slide inspection

Capture every slide at 1600x900.

Create contact sheets with no more than eight slides each. Inspect:

- hierarchy;
- dead space;
- margin consistency;
- repeated compositions;
- cards too small for the canvas;
- text that appears lost inside large boxes;
- footer collisions;
- visual balance.

Open every dense slide individually at full resolution:

- tables;
- dashboards;
- price slides;
- process slides;
- slides with more than four cards;
- slides with small captions;
- hub and network diagrams.

Do not move to the next slide until the current slide is acceptable.

## 3. Copy guardrails

Inspect rendered text, not only source.

Reject:

- a final line with one isolated word;
- a heading with an accidental one-word wrap;
- prose hyphens;
- en dashes or em dashes;
- approximation tildes;
- metalinguage;
- bullets without icons;
- long continuous paragraphs;
- labels added without source support.

Correct line breaks explicitly with `<br>` or constrained widths. Recheck after font loading.

## 4. Layout and contrast

For each slide verify:

- all content remains inside 1600x900;
- safe margins are respected;
- no element overlaps navigation, counter, footer, or progress;
- primary reading text has strong contrast;
- glass text remains readable over the brightest gradient region;
- dark-slide cards explicitly set text colors;
- the composition fills the usable vertical space;
- whitespace is intentional and balanced;
- visual elements are aligned geometrically.

Do not rely on generic overflow checks alone. A technically contained slide can still be visually empty or badly distributed.

## 5. Motion and interaction

Verify:

- floating nodes actually change transform values;
- animated rings or pulses change over time;
- nodes use staggered delays;
- previous and next buttons work;
- keyboard arrows work;
- the first previous button and final next button are disabled;
- slide counter updates;
- progress reaches 100%;
- reduced-motion mode disables decorative animation.

Check browser console warnings and errors. Deliver only with an empty error log.

## 6. Responsive centering

Test:

- 1024x768;
- 1366x768;
- 1600x900;
- 1920x1080.

At every viewport calculate the deck rectangle.

Pass only when:

- left margin equals right margin within 1px;
- top margin equals bottom margin within 1px;
- the full deck is visible;
- no browser zoom change is needed;
- scale never exceeds 1.

Canonical implementation:

```css
#deck {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%) scale(var(--deck-scale, 1));
  transform-origin: center;
}
```

```js
function fitDeck() {
  const viewportWidth =
    window.visualViewport?.width ||
    document.documentElement.clientWidth ||
    window.innerWidth;
  const viewportHeight =
    window.visualViewport?.height ||
    document.documentElement.clientHeight ||
    window.innerHeight;
  const scale = Math.max(
    .1,
    Math.min(
      (viewportWidth - 16) / 1600,
      (viewportHeight - 16) / 900,
      1
    )
  );
  deck.style.setProperty("--deck-scale", scale);
}
```

## 7. Approval criteria

A deck is complete only when:

- static validator returns no errors;
- every slide was rendered and inspected;
- all requested assets load;
- no visible copy violates the guardrails;
- no slide has accidental dead space;
- no repeated background sequence feels mechanical;
- all motion is calm and functional;
- all four viewport tests pass;
- browser console has no errors;
- a portable ZIP opens correctly.
