# BLOOM prototyping repo

Working repo for BLOOM prototypes. Maintainer: Rahmin Sarabi, Co-Executive Director, BLOOM.

Two independent artifacts live here — they share no code, styling, or tooling, so a change to one never affects the other:

1. **Civic Host Cohort recruitment materials** — offering document and landing page for BLOOM's first Civic Host cohort (six regions, launching Fall 2026). Most of this file is about these.
2. **Utah delegate background page** — `utah-decision-map-delegates.html`, prepared for delegates to the Utah Solutions Forum (18–19 September 2026).

Everything below concerns the recruitment materials unless it names the Utah page.

---

## Files

| File | Role |
|---|---|
| `bloom-civic-host-offering.md` | **Source of truth.** Full offering / prospectus. Deep-dive sent to hosts who have leaned in. |
| `bloom-civic-host-invitation-editable.html` | Condensed recruitment landing page. Has a built-in double-click-to-edit toolbar. |
| `bloom-civic-host-invitation.html` | Clean copy of the landing page, editor stripped. **This is the one to publish or send.** Generated from the editable file — don't hand-edit it if you're using `sync-edits.sh`. |
| `edit-server.py` | **Preferred editing path.** Serves the editable page on loopback and adds a "Save to repo" button that writes, regenerates, commits, and pushes in one click. |
| `sync-edits.sh` | Fallback for when you've edited via the download flow: takes the newest `bloom-civic-host-invitation-editable*.html` from `~/Downloads`, regenerates the clean copy, shows a word-diff, commits, pushes. |
| `make-clean.py` | Shared strip logic that derives the clean copy from the editable one. Both of the above call it, so the transform lives in exactly one place. |
| `utah-decision-map-delegates-editable.html` | Separate artifact — delegate background for the Utah Solutions Forum. Its own design system (Archivo / Source Serif 4 / IBM Plex Mono). Edit this one. |
| `utah-decision-map-delegates.html` | Published copy of the Utah page, editor stripped. Derived — regenerated from the editable file on save. |

**Keep the two in sync.** When copy changes in one, check whether it belongs in the other. The markdown is authoritative; the HTML is a condensed, editorialized cut of it — it deliberately omits readiness tiers and full grant mechanics. The HTML *does* include a simplified 4-stop version of the timeline (Commission/Engage/Deliberate/Carry & Federate with rough month ranges) in its own "Time and effort" section right after the deal section — it's framed around workload/pacing per phase (deliberately distinct from "How it works," which covers what each phase does), not a duplicate of the full onboarding→federate phase table in the markdown.

**Editing in the browser.** Opened straight from disk, the editor can only save by downloading a copy — it has no way to write back. Run it through the local server instead and the loop closes:

```
./edit-server.py
```

Open the URL it prints, double-click any text, click **"Save to repo"**. That writes the editable file, regenerates the clean copy, commits, and pushes. No GitHub token anywhere — it uses this machine's existing git credentials and listens only on loopback. `--no-push` commits without pushing; `--port N` if 8765 is taken.

The "Save to repo" button removes itself unless the page is served from localhost, so opening the file directly (or hitting the copy published on Pages) still just offers the two download buttons.

The server lists every editable page at startup; both the invitation and the Utah delegate page are wired up. To make a new page editable: copy the `#editor-style` / `#editor-ui` / `#editor-script` blocks into it and add one line to `PAGES` in `edit-server.py`.

**Utah page caveat.** Its scale, timeline, routes and gaps sections are rendered at load from the `BANDS` / `TL` / `PATHS` / `GAPS` arrays at the bottom of the file. Editing those in the browser would look like it worked and then silently revert on reload, so the editor deliberately skips them — only static prose is double-click editable. On save the four containers are emptied again so the arrays stay the single source. To change that content, edit the arrays directly.

*Fallback:* if you've already edited via the download flow, `./sync-edits.sh` picks the newest `~/Downloads` copy and does the same thing (`-y` skips the prompt; a string argument sets the commit subject). It only handles the invitation page.

Either path regenerates the clean copy from the editable one, so the two can't drift — but that also means **the clean copy is derived output**, and hand-edits to it get overwritten on the next save. Change the editable file, or change both.

---

## What BLOOM is offering

Six regions run one arc, adapted locally. BLOOM enables; the host convenes and carries.

**The spine:** Commission → Engage → Deliberate → Carry → Federate

1. **Commission** — host assembles a cross-partisan steering committee that engages and listens to discern which question to take up and how to frame it — including a political landscape assessment BLOOM helps them conduct — then pre-commits to act on the answer. (This pre-commitment is the load-bearing move; it's what keeps the assembly from being advisory only. The question is discerned through listening, not framed upfront by the committee alone — don't revert to "frames the question" language.)
2. **Engage** — broad public engagement via CivicOS/OpenPoll and community conversations, getting residents into the room (and online) to make sense of the issue together.
3. **Deliberate** — a lottery-selected, demographically representative Civic Assembly works through expert input and trade-offs to a considered judgment.
4. **Carry** — supermajority recommendations advanced with local institutions, city/county officials, school boards, and state representatives where state policy is implicated.
5. **Federate** — findings across all six sites synthesized for leverage at larger scales: state, national, and direct to private and civil society actors.

**The six subtopic lanes** (shared across the cohort so findings can federate):
data centers & AI infrastructure · K–12 education · jobs & workforce · affordability & wealth · surveillance & privacy · public involvement in decision-making *(meta)*

**Matching grants — two cost-shared buckets:** broad public engagement, and the Civic Assembly itself. CivicOS co-design is **provided by BLOOM**, not a bucket the host cost-shares. (This changed mid-draft; don't reintroduce a third bucket.)

**Readiness tiers** (Tier 1 Seeding / Tier 2 Assembling / Tier 3 Ready) determine the on-ramp and pace. Same arc for everyone; bespoke entry point.

**Timeline:** flexible, roughly 5–9 months onboarding to assembly, keyed to readiness tier. Phases can run in parallel; carry is opportunistic. One fixed anchor: a loose shared cohort assembly season so findings land close enough in time to federate.

---

## Facts to get right

- Parent nonprofit is **the Association for Civic Infrastructure**. Formerly "American Public Trust" / APT — **do not use the old name.** (The "Trust" wording caused California SoS filing delays.)
- **Anchor partners:** Central Oregon (COCAP) — oregon.bloomproject.us · Utah (Utah Common Ground / MWEG) — utah.bloomproject.us
- Utah Common Ground coalition includes AEGIX Institute, Braver Angels, the Center for Anticipatory Intelligence at Utah State, Engage Forum, and MWEG.
- **CivicOS / OpenPoll is open source and free to use** — no license or platform fee, host's to keep, adapt, fork, and run. Built on Pol.is with BLOOM additions (OpenPoll, seed statement pipelines, DiverseBJR statement selection).
- Platform capabilities to name: **opinion mapping** (OpenPoll — surfaces existing common ground *and* the still-open questions deliberation can unlock), **live conversation capture** (transcription for in-person and online meetings), **reporting & analysis** (shared legible evidence for coalition and public).
- **Methodological lineage:** the Civic Jury tradition of the **Jefferson Center**, large-scale citizen deliberations of **AmericaSpeaks**, open-source listening technology. Reviewed by leaders in the field including **Audrey Tang**, whose non-domination standard BLOOM adopted. *(Earlier drafts cited James Fishkin / deliberative polling — this was deliberately changed. Don't revert.)*
- **Forum Assembly method** documented in "Designing & Conducting A Forum Assembly: A Practical Guide" (April 2026, work in progress) by Zabrae Valentine and Sandra Pocharski; based on the AmericaSpeaks 21st Century Town Meeting model, piloted as New Hampshire Together 2024.
- **Rahmin's prior work:** Fort Collins Civic Assembly, Engaged California.

---

## Unverified — confirm before publishing

Flagged rather than silently hardened into fact. Do not treat as citable yet.

- [ ] **"~1,000 residents engaged"** in Utah + Oregon pilots — confirm the real figure.
- [ ] **"4 cross-partisan supermajority findings"** — confirm count and phrasing.
- [ ] **"1,000+ deliberations run worldwide"** — sourced from the Utah press release; confirm the underlying citation.
- [ ] **Team titles and roles** — Clara Long (Co-ED), Zabrae Valentine, Humphrey Obuobi, Stuart Lynn. Verify, and add real one-line bios; none were invented.
- [ ] **Catherine Eslinger pull-quote** (MWEG) — real and public, but given about the Utah Solutions Forum specifically. Get her courtesy sign-off before reusing in cohort recruitment.
- [ ] **Audrey Tang framing** — currently "reviewed by leaders in the field including." If involvement was informal, soften to "with input from"; avoid implying formal endorsement.
- [ ] **Apply URL** — `https://bloomproject.us/apply` is a **placeholder in 4 places** in the HTML. Replace with the real form (Typeform / etc.) before sending.
- [ ] **Funders** — currently generic ("mission-aligned funders"). Naming Schmidt Futures / Office of Eric Schmidt is a disclosure decision for Rahmin, deliberately left out.
- [ ] **"501(c)(3) status in process"** — confirm current status before publishing.

---

## Writing conventions

- **Never use the antithetical "X, not Y" / "it's not X, it's Y" construction.** Rahmin dislikes it. State the positive claim directly. This has been scrubbed from both files — don't reintroduce it. (Plain negation describing what BLOOM doesn't do, e.g. "BLOOM does not parachute in, run an event, and leave," is fine.)
- **The civic host is the protagonist**, not BLOOM. Language should give hosts agency: they convene, they carry, they build. Avoid framing that makes them recipients or subjects of a study.
- **"Building," not "demonstrating,"** in the subtitle — hosts are builders, not exhibits. ("Demonstrating" is held in reserve for a possible funder-facing variant, where the evidence register is the right one.)
- **Capacity-building, enable-not-operate.** BLOOM trains, resources, connects, and contributes pro-rata. Hosts own local delivery. Never imply BLOOM runs the assembly.
- **An honest offer names both sides** — keep the reciprocal "what you get / what you commit to" structure.
- Prefer concrete and human over abstract: "residents chosen by lottery" beats "sortition-selected participants." Name real venues, real thresholds.
- Watch for repeated words across paragraph seams (past fixes: reshaping/remaking, future/future).
- Em dashes over double hyphens.

---

## Landing page design

Matches BLOOM's real production visual identity — pulled directly from the live Utah anchor site (utah.bloomproject.us / CivicOS OpenPoll), not a generic invented palette. This was a deliberate correction: the original draft used Fraunces + Public Sans + pine-green/gold, a combination that reads as a generic "AI-generated landing page." Don't revert to that system.

- **Type:** Hanken Grotesk (headlines + body) + DM Mono (buttons, pill badges, small labels — uppercase, letter-spaced). Real site uses a proprietary "Geom" for headlines; Hanken Grotesk is its public fallback and what the real site's body copy already uses.
- **Palette:** cream paper `#FFF8F1`, espresso ink `#432004`, coral accent `#EE503B` (links, small accents), muted forest green `#406B43` (primary CTA buttons, matching the real site's button color). Variable names in the CSS (`--pine`, `--gold`, etc.) are historical — values now point to this palette, not the old pine/gold one.
- **Eyebrow labels** render as small dark pill badges (mono font, uppercase), matching the "OPEN POLL" tag treatment on the real site — not tracked-uppercase plain text.
- **Structure:** hero → why now → the arc (dark signature band, the one bold element) → the toolkit → the lanes → the reciprocal deal → who we are + proof stats + peer pull-quote → the cohort → closing CTA.
- CTA "Express interest" appears in the sticky header, hero, and final section.
- Respects `prefers-reduced-motion`; focus-visible outlines on interactive elements.

---

## Publishing

- Publish or send the **clean copy**, never the editable one — the editor toolbar shouldn't ship.
- For GitHub Pages: rename the clean file `index.html`, then Settings → Pages → source = main branch. Public repo required for free Pages.
- Before making the repo public, read the page as a *public* document — check the funder language and the Eslinger quote.
- A live URL beats emailing an attachment: renders on any device, updatable without re-sending.

---

## Open threads

- Anchor **"Model Map" visual** for the five-verb arc — the highest-leverage asset for helping a prospective host grok the model in under a minute. Ideas explored: a "walk the arc" interactive, the deal as a two-sided balance, a US cohort map with two anchors pinned and four open slots, the lanes as a strip, the readiness ladder as a ramp. Build feedback prompts into the artifact ("where does this arc break for you?") to get per-component signal rather than "looks nice."
- **PDF** of the full offering for attachment.
- **Internal design-spec companion** — budget bands per bucket, staffing load per host, invitation-only vs. public-RFP mechanics. Deliberately kept out of the host-facing document.
- Possible **funder-facing variant** of the landing page (evidence register, "demonstrating," named backing).
