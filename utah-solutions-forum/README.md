# Utah Solutions Forum — landing page

Implementation of `templates/utah-solutions-forum/UtahSolutionsForum.dc.html` from the
**BLOOM Civic Host Design System** design project
(`4ca1912f-e87e-4610-8bfa-1cad009d1f91`).

Single-page landing site for the Utah citizens' assembly, 18–19 September 2026, Lehi.
This is a **separate artifact** from `../utah-decision-map-delegates.html` — that page is
delegate background material and runs its own type system (Archivo / Source Serif 4 /
IBM Plex Mono). This one runs on the Civic Host kit.

## Files

| File | Role |
|---|---|
| `index.html` | The page. Publish this one. |
| `usf.css` | Page-specific styles only — everything the kit already covers is left to the kit. |
| `assets/utah-common-ground-logo.avif` | Host logo, 690×186, transparent. Pulled from the design project. |
| `assets/bloom-project-logo.png` | Partner logo, 2396×961, transparent. Pulled from the design project. |

Design system comes from `../bloom-civic-host-kit/kit.css`, which is the local binding of
the same system — its tokens were checked line-for-line against the project's
`tokens/colors.css` and are identical, so there is no third palette in play here.

Open it directly; there is no build step.

```bash
open utah-solutions-forum/index.html
```

## How the design concept maps to real code

The `.dc.html` is a design-concept file: it renders through a React runtime (`support.js`)
that resolves `<x-import>`, `<sc-if>`, and `{{ }}` bindings. None of that ships. Every
component it imports already exists as a real class in `kit.css`:

| Design concept | Implementation |
|---|---|
| `<x-import …Eyebrow>` | `<span class="eyebrow">` |
| `<x-import …Eyebrow onDark>` | `<span class="eyebrow on-dark">` |
| `<x-import …Button size="lg">` | `<a class="btn btn-primary btn-lg">` |
| `<x-import …Button variant="ghost" size="lg">` | `<a class="btn btn-ghost btn-lg">` |
| `<x-import …Caveat>` | `<p class="caveat">` |
| `<helmet>` | real `<head>` |
| `<sc-if>` pair + `DCLogic` state | ~15 lines of vanilla JS at the bottom of `index.html` |
| `hint-size`, `hint-placeholder-val` | dropped — design-time hints only |

The concept's heavy inline styles were replaced by kit classes wherever the kit has one
(`.tint-pine`, `.tint-paper2`, `.tint-gold`, `.card`, `.card-commit`, `.tool`, `.band`,
`.band-grid`, `.band-cell`, `.wrap`, `.caveat`). What remained genuinely page-specific —
sticky header, hero figures, the five-stage arc, the panel table, the form, the footer —
is in `usf.css`.

`ds-base.js` and `support.js` are not carried over by design: the first is the design-time
loader for the DS token files and `_ds_bundle.js`, both already inside `kit.css`; the second
is the React runtime that only exists to render `.dc.html` inside the design tool.

## Deliberate departures from the concept

Three, all small:

1. **Skip link uses `:focus`, not JS.** The concept moved it with `onFocus` / `onBlur`
   handlers. CSS does the same job and survives script failure.
2. **BLOOM logo is 40px tall, not 34px.** That PNG carries roughly 30% transparent padding
   of its own, so at 34px it renders optically much smaller than the Utah Common Ground
   mark beside it. 40px matches them by eye while keeping BLOOM subordinate, which is the
   ranking the concept intended.
3. **Hero figures are borderless.** Matching the concept, which deliberately did not use
   the kit's `.stat` card here.
4. **Sticky header shrinks below 520px.** At the concept's sizes the title wrapped to two
   lines inside a 64px sticky bar. The title and date now step down slightly so both hold
   one line at 375px.

Two bugs were found and fixed while building, both worth knowing about if this CSS is
copied elsewhere:

- `.usf-arc-now::before` / `.usf-arc-ahead::before` lost to `.usf-arc li::before` on
  specificity, which silently rendered the "Next" and "Ahead" milestones as ordinary
  completed pine dots. The modifiers now carry the `li`.
- `[hidden]{display:none!important}` is required because `.usf-form{display:flex}` is an
  author rule and outranks the UA's `[hidden]{display:none}`. Without it the sign-up form
  stays visible after submit.

## Before this is published

The concept is explicit that this page is a draft, and it carries its own "Draft — pending
review" and "To be confirmed" markers. Carried forward verbatim, plus what implementation
surfaced:

- [ ] **The sign-up form has no backend.** Submitting shows the confirmation and discards
      the address. Wire a real endpoint, or remove the form, before this goes live. This is
      the most likely thing to embarrass someone.
- [ ] **Two placeholder links** still point at `#`: "Read the full selection methodology"
      and "Read a general explainer".
- [ ] **`og:image` points at `./share-image.png`, which does not exist.** Either add the
      share image or drop the tag — a broken one is worse than none.
- [ ] **"About 540 Utahns weighed in"** — confirm the figure. `prototyping/CLAUDE.md` already
      flags a related unverified number (~1,000 residents engaged across Utah + Oregon).
- [ ] **Panel-against-Utah table is all em-dashes**, by design, until the panel is confirmed.
- [ ] **Poll findings, the three learning materials, funders, and all three contact
      addresses** are marked pending in the copy.
- [ ] **Nonpartisan notice** is marked "Draft — pending review" and should get a real review
      before publishing, given what it commits the Forum to.

Page copy is carried over verbatim from the design concept, so copy edits belong upstream in
the design project rather than here — otherwise the two drift.

## One inconsistency worth fixing upstream

The template imports `…Caveat`, but the design project has no `Caveat` component —
`components/core/` holds Button, Chip, CountBadge, EchoBadge, Eyebrow, and StatTile, and
there is no `Caveat.jsx` / `.d.ts` / `.prompt.md` anywhere in the tree. The `.caveat` class
does exist in `kit.css`, which is why this page renders correctly, but the component is
missing from the system it claims to import from.
