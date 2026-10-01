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
- [ ] One command exports, `/extract` produces drafts, and one command imports them
- [ ] Drafts are pt-PT, carry no copied text or contact details, and name the poster
  whenever the listing does
- [ ] Out-of-scope listings are skipped with a recorded reason
- [ ] The same opportunity found on two sources becomes one action
- [ ] Tests pass

## Implementation
