# T-008: Extraction: raw listings to draft actions via Claude Code

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "let's do all sources we have at the moment. I have to show value from the very beginning.
> Let's create the necessary tasks-"

## Repo context
- [T-003](T-003-digest-architecture.md) step 5: extraction is a Claude Code project command
  run on the user's existing plan. There are no API calls. An export command writes the new
  `raw_listings`, Claude Code writes structured drafts, and an import command loads them as
  `pending_review`.
- Rules the drafts must follow:
  - Link-out policy ([T-002](T-002-casting-sources-research.md)): `title` and `summary` are
    written by us in pt-PT, facts only. No copied text, no images, no contact details.
  - Audience (T-002): professional actors. Extras, modelling, promoter work, children's
    castings, and non-acting jobs are out of scope.
  - Poster is required for approval ([T-006](T-006-traceable-poster.md)).
  - The region values and their boundaries are defined in
    [T-005](T-005-models-and-review-admin.md).
  - A deadline given as a date only counts until 23:59 Lisbon time (T-003).
- Depends on [T-007](T-007-collectors.md) for the input.

## Proposed approach
1. `export_listings`: writes every listing with `extracted_at` unset to
   `data/extract/pending.json` (id, source, url, title, text, fetched date).
2. `.claude/commands/extract.md`: reads that file and writes `data/extract/drafts.json`. Each
   listing produces either one draft (every `Action` field it can find, plus the poster's
   name) or a skip with a reason (out of scope, not an opportunity, already closed).
3. `import_drafts`: validates the file, matches or creates the `Organisation` by name, computes
   `fingerprint` (normalised title, organisation, and deadline), and, when the fingerprint
   already exists, refreshes `last_seen_at` instead of creating a duplicate. Everything new
   lands as `pending_review`, and every listing in the file gets `extracted_at` set.
4. Tests for the import (validation, dedup, organisation matching, a date-only deadline).

## Acceptance criteria
- [x] One command exports, `/extract` produces drafts, and one command imports them
- [x] Drafts are pt-PT, carry no copied text or contact details, and name the poster
  whenever the listing does
- [x] Out-of-scope listings are skipped with a recorded reason
- [x] The same opportunity found on two sources becomes one action
- [x] Tests pass

## Implementation
**2026-10-01:** built, and the first real extraction ran over all 153 collected listings
(Claude Code in this session, following `.claude/commands/extract.md`).
- **What was built:** `collection/extraction.py`, the `export_listings` and `import_drafts`
  commands, and the `/extract` command. The command runs the whole loop itself (export,
  read, write drafts, import, repeat) in batches of 25.
- **Divergences from the plan:**
  - The export also lists the **open actions**, so `/extract` can mark a repeat with
    `duplicate_of` instead of relying only on the fingerprint. Titles are written fresh by the
    model, so the same call on two sites rarely gets an identical title. The fingerprint stays
    as a fallback.
  - One listing can produce **several actions** (a page announcing two workshops).
  - **Skip reasons are stored** on `RawListing.skip_reason` and shown in the admin, so the
    reviewer can see why something was dropped. This was added after the first run, so that
    run's reasons weren't kept.
  - A test caught a bug in `normalise()`: it deleted non-ASCII punctuation instead of turning
    it into a space, so "25–40" and "25-40" got different fingerprints.
- **First run:** 153 listings → **11 actions**, 1 duplicate (the same somatic-practice
  workshop on Fundação GDA and Coffeepaste), 141 skipped. Most skips were archive content seen
  for the first time: MAGG articles from 2022–2025 (17), ICA's list of finished films (35),
  Plural news about productions already filming (10), closed enCAST calls (11), non-acting
  jobs and dance on Coffeepaste, visual-arts calls on DGArtes, and workshops with no dates yet
  on ACT. Later runs only see new items, so the yield should be much higher.
- **ICA was switched off** (`active: False` in `collection/sources.py`, which `sync_sources`
  now applies). Its "filmes produzidos" table lists films already delivered, so no casting
  follows. Better ICA pages ("Projetos em Curso", "Vistos de rodagem") are listed for the TV
  producers check in the inbox.
- **Traceability working as designed:** the enCAST musical-theatre call names only "Associação
  Cultural", so its action has no poster and can't be approved until the reviewer finds one.
- Tests: 8 new, 42 in total, all pass.
