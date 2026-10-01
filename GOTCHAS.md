# Gotchas

Pitfalls we've already hit, so we don't rediscover them. Check the topic you're about to touch.

<!-- Format: entries are grouped under a `##` heading per topic (area of code or kind of problem),
not by date. Each entry is a `###` heading with a symptom-style title, then what goes wrong
and why, then a **Fix:** line. Where a mistake happened again, add a **Recurred:** line naming
each date and task. Entries are only added or amended, never deleted. If one stops applying,
add **Obsolete since YYYY-MM-DD:** with the reason. -->

## Sources & research

### Search results point to source pages that no longer exist
Search engines kept showing `tndm.pt/pt/audicao/` and `tndm.pt/pt/` after TNDM relaunched its
site, and both now return 404. People Stars' `/castings` page looks active, but its newest call
closed in 2024. A catalogue built only from search results, or from summaries of pages
nobody opened, will list dead or stale sources. Found in
[T-002](tasks/T-002-casting-sources-research.md).
**Fix:** before adding a source to the catalogue, load it directly with `curl`, check the HTTP
status, and check the date of the newest listing.

### A 200 on `/feed/` doesn't mean the site has a feed
Conservatório Vocare returns HTTP 200 for `/feed/`, but the body is its "Página não
encontrada" page. EVOÉ's `/feed/` is a real RSS feed, but it lists comedy shows, not the
courses we wanted. Checking only the status code would have recorded both as usable feeds.
Found while checking training sources in [T-002](tasks/T-002-casting-sources-research.md).
**Fix:** open the feed and confirm it's XML with `<item>`/`<pubDate>` entries of the kind
you want and recent dates.
**Recurred:** 2026-10-01, [T-007](tasks/T-007-collectors.md). Feeds that T-002 recorded as live
turned out dead when the collectors were built: São Luiz's `/feed/` has one post from 2018,
Zapping's casting tag stops in 2018, and the Film Commission's feed is valid XML with zero
items. Check freshness again when building the collector, not just during research.

### Coffeepaste only shows its newest ~20 classifieds to a plain HTTP client
The listing page renders about 20 classifieds (plus about 10 in a Formação block). `?page=2`
is ignored, `sitemap.xml` doesn't include current posts, and the "next page" button calls a
private CMS endpoint (`repeater.bondlayer.com/fetch`) that rejects a hand-built request with
"invalid project or collection". Found while building the collector in
[T-007](tasks/T-007-collectors.md).
**Fix:** read the page's content bundle (`cdn.bndlyr.com/…/_p/content.*.js`), which holds
those items as structured JSON, and collect often enough that no more than about 20 posts
appear between runs (about every 5 days at current volume).

## Extraction

### A feed's publish date can be years older than the offer
ACT Escola de Actores reuses the same post for each new edition of a workshop, so its RSS
`pubDate` is from 2024 even when the page lists October 2026 dates (or "Datas a anunciar").
Under the 30-day rule ([T-003](tasks/T-003-digest-architecture.md) step 1), an action with no
deadline or event date but an old `published_at` expires on import and never reaches the
digest. Found during the first extraction ([T-008](tasks/T-008-extraction.md)).
**Fix:** take dates from the page text, not the feed. A workshop with no dates at all is
skipped ("dates to be announced") instead of imported with a stale publish date.

## Repository & paths

### Project name is spelled two ways
The GitHub repo and this folder are `theater-watcher` (American spelling), but the local parent
folder is `theatre-watcher` (British spelling). If you type a path from memory, you'll get one of
them wrong. Found while bootstrapping the repo ([T-001](tasks/T-001-bootstrap-doc-system.md)).
**Fix:** use `theater-watcher` everywhere inside the project, in code, docs, and package names.
Copy absolute paths from the environment instead of retyping them.
