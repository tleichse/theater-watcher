# T-011: Email visual design: brief for Claude Design

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "go on with the task. I just tried the creating the html and it pretty good already. How do you
> suggest apporaching the design question, to get something that i like best?" then "Do the
> brief for the chat with Claude Design, and also build what is needed to do the link with the
> email account."

## Repo context
- The structure of the email (sections, their order, the card anatomy) is fixed by
  [T-003](T-003-digest-architecture.md) step 3, plus the region badge
  ([T-005](T-005-models-and-review-admin.md)) and the poster on every card
  ([T-006](T-006-traceable-poster.md)).
- The current placeholder design is described in [T-009](T-009-digest-builder.md). Its colours
  live in `COLOURS` in `digest/render.py`, and its styles in the `<style>` block of
  `digest/email/issue.html`.
- The approach agreed in conversation: decide name, tone, and references first, explore three
  contrasting directions on real content, refine one, then lock it as a small email design
  system that gets applied to the template.

## Open questions
To answer before (or while) using the brief. They're repeated at the top of the brief:
- Does the name readers see stay "theater-watcher", or does it get a pt-PT name?
- Tone: playful and colourful, editorial and elegant, or bold and poster-like?
- Which 3–5 references (programmes, posters, newsletters) does the user like?

## Proposed approach
1. Write [`design/email-brief.md`](../design/email-brief.md): the product, the fixed
   structure, the email-client constraints, three directions to explore, this week's real
   content as sample copy, and the deliverables expected back.
2. The user runs it in Claude Design and picks a direction.
3. Apply the chosen design: tokens to `COLOURS` and the template's styles, and components to
   `issue.html`. Then test by sending to Gmail (web and phone) and checking dark mode.

## Acceptance criteria
- [x] The brief is ready to paste into Claude Design, with constraints and sample content
- [ ] The user has picked a direction
- [ ] The chosen design is applied to the template and checked in a real inbox

## Implementation
**2026-10-01:** wrote [`design/email-brief.md`](../design/email-brief.md). It opens with the
three decisions to make first (name, tone, references), then covers the audience, the fixed
structure and card anatomy, the email-client constraints, three directions to explore
("Cartaz", "Folha de sala", "Bilhete"), this week's real issue as sample content (plus a
request for one dense section with 6 cards), and the deliverables: mockups in round 1, then
colour tokens with contrast ratios, typography, spacing, and table-based HTML snippets for
each component. Waiting on the user's run in Claude Design.

**2026-10-01, logo:** the user asked for a quick logo. `design/logo/` has `logo.svg` plus
`logo-512.png` and `logo-120.png` (120 x 120 is the size Google asks for). It's an eye (the
"watcher") whose iris is split into the five pillar colours from `COLOURS`, on the header navy
`#1F1A3A`, inside a rounded square. It reads at 120 px. It was rendered once with Pillow (not a
project dependency). The Claude Design round can keep it, refine it, or replace it.
**2026-10-01, blocked:** waiting on the user to fill in "My answers" (name, tone, references)
in `design/email-brief.md`, run it in Claude Design, and pick a direction. Then apply the
design system to `digest/email/issue.html` and `COLOURS`, and check it in a real inbox
(needs T-010's send working).
