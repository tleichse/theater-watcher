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
**Not automated yet.** `send_digest` (Gmail, plus recording what was sent) arrives with
[T-010](tasks/T-010-send-and-weekly-run.md). Until then:
1. Open the `.html` preview in Chrome, press **Ctrl+A** and then **Ctrl+C**.
2. In Gmail, start a new message, paste the content into the body, and use the subject that
   `build_digest` printed.
3. Send it.

Because a hand-sent issue isn't recorded, next week's issue will mark everything still open
as **Novo** again. That gets fixed once `send_digest` exists.

## When something goes wrong

| Symptom | What to do |
|---|---|
| `collect` shows a source in red every week | The site probably changed. Note it in [IDEAS.md](IDEAS.md) so it becomes a task. |
| `/extract` reports import errors | It fixes and re-imports them itself. If errors remain, they're listed with the listing id. Ask Claude Code to fix those entries. |
| An action can't be approved | It has no **Organização** (see step 3). |
| `build_digest` shows `0 items` | Nothing is approved, or every approved action closes within 24 hours of the send time. |
