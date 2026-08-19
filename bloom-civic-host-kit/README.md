# BLOOM Civic Host — UI Kit

A warm, editorial system used for the Civic Host cohort invitation and the community-forum
data pages. **This is a distinct system from the marketing-site tokens in the project root's
`colors_and_type.css` — the two are not variants of each other, and importing both will
produce conflicts.**

| | `colors_and_type.css` (marketing) | `kit.css` (this kit) |
|---|---|---|
| Display / body | Inter | Geom / Hanken Grotesk |
| Mono | JetBrains Mono | DM Mono |
| Primary accent | coral `#D4573B` | gold `#EE503B` |
| Heading color | maroon `#6B2A3D` | ink `#432004` |
| Page surface | white / gray-50 | paper `#FFF8F1` / `#FFFDF9` |
| Second accent | — | pine `#406B43` |
| Elevation | shadow scale | hairline borders only |

## Files

- `kit.css` — the whole system: tokens, base element styles, and every component class.
  Self-contained; loads its own fonts. Does not import `colors_and_type.css`.
- `index.html` — an assembled demo page showing the components in context.
- `preview/` — the Design System pane cards, one component group per file.
  `preview/_card.css` mirrors the root `preview/_card.css` utilities so the helpers
  (`.row`, `.gap-*`, `.mt-*`, `.tag`) are identical across both kits; only the token
  import differs.

## Where it came from

- **Palette, type, eyebrows, buttons, stat tiles, dark band, tool cards, pull quotes, dashed
  commit cards** — `bloom-civic-host-invitation.html`
- **Ledger rows, cluster cards, actor tags, dot states, count and echo badges, section tints**
  — the Cache County forum pages, which extend the system for dense response data

## Conventions worth keeping

- **Paper, not white.** White appears nowhere. The lightest surface is `--paper-2`.
- **Two accents, ranked.** Pine carries structure and affirmative action (it is the only
  filled button). Gold is emphasis and is rationed — bullets, active borders, the open state.
  Gold is never a button.
- **Mono does the labeling.** Every eyebrow, tag, count, and unit is DM Mono, uppercase,
  tracked to `.04em`. Body text is never mono.
- **No shadows.** Depth is the `--paper` / `--paper-2` pairing plus a hairline border.
- **The band is punctuation.** Use it once or twice per page to mark a turn. Two dark bands
  back to back read as a mistake.
- **Animation never gates content.** `.reveal` only hides when an inline script has set a
  `js` class on `<html>`. If scripts fail, the content is simply visible.

## Substitutions

Geom is not on Google Fonts under that name; the `@import` requests it and falls back to
Hanken Grotesk, which is close enough that the fallback reads as intentional. If a licensed
Geom becomes available, swap the `--font-display` stack and nothing else changes.
