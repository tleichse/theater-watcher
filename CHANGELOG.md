# Changelog

What shipped, newest first.

<!-- Format: one `##` heading per release: `## YYYY-MM-DD` until the project has version numbers, then
`## vX.Y.Z (YYYY-MM-DD)`. Under each release, `###` subsections by kind: Features / Fixes /
Enhancements / Ops. Write one bullet per shipped change, starting with `[area]` and describing
the result a user sees, not internal reasoning. Add the bullet in the same change that flips
the task to `done`. -->

## 2026-10-01

### Docs
- [research] Final source list for the digest: castings (Coffeepaste, enCAST, TNSJ, TNDM,
  São Luiz, Plural), production news (Plural, the Film Commission, TV news), funding
  (DGArtes, Fundação GDA), and training (ACT, Vocare, Coffeepaste). Only sources that name
  who posts are used.

### Features
- [digest] `build_digest` renders the weekly issue as an email-ready HTML page plus a
  plain-text version, in pt-PT: Últimos dias, the five pillars, Formação, Apoios, No radar,
  and Candidaturas permanentes, with Novo, pillar, and region badges and deadline chips.
- [collection] Collected listings become draft opportunities through the `/extract` command in
  Claude Code: pt-PT titles and summaries, the poster, region, dates and pay, with duplicates
  across sources merged and out-of-scope items skipped with a reason.
- [collection] Listings are collected from all 16 sources (castings, TV and film production
  news, funding calls, and training) with one `collect` command. It respects each site's
  robots.txt and crawl delay.
- [backend] Every opportunity in the digest names who posted it: the admin refuses to approve
  an action without one, and a "Sem quem publica" filter lists the ones still missing it.
- [backend] Opportunities can be stored and reviewed in the admin: sources, organisations,
  and actions, each tagged with a region (Norte, Centro, Sul, Ilhas, Nacional), plus filters,
  bulk approve and reject, and a flag for actions that would close before the next issue.

### Ops
- [repo] The project now runs locally: a Django app (one app each for catalogue, collection,
  and digest) with SQLite, settings in `.env`, and the admin in European Portuguese.

## 2026-09-30

### Docs
- [architecture] Defined how the digest works: an "actions" data model with sharing history
  and deadlines; rules for which actions are open, new, or closing soon; the email layout
  (Últimos dias, the five pillars, Formação, Apoios, No radar, permanent calls); and a local,
  zero-cost stack (Django + SQLite, extraction through Claude Code, and sending through Gmail).

### Ops
- [repo] Set up the project's documentation system: README map, working agreement
  (`CLAUDE.md`), pitfalls log, ideas inbox, task index with a per-task template, and this
  changelog.
