# T-005: Data models and review admin

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "let's go. As for training, some studios as "VS Digital Media" in lisbon are great for
> training. Can we find something there? It would be great if we could categorize the
> opportunities by geography (north, center (including Lisbon), south, or national)"

"Let's go" approved the recommended next step: step 2 of
[T-003](T-003-digest-architecture.md)'s *Proposed approach* (models and admin). The
geography request is new and is handled here. The VS Digital Media lead goes to
[T-002](T-002-casting-sources-research.md).

## Repo context
- The skeleton is in place ([T-004](T-004-project-skeleton.md)): apps `catalog`, `collection`,
  and `digest`, which are still empty.
- The tables and fields are specified in T-003 step 1, and the selection rules in step 2. This
  task builds them and doesn't redesign them.
- Admin is UI the user sees, so labels, choices, and model names are in pt-PT
  (`CLAUDE.md`). Identifiers stay in English.

## Open questions
- ~~Where do the Azores and Madeira go?~~ **Answer (2026-10-01):** in a fifth region, `islands`
  ("Ilhas").
- ~~How does the region show in the email?~~ **Answer (2026-10-01):** as a badge in each card's
  key-facts row. The five pillar sections stay as they are.

## Deep dive: region
`region`: `north` | `centre` | `south` | `islands` | `national`, required on every action.

| Value | pt-PT label | Covers |
|---|---|---|
| `north` | Norte | The Norte NUTS II region (Porto, Braga, Viana, Vila Real, Bragança, …) |
| `centre` | Centro | Centro NUTS II **plus the whole Lisbon metropolitan area**, including the Setúbal peninsula (the user's "center (including Lisbon)") |
| `south` | Sul | Alentejo and Algarve |
| `islands` | Ilhas | Azores and Madeira |
| `national` | Nacional | Nationwide calls, self-tape or online calls with no place to show up, and calls spread over several regions |

Shoots outside Portugal stay out of scope (the reviewer rejects them), so there's no
"abroad" value.

## Deep dive: model details not fixed by T-003
- **`expires_at`** is stored, not computed at query time, so the digest can filter on it. It's
  recalculated in `save()` from the T-003 rule. The reviewer's override is a separate
  `expires_at_override` field, so the rule's result is never lost. An `always_open` action
  with no override has `expires_at = NULL`: it never expires, and it goes only to
  "Candidaturas permanentes" anyway.
- **"Closes before the next issue" flag:** the next issue is the next Monday at 09:00 Lisbon
  time. An approved action misses it if `expires_at ≤ next send + 24h` (the T-003 eligibility
  margin). The send schedule lives in `digest/schedule.py`, because it's a digest rule. The
  catalog admin imports it.
- **`fingerprint`** is just stored here. It's computed by the importer in the extraction task.
- **`organisation`** is nullable, because signals and news-sourced listings don't always name one.
- **`languages`** is a free-text field ("pt, en"). There's no need for a table yet.

## Proposed approach
1. `catalog`: `Source`, `Organisation`, `Action` with `TextChoices` labelled in pt-PT.
2. `collection`: `RawListing` (source, URL, raw title and text, fetched and extracted
   timestamps).
3. `digest`: `Digest` and `DigestItem`, with `schedule.py` for the next send time.
4. Admin: list filters (status, pillar, kind, region, source), search, bulk approve and reject
   actions, and a "misses the next issue" column and filter.
5. Tests for the `expires_at` rule, the next send time, and the flag.

## Acceptance criteria
- [x] All six T-003 tables exist as models with migrations, including `region`
- [x] `expires_at` follows the T-003 rule, and the override wins
- [x] In the admin, a reviewer can filter, bulk approve or reject, and see which actions miss
  the next issue
- [x] Every admin label the user sees is in pt-PT
- [x] Tests pass

## Implementation
**2026-10-01:** built as planned. Notes on what the plan didn't say:
- In `expires_at`, `always_open` is checked after the deadline and before the event start. A
  permanent call that still gives a deadline expires on that deadline.
- `Action.save()` adds `expires_at` to `update_fields` when a caller passes them, so a partial
  save can't leave a stale expiry. The bulk approve and reject admin actions use
  `queryset.update()`, which skips `save()`. That's safe because they change only `status`.
- `first_seen_at` defaults to now, so adding an action by hand in the admin works.
- `RawListing` is unique per `(source, url)`. `DigestItem` is unique per `(digest, action)`.
- The admin index is titled "Revisão", and the apps show as "Catálogo", "Recolha", and
  "Edições". While checking the labels for pt-PT, "cachê" (Brazilian) was replaced with
  "detalhe da remuneração".
- Tests: 15, covering every branch of the `expires_at` rule, the next send time (including the
  October DST change), the margin of the "misses the next issue" check, and the admin list
  rendering with that filter. All pass. Every admin list and add page renders with status 200.
