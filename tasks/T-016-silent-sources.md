# T-016: Make silent sources collect

**Origin:** [IDEAS.md, 2026-10-08](../IDEAS.md#2026-10-08). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> i have a new source to add: it is visoesuteis.pt . can you see if it matters and add it if
> considered relevant?

> there should be interesting thing under the tab /noticias

> I need you to look into other sources that aren't collecting anything and see if there are
> misunderstandings suchs as this one

> maximize the active sources that actually get tangible results / can source content to be
> filtered out and potentially get new items for the newsletter

> optimize the html search to try to guarantee that contents are gathered from the most probable
> pages to have posts for auditions and programmes

> you may use playwright mcp if it helps

## Repo context
- Visões Úteis was already in `companies.csv` (DGArtes quadrienal 2023-2026) as `co-visoes-uteis`,
  collected by `site_watch`, and had never produced a listing. Its homepage linked an open call
  ("Estão abertas as inscrições para o Programa de Associação de Artistas 2027/2028").
- On 2026-10-08, 413 of 588 active sources had never produced a listing: 412 on `site_watch`, plus
  TNDM (`html_list`).
- `site_watch` read a site's feed if it advertised one and stopped there. Otherwise it read the
  homepage's own links and followed those whose anchor text matched `INSTITUTION_KEYWORDS`.
- `collect_source` updates a known listing whose text changed and clears `extracted_at`, so an
  adapter can re-send a page every run and only changes reach extraction.
- `collect` runs sources one after another; the fetcher waits a second between requests to the
  same site.

## Deep dive: why 413 sources were silent
A homepage-only audit (scratch script, not kept) sorted them as follows:

| Group | Sites | Cause |
|---|---|---|
| Feed advertised | 131 | 60 empty feeds, 37 with nothing since before 2025, 28 fresh with no match, 6 dead. The adapter trusted the feed and never read the homepage; 36 of these homepages linked a matching page. |
| Links, none matching | 121 | Quiet, or calls one level down (see the next deep dive) |
| Few or no links | 68 | Built in JavaScript (React, Next, Wix, frames: ~50), redirect stubs (10), WordPress rendered client-side (6) |
| Work-network filter | 57 | See GOTCHAS; collect normally elsewhere |
| Matching link missed | 11 | Only the first anchor of each link was matched; card layouts put an empty image anchor first |
| Keyword only in the address | 10 | e.g. Teatro do Bolhão's `/cursos/curso-profissional-de-interprete` behind "Saber mais" |
| Other errors | 13 | SSL errors (11), a 500, and two companies that moved domain |

## Deep dive: which pages to read
Calls and training programmes rarely sit on the homepage; they sit in a section ("Audições",
"Oportunidades", "Formação", "Notícias") or a post inside it. Options:
- **Crawl deeper** (every own link, two levels): finds most things but multiplies requests per
  site by tens, and `collect` is sequential.
- **Read a few sections** chosen from the homepage links by name: up to 3 extra requests per site.
- **A browser** (Playwright) for JavaScript-built sites: the only way to read the ~50 of them, but
  a heavy new dependency for the unattended weekly run. The Playwright MCP the user offered is an
  interactive tool, so it can't run inside `collect`.

Recommendation: read a few sections now; leave the browser as a follow-up decision.

## Proposed approach
1. Visões Úteis: a dedicated `html_list` source on `/pt/noticias` with no keyword filter, since its
   open calls hide behind titles like "Clube de teatro"; stop the homepage source with a `collect`
   column in `companies.csv` (the other three CSVs already have one).
2. `site_watch` and `html_list`: match every anchor text of a link, not the first.
3. `site_watch`: read the homepage links even when there is a feed; also match the link's path.
4. `site_watch`: pick up to 3 sections from the homepage links (calls, then training, then news),
   add their links to the pool, and re-send call and training sections every run.
5. `site_watch`: follow a same-site homepage that only redirects (meta refresh or
   `window.location`).
6. Data: fix moved domains, mark parked or unrelated sites `collect=no`, and add a WordPress-API
   source for EPTC, whose homepage is built in JavaScript.

## Acceptance criteria
- [x] Visões Úteis's news posts are collected.
- [x] A full `collect` after the change: the number of sources with at least one listing is
  recorded below, before and after.
- [x] Tests cover each adapter change.
- [x] Every collect writes a Markdown report to `data/digests/reports/` (sources visited, reached,
  with new content, pages fetched, by group), flags a partial run, and gains the extraction
  numbers after `/extract`.

## Implementation
2026-10-08, in order:
- **Visões Úteis.** Dedicated `visoes-uteis` source (`html_list` on `/pt/noticias`, no keywords),
  named "Visões Úteis (notícias)" because source names are unique and the old `co-` row keeps
  "Visões Úteis". `companies.csv` gained the `collect` column. The one listing the old source had
  collected was marked skipped as a duplicate. First collect: 10 posts.
- **Anchor texts** (`site_watch`, `html_list`): every anchor of a link is matched, and the longest
  is the fallback title. This alone also picked up a missed TNSJ post.
- **Feed and homepage** are both read; the link's path is matched too (dashes as spaces).
- **Sections:** up to 3, chosen from the homepage links by name and path (at most two path
  segments, no query), in the order calls, training, news. Their links join the pool; call and
  training sections are sent as listings every run, so a changed page is re-extracted. The first
  training pattern included `escola` and `educativ`, which picked schools' about-us pages
  ("Documentos", "Direção"); both were dropped after the first full collect.
- **Redirect stubs:** a homepage under 3,000 characters with a meta refresh or `window.location`
  to the same site is followed once. Links that don't parse (Teatro Villaret's unrendered
  `[acf field=…]` shortcode crashed the whole source) are skipped.
- **Data:** Alfama and Travelling moved domain; Filbox moved to a GoDaddy site; `collect=no` for
  Beactive (500), Jump Willy (empty), Mundo 4K (Vimeo), O2 and Bragacine (parked), and
  Sonomage, Soul Kitchen and Via Satélite (domains for sale). Pim Pam Pum redirects to a baby
  brand's site; left as is pending the user's answer. EPTC got a `wordpress` source on its posts
  API (`eptc`) and its `schools.csv` row is `collect=no`.
- **Not done:** a sitemap fallback for JavaScript-built sites. 30 of the 68 had a sitemap, but
  only 6 listed a matching page, mostly old or off-topic. A headless browser for those ~50 sites
  is left as a decision for the user.
- **Run report** (asked mid-task, see [IDEAS](../IDEAS.md#2026-10-08)): `collect` counts the
  pages each source fetched and writes `data/digests/reports/<date>-<time>-collect.json` and
  `…-report.md`; `run_report` rewrites the report with what extraction made of that run.
  `/collect-extract` runs it at the end.

### Yield
First full collect after the adapter changes (12:37–14:02, 85 min; the backlog of never-reached
pages made it long): 1,091 new listings from 169 sources. Active sources that have ever produced
a listing went from 175 of 588 (30%) to 251 of 583 (43%); 76 previously silent sources produced
something. A spot check of 30 listings: about half are current calls, workshops, residencies or
open applications; the rest are old editions or menu pages that extraction skips. (This first
note also cited SP Televisão's "LUA VERMELHA procura novos talentos" as a find; extraction showed
it is dated 30 May 2025, so it was past.)

### First weekly run with the changes (2026-10-08, `/collect-extract`)
- **Collect** (14:24–15:11, 47 min, no backlog): 580 of 580 active sources visited, 491 reached,
  72 behind the work network's filter, 17 failed; 1,099 pages fetched (2.2 per reached source);
  23 new and 2 changed listings from 8 sources. Re-read sections added almost no churn.
- **Fixes found by that run:** CRIM's robots.txt refuses one sub-page, and the refusal (`Disallowed`)
  failed the whole site; `site_watch` now skips a refused page like a broken one. Malagueta refuses
  its whole site and is `collect=no`.
- **Extraction** of the run plus the backlog from the first collect: 1,115 listings, 23 new actions
  (15 training, 5 grants/residencies, 3 castings/auditions; 21 theatre, 1 cinema, 1 dubbing),
  3 duplicates of known actions, 1,089 skipped. Most of the backlog was old pages (past editions,
  news archives) or school catalogues. Two more noise sources showed up and were fixed:
  - the address match took the whole path, so every page under Jobra's
    `/cursos-profissionais-com-inscricoes-abertas/` matched; it now uses the last segment only;
  - `curso` matched inside "Recursos Humanos" (ESMAE's staff pages); it is now `curso`.
  - Ei! Marionetas is in `venues.csv` twice, under its `.com` and `.pt` sites, so it was collected
    twice; the `.com` row (a mirror) is now `collect=no`.
- **Report:** the extraction part first counted actions created from the backlog as "seen again",
  because their first-seen date is the listing's fetch time. `collect` now records the last action
  id at the start, and the report counts backlog actions on their own line.
