---
name: colli-html-ppt
description: Transform approved slide-by-slide text into a complete 1600x900 interactive HTML presentation using the exact Colli&Co visual system, logos, typography, gradients, Liquid Glass, navigation, progress line, responsive centering, visual components, and mandatory slide-by-slide QA. Use after the narrative and slide copy are already defined, whenever the user asks to turn slide text, a presentation outline, proposal, pitch, report, or commercial story into an HTML PPT with the Colli&Co look. Also use when revising an existing Colli&Co HTML deck for spacing, contrast, visual hierarchy, widow words, icon bullets, background cadence, or responsive fit.
---

# Colli HTML PPT

Create a polished HTML slide deck from already approved copy. Treat this as a visual production skill, not a writing skill.

## Non-negotiable contract

1. Preserve the approved meaning, numbers, claims, slide order, and narrative.
2. Do not invent facts, metrics, examples, client context, supporting copy, conclusions, or labels.
3. Permit only punctuation, line-break, capitalization, and microcopy adjustments required by the guardrails.
4. Produce a self-contained HTML presentation sized at 1600x900 per slide.
5. Use the bundled Colli&Co logos. Copy them from `assets/` into the output.
6. Use the bundled starter in `assets/starter/` as the implementation base.
7. Read `references/design-system.md` before composing.
8. Read `references/composition-patterns.md` before selecting slide layouts.
9. Read and execute `references/visual-qa.md` before delivery.
10. Use the in-app Browser for visual validation. Do not approve a deck from source inspection alone.

## Input boundary

Expect one of these:

- numbered slides with titles and copy;
- a table containing slide number, title, and content;
- an approved narrative explicitly divided into slides;
- an existing Colli HTML deck that needs visual corrections.

If copy is not divided by slide, stop and ask for the approved slide structure. This skill must not decide the sales narrative or create missing content.

## Workflow

### 1. Parse without rewriting

Build a content manifest with:

- slide number;
- approved title;
- approved body copy;
- supplied metrics;
- supplied tables or comparisons;
- supplied logo or image assets;
- semantic intent inferred only from the approved text.

Choose a visual form for each slide without adding claims. A supplied list may become cards, a supplied comparison may become a table, and supplied numbers may become charts.

### 2. Scaffold the project

Run:

```bash
python3 scripts/new_deck.py --output /absolute/output/folder
```

This copies the canonical HTML base and Colli&Co logos.

Keep this structure:

```text
output/
├── index.html
└── assets/
    ├── colli-red.png
    ├── colli-white.png
    └── user-supplied-assets
```

Do not use a framework unless the user explicitly requests one. Default to one portable HTML file plus local assets.

### 3. Establish visual rhythm

Before implementing slides, assign:

- one slide archetype from `references/composition-patterns.md`;
- one background treatment;
- one dominant visual object;
- one reading path;
- one intentional focal point.

Never produce a sequence of repeated card grids with only text changes. Vary structure while retaining the same design language.

Use a deliberate background cadence:

- light editorial slides;
- red institutional slides;
- dark depth slides;
- white product or dashboard slides.

Avoid three consecutive slides with the same background and composition unless the user supplied a strict template.

### 4. Compose visually

Convert text into the smallest truthful visual structure:

- metrics into large number cards or provided-data charts;
- comparisons into split panels or tables;
- sequential actions into timelines, flows, or funnels;
- networks into hubs and orbiting nodes;
- capabilities into icon cards;
- conditions into price and condition panels;
- paragraphs into short visual blocks without deleting approved meaning.

Every bullet must include a meaningful outline icon. Use bundled SVG symbols or add matching outline icons. Do not use decorative dots as the final bullet treatment.

Add restrained motion only when it clarifies hierarchy:

- floating or wiggle motion for orbiting nodes;
- pulse or orbit for a central metric;
- staged emphasis for a process;
- subtle chart or bar entrance.

Motion must remain continuous, calm, and professional. Respect `prefers-reduced-motion`.

### 5. Enforce the copy guardrails

Inspect visible slide text and correct:

- hyphens used as prose separators;
- en dashes and em dashes;
- `~` used to mean approximation;
- metalinguage about slides, presentation, AI, prompts, layouts, or the creation process;
- paragraphs that should be visual components;
- bullets without icons;
- a final line containing a single widow word;
- headings with awkward one-word wraps;
- unsupported labels or captions not present in the approved copy.

Use commas, periods, colons, parentheses, line breaks, or visual separation instead of prohibited separators. Never alter numerical meaning.

### 6. Keep the deck centered on every screen

Retain the canonical centering implementation from the starter:

- fixed full-screen viewport;
- deck absolutely positioned at 50% left and top;
- `translate(-50%, -50%) scale(...)`;
- scale calculated from `visualViewport` when available;
- 8px minimum breathing room;
- scale capped at 1 to preserve native 1600x900 sharpness.

Never center only with a fixed transform overwritten by JavaScript.

### 7. Run static checks

Run:

```bash
python3 scripts/validate_deck.py /absolute/output/folder/index.html
```

Fix every error. Review warnings manually. Static checks do not replace browser QA.

### 8. Validate every slide visually

Follow `references/visual-qa.md` exactly.

Minimum approval set:

- every slide captured at 1600x900;
- a contact sheet reviewed;
- dense slides reviewed individually at full resolution;
- all animations verified to move;
- no console errors;
- navigation and progress tested;
- opening state tested at 1024x768, 1366x768, 1600x900, and 1920x1080;
- deck centered and fully visible at every tested size.

Iterate until all slides pass. Do not deliver with known visual debt.

## Output requirements

Deliver:

1. the final `index.html`;
2. its `assets/` folder;
3. a ZIP containing the complete portable presentation;
4. a short verification statement listing the tested viewport sizes.

If the user asks for deployment, use the protected Vercel workflow separately. Do not add deployment logic to this visual skill.

## Absolute prohibitions

- Do not generate PowerPoint XML or `.pptx` unless explicitly requested.
- Do not use lorem ipsum or placeholder copy in the final output.
- Do not fabricate chart data.
- Do not introduce a new brand palette.
- Do not substitute Colli&Co typography with a visually unrelated font.
- Do not use emojis as interface icons.
- Do not approve slides without browser rendering.
- Do not change unmentioned slides during a narrowly scoped revision.
