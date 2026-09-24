---
name: spendly-ui-designer
description: Generate modern, production-ready UI (Jinja2 templates + CSS) for Spendly, a personal expense-tracker Flask web app (github.com/1AshishJadhav/Spendly). Use this skill whenever the user says things like "design the ___ page", "create UI for ___", "build components for ___", "redesign / improve ___", or otherwise asks for a new or reworked screen, section, or component for Spendly — even if they don't explicitly say "UI" or name this skill. Produces a brief UI structure writeup plus real Jinja2 template code and CSS additions, in a clean fintech-SaaS style consistent with the existing Spendly design (DM Serif Display / DM Sans, card-based layout, Lucide icons via CDN).
---

# Spendly UI Designer

Generates modern, production-ready UI for **Spendly**, a personal expense tracker. Spendly is a server-rendered Flask app — there is no frontend framework, no build step, no npm. Every output from this skill must be real, working code that drops directly into that project structure, not a React component or a standalone mockup.

## Project facts (don't re-derive these — just use them)

- **Stack**: Flask 3 + Jinja2 templates + hand-written CSS + vanilla JS. No React, no Vue, no Tailwind, no Bootstrap, no npm packages, no build tooling.
- **Structure**:
  - `templates/base.html` — shared layout. Every page template extends this with `{% extends "base.html" %}`.
  - `templates/<page>.html` — one template per page.
  - `static/css/style.css` — single hand-written stylesheet, uses CSS custom properties (variables) for theming.
  - `static/js/main.js` — vanilla JS, no dependencies.
- **Fonts**: Google Fonts — `DM Serif Display` for headings, `DM Sans` for body text.
- **Icons**: Lucide, loaded via CDN script tag (no npm). Add once in `base.html` if not already present:
  ```html
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
  <script>
    lucide.createIcons();
  </script>
  ```
  Then use icons inline as `<i data-lucide="wallet"></i>` (or `<i data-lucide="...">` per Lucide's icon names). If `main.js` already initializes Lucide on page load, don't duplicate the `lucide.createIcons()` call — check first.
- **Project status**: marketing pages (landing, legal, auth) are built; the expense-tracking core (dashboard, expense CRUD, categories, budgets) is still being scaffolded — so most requests will be for new pages/components in that core area.

## Before generating anything

1. **Look for the real project files** if they're available in this conversation or workspace (uploaded, or accessible via a connector/repo checkout). Read `base.html` and `style.css` first — actual current CSS variables, spacing scale, and existing component patterns (buttons, cards, nav) always win over the defaults below. Never invent a second design language alongside an existing one.
2. **If the project files aren't available** and the request isn't a first-time / greenfield page, ask the user for the relevant existing template(s) and CSS, or a screenshot of the current design, before generating — per the consistency rule below. Don't guess at colors or spacing that could clash.
3. **Identify the page/component name** and any constraints, data shape, or reference given. If the request is vague (e.g. "design the dashboard" with no detail on what data it shows), make a reasonable assumption based on an expense tracker's typical needs (recent transactions, category breakdown, monthly total, budget progress) and state the assumption briefly rather than stopping to ask — unless nothing reasonable can be assumed.

## Design rules

- **Style**: minimal, clean fintech-SaaS look. Think Mercury, Monzo, Linear — not a generic Bootstrap admin template.
- **Layout**: card-based. Group related info into cards with generous internal padding.
- **Spacing**: consistent 8px grid — all margins/padding/gaps should be multiples of 8px (8, 16, 24, 32...). Use CSS custom properties for spacing if the existing stylesheet already defines them; otherwise define a small set (`--space-1: 8px` etc.) rather than hardcoding scattered pixel values.
- **Corners & shadows**: rounded corners (typically 8–16px radius), soft/subtle box-shadows for elevation — never harsh drop shadows.
- **Color**: subtle, restrained palette. Reuse the existing CSS variables for primary/accent/neutral colors rather than introducing new hex values. If defining new ones (greenfield page), keep it to a small neutral base + one or two accent colors appropriate to a finance app (avoid alarming reds except for genuine warnings like over-budget).
- **Typography**: DM Serif Display for headings/page titles, DM Sans for body and UI text — match existing heading/body hierarchy (sizes, weights) rather than reinventing it.
- **Icons**: Lucide icons (see CDN snippet above) used meaningfully — next to nav items, category labels, empty states, action buttons — not decoratively scattered.
- **Avoid**: generic/dated UI (default browser form styling, boxy unstyled tables, clip-art icons), unstructured code dumps, inline `style=""` attributes (use the stylesheet), clutter, or inconsistent one-off styling choices that diverge from the rest of the page.

## Output format

Every response from this skill has four parts, in this order:

### 1. UI structure (brief)

A short writeup — a few bullet points, not an essay — covering:

- Layout and key sections (what's on the page, top to bottom or by region)
- Notable UX decisions and why (e.g. "budget progress shown as a bar, not a number, for at-a-glance scanning")

### 2. Code

- A complete Jinja2 template (`templates/<name>.html`, `{% extends "base.html" %}`, using `{% block %}`s consistent with `base.html`'s blocks)
- The CSS additions needed, scoped clearly (e.g. a comment header like `/* --- Dashboard page --- */`) and appended to `static/css/style.css` (or written as a snippet to append, if you don't have write access to the real file)
- Modular, minimal: reusable pieces (a card, a stat block) should be easy to lift into a Jinja2 `{% include %}` or macro if the user asks, but don't over-engineer for a single-use page
- No boilerplate padding — every class and element should earn its place

### 3. Design quality check

A one-line confirmation of how the output hits the design rules (modern SaaS feel, spacing/hierarchy, card layout, subtle color) — not a restatement of the code, just a sanity check the user can skim.

### 4. Icons used

List the specific Lucide icon names used and where, so the user can swap them easily if they don't fit.

## Consistency rule

Always match the existing Spendly design over these defaults when the two conflict. If you don't have access to the current templates/CSS and the request isn't clearly greenfield, ask the user for the existing template file(s), `style.css`, or a screenshot before generating — don't produce something that might clash with pages already built.
