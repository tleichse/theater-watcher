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
  **Partly answered (2026-10-01):** the user will put both in `.env` themselves (HOWTO.md,
  one-time setup step 3). They were deliberately not shared in chat.
- ~~If the digest must be sent from the work network (which blocks SMTP), should delivery
  switch to the Gmail API over HTTPS? That needs a one-time Google Cloud OAuth setup.~~
  **Answer (2026-10-01):** yes, the Gmail API **replaces** SMTP. It costs nothing at this
  volume (standard use is free, and one email a week is far below quota). The `gmail.send`
  scope is "sensitive", so while the OAuth app is in "Testing" Google expires its refresh
  token after 7 days. The plan is to publish the app to "In production" without verification
  (personal use, under 100 users), and to fall back to a weekly re-authorisation if that
  doesn't stop the expiry. Checked from the work network: `oauth2.googleapis.com`,
  `gmail.googleapis.com`, and `accounts.google.com` are reachable with valid TLS.
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
- [x] `digests` and `digest_items` are written only after a successful send
- [x] The same issue can't be sent twice
- [ ] `run_week` guides the whole Monday routine
- [ ] Tests pass

## Implementation
**2026-10-01, sending:** built `send_digest` (`digest/send.py`). `run_week` isn't built yet, so
this task stays in progress.
- **Gmail settings** come from `.env` (`GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`,
  `DIGEST_RECIPIENT`) into Django 6.1's `MAILERS` setting (see the gotcha). Without
  `GMAIL_ADDRESS`, the mailer prints to the console and `send_digest` refuses to run, so an
  issue is never *recorded* as sent when it wasn't.
- **Order:** select, render, send the HTML and text versions, then write `Digest` and its
  `DigestItem` rows (section, position, `was_new`) in one transaction. If the send fails,
  nothing is recorded. If recording failed after a successful send, the email would be out but
  unrecorded. That's accepted as very unlikely with SQLite on the same machine.
- **Twice-sending** is blocked twice: `send_issue` checks for the slot, and
  `Digest.scheduled_for` is now unique.
- **`--test`** sends the real issue with a "[TESTE]" subject and records nothing. It checks
  the connection, and lets the user see the design in a real inbox (useful for
  [T-011](T-011-email-design-brief.md)).
- **Which issue:** both `build_digest` and `send_digest` default to `current_issue_at()`, which
  is the Monday 09:00 slot until a day after it, then the next one. Before this,
  `build_digest` used `next_send_at()`, so building at 09:30 on a Monday would have previewed
  the *following* week.
- A warning is printed when the HTML goes over 100 KB, Gmail's clipping limit. The first issue
  is 29.5 KB for 10 cards.
- Tests: 8 new, 61 in total, all pass. Without Gmail settings, the real command refuses with a
  clear message, as checked on this machine.
- **Still open:** a real send to the user's inbox (needs their app password), and `run_week`.
**2026-10-01, first real send:** failed on the user's work network. Email ports are blocked, or
intercepted by a firewall (see the gotcha "The work network blocks sending email"). The code
and settings weren't at fault: the connection was cut before login. `send_digest` now turns
connection and login failures into a short message saying nothing was recorded, instead of a
traceback. Next step: retry from a network that allows SMTP. If sending must work from the
work network, decide on a delivery path over HTTPS (open question below).
**2026-10-01, Gmail API:** SMTP was replaced by the Gmail API, as decided above.
- `digest/gmail.py` is a Django email backend (`GmailApiBackend`, set in `MAILERS`) that posts
  the full MIME message, base64url-encoded, to `users/me/messages/send` with an
  `AuthorizedSession`. `send_digest` and `send_issue` didn't change, apart from the error
  messages.
- `authorize_gmail` runs the one-time browser login (`InstalledAppFlow.run_local_server`)
  with the OAuth "Desktop app" client in `data/gmail-client.json`, and saves
  `data/gmail-token.json`. Both are git-ignored through `data/*`. The backend refreshes the
  token itself. If the refresh fails, it raises `GmailAuthRequired`, which `send_digest`
  turns into "run authorize_gmail".
- `GMAIL_APP_PASSWORD` is gone from `.env`. Only `GMAIL_ADDRESS` and `DIGEST_RECIPIENT`
  remain.
- New dependencies: `google-auth` and `google-auth-oauthlib`. No Google API client library
  (one REST call doesn't need it).
- `HOWTO.md` one-time setup step 3 walks through the Google Cloud setup: project, Gmail API,
  auth platform (External), **Publish app** to avoid the 7-day expiry, Desktop client, then
  `authorize_gmail` and a test send.
- Tests: 65, all pass. The backend is tested with a mocked session (checks the URL and the
  encoded MIME content), plus a missing token, a failed refresh, and the "authorise again"
  message. On this machine, `authorize_gmail` without the client file explains where to put
  it.
- **Still open:** the user's Google Cloud setup and the first real send, and `run_week`.
**2026-10-01, blocked:** waiting on the user. (1) Choose how to keep the Gmail authorisation:
publishing the Google app failed because the homepage must be on a domain the user owns
(GOTCHAS.md). The options on the table are **test user** (works now, new login about every 7
days; proposed: `send_digest` reopens the browser login by itself when it has expired) or a
**GitHub Pages** site verified in Search Console. (2) After that, the first real send with
`send_digest --test`. `run_week` isn't started yet.
