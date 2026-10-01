# T-010: Send through Gmail and the weekly run command

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "let's do all sources we have at the moment. I have to show value from the very beginning.
> Let's create the necessary tasks-"

## Repo context
- [T-003](T-003-digest-architecture.md): delivery uses Gmail SMTP with an app password (which
  needs 2-step verification) to the single recipient set in `.env`. Sending writes `digests`
  and `digest_items`, which are the only record of what was shared. The weekly run on Monday
  morning is: collect → extract → review → build → send.
- Depends on [T-009](T-009-digest-builder.md) (rendering) and on the user's Gmail app password.

## Open questions
- Which address receives the digest, and has the app password been created?
- Can `run_week` launch extraction itself through Claude Code's non-interactive mode
  (`claude -p "/extract"`), or should it stop and ask the user to run `/extract`? To be
  checked when building it.

## Proposed approach
1. `.env` gets `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `DIGEST_RECIPIENT`. The Django
   mail settings use Gmail SMTP over TLS.
2. `send_digest`: builds the issue (T-009), sends the HTML and text versions, and only then
   writes `Digest` and its `DigestItem` rows in one transaction. It refuses to send a second
   issue for the same send time.
3. `run_week`: runs collect and export, then extraction (by itself if non-interactive mode
   works, otherwise it pauses with instructions), import, a pause for review in the admin, a
   preview, and send once confirmed.
4. Tests with Django's in-memory email backend.

## Acceptance criteria
- [ ] A real issue reaches the recipient's inbox
- [ ] `digests` and `digest_items` are written only after a successful send
- [ ] The same issue can't be sent twice
- [ ] `run_week` guides the whole Monday routine
- [ ] Tests pass

## Implementation
