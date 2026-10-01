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

## Deep dive: where student productions publish castings (2026-10-01)

Each school's site was loaded directly (and, where the work network failed, from outside it
via a web fetch), and checked for any casting, audition, or open-call page.

| School | What its site has | Verdict |
|---|---|---|
| ESTC (Amadora) | "Ofertas Públicas – Cinema" lists **teaching jobs**, not castings. News has no casting items. `robots.txt` blocks only system folders. | **No source.** Its students' castings appear on Coffeepaste (e.g. an ESTC student and alumni film looking for 5 boys aged 13–16, Sep 2025). |
| Universidade Lusófona (cinema department) | `cinemaeartes.ulusofona.pt` returned **503** both from here and from outside. The main site has course pages only. | **No source for now.** Check again later. |
| ESAD Caldas da Rainha | `www.esad.ipleiria.pt` has a certificate mismatch. The real site is `ipleiria.pt/esadcr/`: events (workshops, talks), no casting page. | **No source.** Its master's-thesis films post on enCAST (one was in the first run). |
| ESMAE (Porto) | One "Audições" item, for **choirs** (music). | **No source** |
| Católica Porto, Escola das Artes | "Oportunidades e Emprego" goes to a careers portal (jobs). | **No source** |
| ESCS, ETIC, Restart, UBI | Nothing casting-related on their homepages. | **No source** |

**Finding:** schools don't publish their students' castings on their own sites. The calls
travel through **Coffeepaste** (several student and independent short-film castings found by
search: Porto/Valongo, a master's final project, "Casting curta – perfis") and **enCAST**,
both already collected, and through Facebook and Instagram groups and internal mailing lists,
which are excluded or unreachable. So adding school sites wouldn't add castings. The way to
get more student castings is to reach the people who post them: ask the cinema departments
(ESTC, Lusófona, ESAD, ESMAE, Católica, UBI) to forward their students' calls. That's
opportunity #1 in [GROWTH.md](../GROWTH.md), the submission channel.

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
- [x] Every school on the list checked, with a verdict and the reason
- [x] Sources that pass are in the registry and collect without errors (none passed)
- [ ] The unpaid-student-productions question is answered

## Implementation
**2026-10-01:** checked all ten schools (see the deep dive). None publishes castings on its
site, so no source was added. Student castings already arrive through Coffeepaste and enCAST,
whose reach depends on collecting twice a week (Coffeepaste only shows about 5 days). The
remaining lever is outreach and a submission channel (GROWTH.md #1). Waiting on the user's
answer to the unpaid-productions question before closing.
