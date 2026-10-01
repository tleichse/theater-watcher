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

### Some company sites look dead from the work network but aren't
On the work network, a few theatre company sites (Escola de Mulheres, Teatro das Beiras,
Projecto Ruínas, Astro Fingido) fail with `SSLError: self-signed certificate in certificate
chain` over HTTPS, or with a 403 titled "Access Notification" (`Server: Cato`) over HTTP. That's
the corporate web filter blocking the site by category, not the site being down. WebFetch goes
through the same filter, so it fails too. Earlier site checks in
[T-013](tasks/T-013-producer-and-company-sources.md) treated these as dead and left the
websites blank; the DGArtes directory crawl showed they were live.
**Fix:** check a suspect site with a web search (the result pages show it's indexed and
current) instead of loading it. Keep it in `companies.csv`: those sources fail from the work
network and collect normally from any other. Don't try to get around the filter.
**Recurred:** 2026-10-01, T-013: the full `collect` showed about 25 of these in red, which
looked like breakage. `collect` now recognises the filter (a self-signed certificate, or
`Server: Cato`) and groups those sites in one line at the end.

### Accents come out as "Ã§" and "Ã£" on some sites
JAT (`colectivojat.com`) and A Oficina (`aoficina.pt`) send `Content-Type: text/html` with no
charset, and declare UTF-8 only in a `<meta>` tag. With no charset in the header, `requests`
falls back to ISO-8859-1, so "Formação" was stored as "FormaÃ§Ã£o". Found during the first
`/extract` over the new company sources in
[T-013](tasks/T-013-producer-and-company-sources.md).
**Fix:** `Fetcher.get` decodes as UTF-8 when the header has no charset and the bytes are valid
UTF-8. The four listings already stored were repaired in place, so they weren't queued for
extraction again. To look for this, search for "Ã§" or "Ã£", not a bare "Ã", which is a real
letter ("NÃO").

## Extraction

### A feed's publish date can be years older than the offer
ACT Escola de Actores reuses the same post for each new edition of a workshop, so its RSS
`pubDate` is from 2024 even when the page lists October 2026 dates (or "Datas a anunciar").
Under the 30-day rule ([T-003](tasks/T-003-digest-architecture.md) step 1), an action with no
deadline or event date but an old `published_at` expires on import and never reaches the
digest. Found during the first extraction ([T-008](tasks/T-008-extraction.md)).
**Fix:** take dates from the page text, not the feed. A workshop with no dates at all is
skipped ("dates to be announced") instead of imported with a stale publish date.

## Django

### Django 6.1 configures email with `MAILERS`, not `EMAIL_*`
`startproject` on Django 6.1 generates a `MAILERS` setting. SMTP settings go in its
`OPTIONS` (`host`, `port`, `username`, `password`, `use_tls`), not in the `EMAIL_HOST`,
`EMAIL_HOST_USER`, ... settings that most guides and older code still use. Those are
deprecated and go away in Django 7.0. Found while connecting Gmail in
[T-010](tasks/T-010-send-and-weekly-run.md).
**Fix:** configure `MAILERS['default']` as in `config/settings.py`. In tests Django swaps
every mailer for the in-memory one, so tests never send real email.

## Email delivery

### The work network blocks sending email (SMTP)
On the user's work laptop and network, `send_digest` failed with `SMTPServerDisconnected:
Connection unexpectedly closed: [WinError 10054]` before Gmail even greeted. Probing
`smtp.gmail.com` showed ports 587 and 25 reset immediately, and port 465 answering with a
**self-signed certificate in the chain** (a firewall intercepting the traffic, not Gmail).
HTTPS (443) works, which is why collection and Gmail in the browser are fine. Credentials
were never reached, so this isn't a password problem. Found on the first real send in
[T-010](tasks/T-010-send-and-weekly-run.md).
**Fix:** sending now goes through the Gmail API over HTTPS (`digest/gmail.py`), which this
network allows with valid certificates. If you ever go back to SMTP, use a network that allows
it (home Wi-Fi, a phone hotspot). Don't try to get around the firewall's certificate: that
inspection is the network owner's policy.

### Gmail API logins expire every 7 days while the app is in "Testing"
`gmail.send` is a "sensitive" scope. An OAuth app left in **Testing** with an **External**
audience gets its refresh token revoked after exactly 7 days, so a weekly digest would need a
new browser login almost every week. Found while planning the Gmail API switch in
[T-010](tasks/T-010-send-and-weekly-run.md).
**Fix:** publish the app (Audience › **Publish app**, "In production") without submitting it
for verification. That's fine for personal use, at the cost of a one-time "unverified app"
warning. If it ever expires anyway, `send_digest` says to run `authorize_gmail`.
**Recurred:** 2026-10-01, [T-010](tasks/T-010-send-and-weekly-run.md). Publishing turned out to
be blocked. "In production" needs a homepage and a privacy policy URL on a domain **you've
proven you own**, and `https://github.com/<user>/<repo>` was rejected ("not registered to
you"). Without your own verified site (GitHub Pages verified in Search Console, or a paid
domain), the practical fix is to stay in **Testing**, add your address under **Test users**,
and accept a new login roughly every week.

## Repository & paths

### Project name is spelled two ways
The GitHub repo and this folder are `theater-watcher` (American spelling), but the local parent
folder is `theatre-watcher` (British spelling). If you type a path from memory, you'll get one of
them wrong. Found while bootstrapping the repo ([T-001](tasks/T-001-bootstrap-doc-system.md)).
**Fix:** use `theater-watcher` everywhere inside the project, in code, docs, and package names.
Copy absolute paths from the environment instead of retyping them.
