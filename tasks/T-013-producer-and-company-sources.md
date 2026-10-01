# T-013: TV and film producers and DGArtes-funded companies as sources

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "would it be important to include also sources from the portuguese main tv channels, through
> their corresponding film companies and so on?" (agreed to do "after" the first issue)

Re-prioritised as opportunity #3 in [GROWTH.md](../GROWTH.md) on 2026-10-01 ("start with 1.
from yout recommendation").

## Repo context
- Plural (TVI's producer) is already two sources: an always-open form and production news
  ([T-007](T-007-collectors.md)).
- The DGArtes list of 33 funded theatre structures is in
  [T-002](T-002-casting-sources-research.md) (public-sector deep dive) as the "watch list".
- ICA was switched off because "filmes produzidos" lists finished films
  ([T-008](T-008-extraction.md)). Its "Projetos em Curso" and "Vistos de rodagem" pages are
  candidates for upcoming productions.
- The parked T-002 question about whether VSI Lisbon was the studio the user meant belongs
  here.

## Proposed approach
1. TV producers: SP Televisão (SIC), RTP's main independent producers (Coral Europa, Ukbar,
   Stopline, Hop!, and others found during the check), and Plural's sister companies. For each,
   check for a casting or contact page, news or a feed, freshness, and `robots.txt`.
2. ICA "Projetos em Curso" and "Vistos de rodagem".
3. The DGArtes-funded companies: list their sites and check which post auditions.
4. Add the sources that pass to the registry, and run a real collect.

## Acceptance criteria
- [ ] Each producer and ICA page checked, with a verdict
- [ ] The DGArtes-funded company list checked, with a verdict per site
- [ ] Sources that pass are in the registry and collect without errors

## Implementation
