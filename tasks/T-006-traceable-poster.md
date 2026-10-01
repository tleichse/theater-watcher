# T-006: Require a traceable poster on every shared action

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "one thing that i really need is that the sources of the action have to be traceable. You
> have to know who is posting."

Followed by: "are we ensuring that?"

## Repo context
- **At the source level, mostly yes.** [T-002](T-002-casting-sources-research.md) keeps only
  tier A sources (the organisation posts its own calls) and tier B sources (a curated board
  where each call names who posted it). The anonymous tier C aggregators are excluded.
- **At the action level, no.** In [T-005](T-005-models-and-review-admin.md),
  `Action.organisation` is nullable, and an action can be approved without one. A Coffeepaste
  or enCAST post whose poster wasn't captured could reach the digest anonymously.
- The email card already shows the organisation (T-003 step 3), so once it's required, readers
  will see who posted.

## Deep dive: what "traceable" means here
An action is traceable when it has (1) **who posted it**: `organisation`, which may also be
an individual such as a casting director or an independent filmmaker, and (2) **where it was
posted**: `source` and `source_url`, which are already required. (2) is already enforced, so
the gap is (1).

Options for enforcing (1):
- **Make `organisation` non-null.** Rejected: extraction will sometimes fail to find the
  poster, and the importer would then have to invent an "Unknown" organisation, which is
  exactly the anonymity we're trying to block.
- **Allow drafts without a poster, but forbid approval without one** (chosen): a database
  `CheckConstraint` (`status != approved` or `organisation` is set), so no code path can get
  around it. Bulk approve skips such actions and reports how many it skipped. The reviewer
  either fills in the poster or rejects the action.

## Proposed approach
1. Add the `CheckConstraint` on `Action`, with a pt-PT error message. Add help text on
   `organisation` saying it's required for approval.
2. Bulk approve only approves actions that have a poster, and tells the reviewer how many it
   skipped.
3. Add a "Sem quem publica" filter to the review list, so these actions are easy to find.
4. Tests: the constraint blocks it at the database, the admin form refuses it, and bulk
   approve skips it.
5. Record in T-002 that "who posted it" is now a hard rule: becasting stays out, and every
   tier C source is excluded for good.

## Acceptance criteria
- [x] An action without a poster can't be saved as approved, whether through the admin form,
  bulk approve, or code
- [x] Bulk approve tells the reviewer what it skipped and why
- [x] The reviewer can filter for actions with no poster
- [x] T-002 records the rule and the becasting decision
- [x] Tests pass

## Implementation
**2026-10-01:** built as planned. The `CheckConstraint` (`approved_action_has_poster`) uses
`condition=`, because Django 6 removed the old `check=` argument. In the admin form, the
constraint's message shows as a form error, so no separate `clean()` is needed. Tests (5 new,
20 in total, all pass): saving directly to the database raises `IntegrityError`, the admin add
form shows the pt-PT error and saves nothing, bulk approve leaves the anonymous action as
`pending_review` and warns the reviewer, and the "Sem quem publica" filter renders.
**For the extraction task:** the prompt has to capture the poster (the person or organisation
named on the listing). Anything without a poster stays a draft until the reviewer adds one
or rejects it.
