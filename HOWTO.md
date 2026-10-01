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
   `sync_sources` reports how many sources it synced (about 150: the fixed sources plus every
   theatre company in `collection/companies.csv` that has a website). After this, `collect`
   syncs by itself every time it runs, so edits to `collection/sources.py` or
   `collection/companies.csv` are picked up without running this again.
2. Create your admin login. It asks for a password, so run it yourself:
   ```sh
   uv run python manage.py createsuperuser
   ```
3. Connect Gmail for sending. It goes through the Gmail API over HTTPS, because the work
   network blocks normal email sending ([GOTCHAS.md](GOTCHAS.md#the-work-network-blocks-sending-email-smtp)).
   It's free. This takes 10–15 minutes, once. Google sometimes renames menu items, so look for
   the closest match.
   1. Open <https://console.cloud.google.com/> with the Gmail account that will send the
      digest. Create a **new project** called `theater-watcher`. No billing account is needed.
   2. **APIs & Services › Library**: search for **Gmail API** and click **Enable**.
   3. **Google Auth Platform** (formerly "OAuth consent screen"), then **Get started**:
      - App name `theater-watcher`, and your email as the support address.
      - Audience: **External**.
      - Contact email: yours. Accept the policy, then **Create**.
   4. **Audience**: click **Publish app** and confirm, so the status becomes **In production**.
      This stops Google from expiring your login every 7 days, which it does in "Testing".
      You don't need to submit it for verification: it's only for you.
   5. **Clients › Create client**: Application type **Desktop app**, name `theater-watcher`,
      **Create**. Then **Download JSON** and save the file as `data/gmail-client.json` in this
      repo (git-ignored).
   6. In `.env`, fill in:
      ```
      GMAIL_ADDRESS=you@gmail.com
      DIGEST_RECIPIENTS=you@example.com, friend@example.com
      ```
      `DIGEST_RECIPIENTS` takes one or more addresses separated by commas. Everyone gets the
      email in **Bcc**, so nobody sees the others' addresses. To add or remove a reader, edit
      this line. Only add people who asked to receive it.
   7. Authorise sending:
      ```sh
      uv run python manage.py authorize_gmail
      ```
      A browser window opens. Pick the account. Google warns **"Google hasn't verified this
      app"**: click **Advanced › Go to theater-watcher (unsafe)**. It's safe, because it's your
      own app. Then **Continue** to allow sending email. The terminal prints `Authorised.`
      and saves `data/gmail-token.json` (git-ignored). Never commit it or share it: it lets
      anyone send email as you.
   8. Check everything by sending yourself the current issue as a test (nothing gets recorded):
      ```sh
      uv run python manage.py send_digest --test
      ```
      It should print `Sent "[TESTE] theater-watcher #…"`, and the email should arrive.

## Mid-week (e.g. Thursday): collect only

```sh
uv run python manage.py collect
```
Each source prints `N new, M updated`. A line in red means that source failed this time. The
rest still ran, so there's nothing to fix unless the same source keeps failing. Sites that the
work network's filter blocks aren't listed in red; they're grouped in one line at the end. They
come through when you collect from another network (home Wi-Fi, a phone hotspot). Why twice a
week: Coffeepaste only shows about the last 5 days of posts
([GOTCHAS.md](GOTCHAS.md#coffeepaste-only-shows-its-newest-20-classifieds-to-a-plain-http-client)).

## Monday morning

**Shortcut for steps 1 and 2:** open Claude Code in this repo and type `/collect-extract`. It
runs the collect, reports what came in, then does the whole extraction. Or do the two steps
by hand, as below.

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
It prints `Sent "theater-watcher #N · …" to N reader(s) in Bcc` and `Recorded as issue #N`.
A `--test` send goes only to your own `GMAIL_ADDRESS`, never to the readers. Recording
is what makes next week's **Novo** badges correct. An issue is recorded only once. Running it
again says `already sent`. To send it again anyway, for example after adding readers, use:
```sh
uv run python manage.py send_digest --resend
```
This goes to **everyone** in `DIGEST_RECIPIENTS` again, including people who already got it.
It keeps the same number, and nothing is recorded twice, so next week's **Novo** badges stay
right.

The "current issue" is this Monday's 09:00 slot, until Tuesday morning. If you build or send
later in the week, it's the next Monday's issue. To send a specific one, add
`--at 2026-10-05T09:00`.

## Now and then: look for new companies
The theatre companies that get collected are in `collection/companies.csv`. Where each one came
from, and the full step-by-step process for finding new ones, is in
[`collection/company_lists/README.md`](collection/company_lists/README.md). Run it with Claude Code
(*"Let's look for new theatre companies, following collection/company_lists/README.md"*):
- when DGArtes publishes a decision: the yearly *Apoio a Projetos* results (July to September)
  and the 2027–2030 four-year list (January 2027);
- once a year, to recheck companies whose `last_active` year is about to fall out of the two-year
  "validated" window.

## When something goes wrong

| Symptom | What to do |
|---|---|
| `collect` shows a source in red every week | The site probably changed. Note it in [IDEAS.md](IDEAS.md) so it becomes a task. |
| `/extract` reports import errors | It fixes and re-imports them itself. If errors remain, they're listed with the listing id. Ask Claude Code to fix those entries. |
| An action can't be approved | It has no **Organização** (see step 3). |
| `build_digest` shows `0 items`, or `send_digest` says "Nothing to send" | Nothing is approved, or every approved action closes within 24 hours of the send time. |
| `send_digest` says "Set GMAIL_ADDRESS…" | Fill in the two Gmail lines in `.env` (one-time setup, step 3.6). |
| `authorize_gmail`: browser shows "has not completed the Google verification process… Error 403: access_denied" | The Google Cloud app is still in **Testing**, and your account isn't a test user. In **Google Auth Platform › Audience**, click **Publish app** (status **In production**), then run `authorize_gmail` again. You'll get the "unverified app" screen instead: **Advanced › Go to theater-watcher**. (Alternative: add your address under **Test users**, but then the login expires every 7 days.) |
| `send_digest` says to run `authorize_gmail` | The login expired or was revoked (or never happened on this machine). Run `uv run python manage.py authorize_gmail`, then send again. Nothing was recorded. If this happens every week, the Google Cloud app is still in "Testing" (step 3.4). |
| `send_digest` says "Gmail did not accept the email" | A network or Gmail error. Nothing was recorded, so try again. If it persists, check that <https://gmail.googleapis.com> opens in the browser. |
| `send_digest` warns the HTML is over 100 KB | Gmail will show "Mensagem cortada" with a link to the rest. Fine occasionally. If it happens every week, tell Claude so the template gets lighter. |
