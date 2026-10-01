# T-014: EU funding and mobility calls as sources

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "Also maybe erasmus funding and opportunities from the euopean union should also be considered.
> Would that be a different kind of list?"

## Repo context
- The `grant` kind already exists (funding, residency, prize, festival open call), and DGArtes's
  "oportunidades" feed (`dgartes`) already relays some EU calls when DGArtes posts them (Perform
  Europe, Culture Moves Europe, its own top-up to Creative Europe).
- Companies and producers are *organisations that might post a call*, so they live in a CSV
  (`companies.csv`, `producers.csv`) and all share the `site_watch` adapter. EU programmes are a
  handful of portals, each with its own feed or page layout, so they belong in `SOURCES` in
  `collection/sources.py`, like DGArtes. **So yes, it's a different kind of list:** a few
  hand-configured sources, not a CSV.
- `/extract` skips "shoots or productions abroad". EU mobility grants pay Portugal-based artists
  to work in another country, so that rule needs an exception for grants.

## Deep dive: which EU sources (checked 2026-10-01)
| Candidate | What it is | How to collect | Verdict |
|---|---|---|---|
| European Commission, Culture and Creativity (`culture.ec.europa.eu/rss.xml`) | Official news, including every Culture Moves Europe and Creative Europe call | RSS, keyword filter on calls | **Add** |
| Perform Europe (`performeurope.eu/feed/`) | Creative Europe touring grants for performing arts | RSS, keyword filter | **Add** |
| On the Move (`on-the-move.org/news`, Performing Arts filter) | The reference digest of artist mobility calls, worldwide | `html_list` on the filtered list, links `/news/<slug>` | **Add**; expect many skips (calls outside Europe or not for actors) |
| Europa Criativa Portugal desk (`europacriativa.eu`) | National Creative Europe desk | Lists load by script; no feed | Skip for now: its calls reach us through the EC feed and DGArtes |
| Iberescena (`iberescena.org`) | Ibero-American performing arts fund; Portugal is a member | Feed is empty | Skip for now; recheck by hand |
| Erasmus+ Youth and European Solidarity Corps (Agência Nacional, SALTO-YOUTH) | Youth exchanges and training for 13–30-year-olds, run by youth associations | — | **Skip**: aimed at young people and youth workers in general, not professional actors (T-002 audience). Erasmus+ for drama schools is institutional, not an open call. |

## Proposed approach
1. Add `ec-culture`, `perform-europe` and `on-the-move` to `SOURCES` (tier B, like DGArtes).
2. In `extract.md`, keep grants that fund Portugal-based artists to work abroad (mobility,
   residencies, touring) in scope, as `grant`, region `national`.
3. Run `collect` on the three sources and `/extract`, and record the yield here.

## Acceptance criteria
- [x] The three sources collect without errors
- [ ] Mobility grants for Portugal-based artists come through as `grant` actions
- [x] Verdicts for the skipped candidates are recorded here

## Implementation
**2026-10-01.** Built as part of the user's goal of an exhaustive database
([T-015](T-015-exhaustive-contacts.md)), which took this ask as a go-ahead.
- `ec-culture` (the EC's culture RSS, filtered to calls, mobility, residencies and funding),
  `perform-europe` (its RSS, filtered to calls) and `on-the-move` (`html_list` on the news page).
  On the Move's robots.txt forbids its discipline filter (`?f[0]=...`), so the link pattern keeps
  only calls whose address mentions Portugal, theatre, performing arts, acting or Culture Moves
  Europe.
- `extract.md` now keeps grants, residencies and touring calls that Portugal-based artists can apply
  for, even though the work happens abroad, as `grant` with region `national`.
- First collect: 3 listings from the EC, 4 from Perform Europe, 2 from On the Move.
- Europa Criativa and Iberescena, skipped as sources, are in `producers.csv` as contacts (kind
  `funder`, `collect` set to `no`). Erasmus+ Youth stays out, for the reason in the deep dive.
