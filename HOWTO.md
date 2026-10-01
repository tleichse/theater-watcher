# How to run the weekly digest

Step-by-step routine for whoever runs theater-watcher. All commands run from the repo root.

<!-- Format: numbered steps grouped by when they happen (one-time, mid-week, Monday). Each step
says what to run or click and what you should see. This file only describes *how to operate*
the current version: why things work this way lives in the linked task files. When a command
or screen changes, update the step in the same change. -->

## One-time setup

1. Install [uv](https://docs.astral.sh/uv/), then run:
   ```sh
   uv sync
   cp .env.example .env              # set DJANGO_SECRET_KEY to a long random string
   uv run python manage.py migrate
   uv run python manage.py sync_sources
   ```
   `sync_sources` should report `16 sources synced.`. Run it again whenever
   `collection/sources.py` changes.
2. Create your admin login. It asks for a password, so run it yourself:
   ```sh
   uv run python manage.py createsuperuser
   ```
3. Connect Gmail for sending:
   1. In your Google Account, turn on **2-Step Verification** (Security).
   2. Go to **Security › App passwords**, create one called "theater-watcher", and copy the
      16-character password.
   3. In `.env`, fill in:
      ```
      GMAIL_ADDRESS=you@gmail.com
      GMAIL_APP_PASSWORD=the16characterpassword
      DIGEST_RECIPIENT=where-the-digest-goes@example.com
      ```
      `.env` is git-ignored. Never commit it, and never paste the password into a chat.
   4. Check the connection by sending yourself the current issue as a test (nothing gets
      recorded):
      ```sh
      uv run python manage.py send_digest --test
      ```
      It should print `Sent "[TESTE] theater-watcher #…"`, and the email should arrive.

## Mid-week (e.g. Thursday): collect only

```sh
uv run python manage.py collect
```
Each source prints `N new, M updated`. A line in red means that source failed this time. The
rest still ran, so there's nothing to fix unless the same source keeps failing. Why twice a
week: Coffeepaste only shows about the last 5 days of posts
([GOTCHAS.md](GOTCHAS.md#coffeepaste-only-shows-its-newest-20-classifieds-to-a-plain-http-client)).

## Monday morning

### 1. Collect
```sh
uv run python manage.py collect
```

### 2. Extract (in Claude Code)
Open Claude Code in this repo and type:
```
/extract
```
It works through the new listings in batches and ends with a report: how many actions were
created, how many listings were skipped, and the main skip reasons. Everything it creates
lands as **"Por rever"**. Nothing reaches the email without your approval.

### 3. Review and approve (Django admin)
1. Start the admin:
   ```sh
   uv run python manage.py runserver
   ```
   Open <http://localhost:8000/admin/> and log in.
2. Go to **Catálogo › Ações**. In the right-hand filters, pick **Estado: Por rever**.
3. For each action, open it and check:
   - **Título** and **Resumo**: correct, in European Portuguese, and in our own words.
   - **Organização**: who posted it. **It's required for approval.** If it's empty, find out
     from the original page ("Ligação original") and pick or add the organisation, or reject
     the action. The **Quem publica: Sem quem publica** filter lists every action still
     missing one.
   - **Região**, **Pilar**, **Tipo**, and the dates (**Prazo**, **Início**).
   - The **Ligação original** opens the right page.
   To change when an action stops appearing, set **Expira em (manual)**.
4. Back on the list, tick the actions you want and choose **Aprovar as ações selecionadas**
   (or **Rejeitar as ações selecionadas**) from the action menu, then **Ir**. If you see a
   warning that some weren't approved, those have no organisation (see above).
5. Optional: the **Falha a próxima edição: Sim** filter lists actions that close too soon to
   appear in Monday's issue (less than 24 hours after sending). Approving them does no harm,
   but they won't show.
6. Optional: **Recolha › Anúncios recolhidos** shows every collected listing, with its
   **Motivo de exclusão** when `/extract` skipped it. Use it to check that nothing good was
   dropped.

### 4. Build and preview the issue
```sh
uv run python manage.py build_digest
```
It prints the subject (e.g. `theater-watcher #1 · 8 novas, 2 a fechar`) and two files:
- `data/digests/issue-<N>-<date>.html`: open it in your browser to see the email.
- `data/digests/issue-<N>-<date>.txt`: the plain-text version.

If it says `0 items`, nothing has been approved yet (go back to step 3). If something looks
wrong, fix the action in the admin and run `build_digest` again. It only writes files, so
you can repeat it as often as you like.

### 5. Send
Optional: send yourself a test copy first, to see it in your inbox. Nothing gets recorded:
```sh
uv run python manage.py send_digest --test
```
When you're happy with it, send the real issue:
```sh
uv run python manage.py send_digest
```
It prints `Sent "theater-watcher #N · …" to <recipient>` and `Recorded as issue #N`. Recording
is what makes next week's **Novo** badges correct. An issue can only be sent once. Running it
again says `already sent`.

The "current issue" is this Monday's 09:00 slot, until Tuesday morning. If you build or send
later in the week, it's the next Monday's issue. To send a specific one, add
`--at 2026-10-05T09:00`.

## When something goes wrong

| Symptom | What to do |
|---|---|
| `collect` shows a source in red every week | The site probably changed. Note it in [IDEAS.md](IDEAS.md) so it becomes a task. |
| `/extract` reports import errors | It fixes and re-imports them itself. If errors remain, they're listed with the listing id. Ask Claude Code to fix those entries. |
| An action can't be approved | It has no **Organização** (see step 3). |
| `build_digest` shows `0 items`, or `send_digest` says "Nothing to send" | Nothing is approved, or every approved action closes within 24 hours of the send time. |
| `send_digest` says "Set GMAIL_ADDRESS…" | Fill in the three Gmail lines in `.env` (one-time setup, step 3). |
| `send_digest` fails with `SMTPAuthenticationError` | The app password is wrong or was revoked. Create a new one (one-time setup, step 3). Nothing was recorded, so just run it again. |
| `send_digest` warns the HTML is over 100 KB | Gmail will show "Mensagem cortada" with a link to the rest. Fine occasionally. If it happens every week, tell Claude so the template gets lighter. |
