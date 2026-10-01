# T-012: Film schools and student productions as sources

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "Find the biggest opportunities for growth for this digest? Is it in terms of sources?
> Keywords? I want ot make this digest the one that everyone goes to." then "write an md with
> these opportunities, and start with 1. from yout recommendation."

Opportunity #2 in [GROWTH.md](../GROWTH.md). Recommendation 1 there covers both #2 (this task)
and #3 ([T-013](T-013-producer-and-company-sources.md)).

## Repo context
- Issue #1 had no Cinema castings ([GROWTH.md](../GROWTH.md), "Where we stand").
- Student shorts already show up indirectly: the first run's enCAST listings included an ESAD
  Caldas da Rainha master's-thesis short film (closed). Coffeepaste carries some too.
- Rules that apply: a source must name who posts each call ([T-006](T-006-traceable-poster.md)),
  `robots.txt` and the link-out policy ([T-002](T-002-casting-sources-research.md)), and no
  Facebook or Instagram scraping (Meta's terms, decided in T-002).
- Adding a source means a `collection/sources.py` entry, usually with an existing adapter
  ([T-007](T-007-collectors.md)).

## Open questions
- Do unpaid student productions belong in the digest? The audience is professional actors
  (T-002), and many student shorts pay expenses only. Proposal: include them, since students'
  films are a real route into cinema, and the card already shows "Não pago" or "Só despesas".

## Proposed approach
1. List the film and acting schools that produce films: ESTC, Universidade Lusófona, ESAD
   Caldas da Rainha, ESMAE, Universidade Católica (Escola das Artes), ESCS, ETIC, Restart,
   UBI, and ESAP.
2. For each one, find where student productions publish casting calls (a news page, a
   dedicated castings page, a platform), and check the page loads, how recent its latest
   call is, `robots.txt`, and whether it has a feed.
3. Record the verdicts in a deep dive here. Add the sources that pass to the registry and run
   a real collect.

## Acceptance criteria
- [ ] Every school on the list checked, with a verdict and the reason
- [ ] Sources that pass are in the registry and collect without errors
- [ ] The unpaid-student-productions question is answered

## Implementation
