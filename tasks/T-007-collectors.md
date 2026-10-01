# T-007: Collectors for every source on the final list

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "how do we make a first run now? ist here something missing? Do we have to work on more
> sources?" then "let's do all sources we have at the moment. I have to show value from the
> very beginning. Let's create the necessary tasks-"

The user turned down the thinner first version (two collectors first) that was offered in the
same conversation, so that the first issue already covers every source.

## Repo context
- The source list, with tiers, access notes, and verdicts, is in
  [T-002](T-002-casting-sources-research.md) (verification pass and later deep dives). The
  legal rules are in T-002's link-out policy: respect `robots.txt` and its crawl delay,
  identify ourselves with a user agent that includes a contact URL, fetch at a low rate, and
  prefer RSS or sitemaps.
- [T-003](T-003-digest-architecture.md) step 4 (collect) writes to `raw_listings` and deletes
  raw text after about 60 days. Collection is weekly and run by hand.
- `Source` and `RawListing` exist ([T-005](T-005-models-and-review-admin.md)). `RawListing` is
  unique per `(source, url)`.
- Traceability rule ([T-006](T-006-traceable-poster.md)): only sources that name who posted.

## Sources in scope (from T-002)
| Source | Feeds into | Access method |
|---|---|---|
| Coffeepaste (Audição/Casting, Oportunidade, Formação, Bolsa, Residências, Concurso/Prémio) | castings, training, Apoios | HTML |
| enCAST.pro (Portugal) | castings | sitemap |
| TNSJ | castings | sitemap / news |
| TNDM | castings, internships | HTML `/noticias` |
| Teatro São Luiz | castings | RSS |
| Plural Entertainment | always-open calls | RSS / fixed pages |
| ICA (films produced) | No radar | HTML tables |
| Portugal Film Commission | No radar | RSS |
| atelevisao, Zapping-TV, MAGG | No radar (headline and link only) | RSS |
| DGArtes `oportunidade` | Apoios | RSS (crawl delay 10 s) |
| Fundação GDA | Apoios | RSS |
| ACT Escola de Actores | training | RSS |
| Conservatório Vocare | training | HTML |

Not included: the companies on the DGArtes funded-company watch list (about 33 sites, each
needing its own adapter, which makes it a later task), and Cultura Portugal (optional in
T-002, and it overlaps with DGArtes).

## Open questions
- What contact URL goes in the user agent? Proposal: the GitHub repo
  (`https://github.com/tleichse/theater-watcher`). It's public only if the repo is.

## Proposed approach
1. Source configuration lives in code, as a registry: slug, name, URL, tier, method, the URL
   to read, and filters. A `sync_sources` command upserts the registry into `Source`, so a
   fresh clone gets every source with one command, and the admin can still switch a source
   off with `active`.
2. Shared fetch layer: one HTTP session with our user agent, a `robots.txt` check per
   host, and the crawl delay respected (at least 1 s between requests to the same host).
3. Generic adapters: **RSS** (most sources) and **sitemap** (URL pattern filter, then fetch
   each new page's text). Specific HTML adapters: Coffeepaste, TNDM, ICA, Vocare.
4. `collect` command: runs every active source, stores new listings (skipping
   `(source, url)` pairs already stored), reports counts per source, keeps going if a source
   fails, and deletes raw text older than 60 days.
5. Tests per adapter against saved sample pages, so they don't depend on the network.
6. A real run against every source. Record what each one returned.

## Acceptance criteria
- [ ] Every source in the table is in the registry, and `sync_sources` loads them
- [ ] `collect` fetches every active source and respects `robots.txt` and crawl delays
- [ ] A failing source doesn't stop the run, and the report says which one failed
- [ ] Re-running doesn't duplicate listings
- [ ] Raw text older than 60 days is deleted
- [ ] Adapter tests pass offline
- [ ] A real run returns listings from every source that has current content

## Implementation
