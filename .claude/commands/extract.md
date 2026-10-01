---
description: Turn collected listings into draft actions for review (theater-watcher extraction, T-008)
---

You are extracting casting and training opportunities for **theater-watcher**, a weekly pt-PT
digest for **professional actors in Portugal**. Work in batches until nothing is left.

## Loop
1. Run `uv run python manage.py export_listings`. If it exported 0 listings, stop and report
   the totals.
2. Read `data/extract/pending.json`. It has `today`, the `listings` to process, and the
   `open_actions` already in the database.
3. Write `data/extract/drafts.json` (format below) with **one result per listing** in the batch.
4. Run `uv run python manage.py import_drafts`. If it reports errors, fix only those entries in
   `drafts.json` and run it again. Entries that were already imported are ignored.
5. Go back to step 1.

At the end, report how many actions were created, how many listings were skipped, and the
most common skip reasons.

## Output format
```json
{"results": [
  {"listing_id": 12, "skip_reason": "figuração"},
  {"listing_id": 13, "actions": [{ ...action... }]}
]}
```
A listing gives **zero actions** (then `skip_reason` is required, in English, a few words) or
**one or more** actions (for example, one page that announces two separate workshops).

Action fields (leave out or use `null` when unknown):

| Field | Values |
|---|---|
| `kind` | `casting` (call for performers for a production, including voice work), `audition` (an audition held by a theatre or company for a production or ensemble), `training` (workshop, course, masterclass, internship for performers), `grant` (funding, residency, prize, festival open call for performing-arts work), `signal` (news that a production is starting, with no call yet) |
| `pillar` | `theatre` (including musical theatre and performance), `cinema` (film, short film, documentary, streaming series), `tv` (soap operas and TV series), `marketing` (ads, brand or social-media campaigns, radio spots, institutional videos), `dubbing` (dubbing, voice-over, voice acting, audiobooks) |
| `title` | pt-PT, max 90 characters, **your own words**: who or what is sought, then the project. E.g. "Atores 25–40 anos — curta-metragem em Braga", "Workshop de câmara e casting — ACT" |
| `summary` | pt-PT, 1–2 sentences, **your own words**, facts only: role, dates, place, pay, who it's for. Never copy sentences from the listing. Never include emails, phone numbers, or names of private individuals. |
| `organisation` | **Who is posting or casting** (company, theatre, school, foundation, or the named person if no entity is given). For news signals: the producer or broadcaster. For DGArtes: the third party running the call, not DGArtes. On a company's or producer's own site (`source` starts with `co-` or `pr-`), it's that company, written exactly as `source_name`. Use `null` only when the listing really doesn't say. Never invent one. |
| `location` | Town or city as written ("Lisboa", "Porto", "Online") |
| `region` | **Required.** `north` (Norte: Porto, Braga, Viana do Castelo, Vila Real, Bragança), `centre` (Centro **plus the whole Lisbon metropolitan area**, including Setúbal), `south` (Alentejo, Algarve), `islands` (Azores, Madeira), `national` (nationwide, online or self-tape only, several regions, or "Portugal" with no place) |
| `remote` | `true` for self-tape or online |
| `age_min`, `age_max` | Integers, playing or required age |
| `gender` | `any`, `female`, `male`, `other` |
| `languages` | e.g. "pt-PT, en" |
| `pay` | `paid`, `unpaid`, `expenses`, `unknown` |
| `fee_text` | Short, e.g. "1 300 € por performer" |
| `price_eur` | Training only: number, `0` when free |
| `format` | Training only: `in_person` or `online` |
| `published_at` | `YYYY-MM-DD` if the listing shows it |
| `deadline_at` | Application deadline, `YYYY-MM-DD` (a date means until 23:59 Lisbon), or full ISO if a time is given. Coffeepaste's `Prazo: 2026-10-23T00:00:00.000Z` means the date `2026-10-23`. |
| `event_start`, `event_end` | `YYYY-MM-DD`: shoot, rehearsal, run, or course dates |
| `always_open` | `true` only for permanent sign-up forms with no deadline (e.g. a producer's "send us your CV" page) |
| `duplicate_of` | The `id` of an `open_actions` entry when this is the **same opportunity** (same organisation, same call), e.g. posted on two sites. Then only `duplicate_of` is needed. |

## Skip (zero actions) when
- **Out of audience:** extras or figuração, modelling, promoters, castings for children or
  teenagers only, reality shows or contests for the general public, non-acting jobs
  (technicians, teachers, designers, producers, stage managers, marketing roles).
- **Out of scope:** dance-only, music-only, or visual-arts-only calls, and grants that aren't for
  performing arts or film. Training unrelated to acting or voice (e.g. stop-motion building,
  podcast production).
- **Not in Portugal:** shoots or productions abroad, unless the call explicitly seeks actors
  based in Portugal for remote or self-tape work. Exception: a grant, residency or touring call
  that artists based in Portugal can apply for (e.g. Culture Moves Europe, Perform Europe) is in
  scope as `grant`, region `national`, even though the work happens abroad.
- **Closed or past:** the deadline is before `today`, the event already happened, or the page
  says it's sold out ("esgotado") or closed ("encerrado").
- **Not an opportunity:** gossip, ratings, programme listings, results of past calls, news
  about productions that are already filmed or airing.
- **ICA rows** (`source: ica`) are films already produced. Skip them unless the row clearly
  says the project hasn't been shot yet.
- Test or placeholder posts.

## Rules that always apply
- Facts only, in your own words (the "link-out" policy): the digest links to `url` for
  everything else.
- When unsure whether an opportunity is in scope, **include it**. The reviewer decides. When
  unsure about a field, leave it `null` instead of guessing.
- Write every `title` and `summary` in **European Portuguese** (pt-PT), never Brazilian.
