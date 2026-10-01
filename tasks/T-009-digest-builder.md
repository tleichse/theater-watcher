# T-009: Digest builder: selection rules and email rendering

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "let's do all sources we have at the moment. I have to show value from the very beginning.
> Let's create the necessary tasks-"

## Repo context
- The selection rules are in [T-003](T-003-digest-architecture.md) step 2: what is eligible,
  new, or closing soon, and how sections are ordered. The email structure and card anatomy
  are in T-003 step 3, plus the region badge ([T-005](T-005-models-and-review-admin.md)) and
  the poster on each card ([T-006](T-006-traceable-poster.md)).
- Rendering is done with `jinja2` directly, then premailer, producing HTML and plain text
  (T-003 step 5). Email rules: tables for layout, fixed colours, fallback fonts.
- `digest/schedule.py` already has the send time and the 24 h eligibility margin.
- The user's design system (from Claude Design) isn't ready yet. "Show value from the very
  beginning" means the placeholder has to look finished: colourful and clean, not bare HTML.

## Proposed approach
1. `digest/selection.py`: given a send time, returns the sections (Últimos dias, the five
   pillars, Formação, Apoios e oportunidades, No radar, Candidaturas permanentes), each with
   its actions and a new-or-not flag, following T-003 step 2.
2. Jinja templates for HTML and text in `digest/email/`, which Django's template loader doesn't
   scan. Dates and labels are in pt-PT ("Fecha em 3 dias", "Candidaturas até 12 out").
3. `build_digest [--at …]`: renders the next issue to `data/digests/` (HTML and `.txt`) and
   prints a summary. It writes nothing to the database. Recording happens on send
   ([T-010](T-010-send-and-weekly-run.md)).
4. Tests for each selection rule. A rendering test checks that every section appears,
   including the empty-section text.

## Acceptance criteria
- [x] The selection follows every T-003 step 2 rule, with a test for each
- [x] The HTML renders correctly in a browser and is email-safe (inlined CSS, table
  layout), and there's a plain-text version
- [x] All five pillar sections always appear, with "Sem novidades esta semana" when one is
  empty
- [x] Everything a reader sees is in pt-PT
- [x] Tests pass

## Implementation
**2026-10-01:** built as planned. The user built a real issue from the first extraction and
found it "pretty good already". Notes:
- `digest/selection.py` follows T-003 step 2 exactly. An action is eligible when it's approved
  and `expires_at` is more than 24 h after the send time, or never expires. Then, in order:
  `always_open` goes to Candidaturas permanentes, signals to No radar, anything closing within
  7 days to Últimos dias (moved, not repeated), training to Formação, grants to Apoios, and
  everything else to its pillar. "Novo" means the action has no `DigestItem` in an earlier
  issue. Within a section, new items come first, then by expiry.
- `digest/render.py` builds the pt-PT strings (dates like "15 out", "Fecha em 3 dias",
  "Candidaturas até …", "Começa a …"), the facts line (place · pay or price · ages), and the
  issue number (last recorded `Digest` + 1). Templates live in `digest/email/`, outside the
  Django template folders, and premailer inlines the CSS.
- `build_digest [--at …]` writes `data/digests/issue-<N>-<date>.html` and `.txt` and
  **records nothing**. Recording is `send_digest`'s job ([T-010](T-010-send-and-weekly-run.md)),
  so a preview can be rebuilt as often as needed.
- Only the five pillar sections always appear (with "Sem novidades esta semana"). Formação,
  Apoios, No radar, and Candidaturas permanentes appear only when they have items.
- **Placeholder visual design:** dark header with a five-colour pillar strip, one colour per
  section, Georgia headings, Arial body, cards with pillar, Novo, and region badges, a
  deadline chip, and a button. All colours are fixed hex values in `COLOURS` in `render.py`
  and the `<style>` block of `issue.html`, which is what the user's design system will replace.
- Tests: 11 new, 53 in total, all pass.
