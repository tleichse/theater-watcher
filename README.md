# theater-watcher

A weekly email digest of new casting opportunities in Portugal, gathered from validated
sources. It covers five pillars: **Theatre**, **Cinema** (films, series, documentaries),
**TV** (soap operas), **Marketing** (TV and radio ads and sketches) and **Dubbing**.

## Getting started
A Django app that runs locally (see [T-003](tasks/T-003-digest-architecture.md) for why).
Requires [uv](https://docs.astral.sh/uv/); it installs the pinned Python (3.12) itself.

```sh
uv sync
cp .env.example .env        # then set DJANGO_SECRET_KEY
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver   # admin at http://localhost:8000/admin/
```

The full setup and the weekly routine (collect, extract, review, build, send) are in
[`HOWTO.md`](HOWTO.md).

## Code layout
One Django app per pipeline stage. The reasoning is in [T-004](tasks/T-004-project-skeleton.md).

| Where | What's there |
|---|---|
| `config/` | Django project settings and URLs |
| `catalog/` | Sources, organisations, actions, and the review admin |
| `collection/` | Raw listings, one adapter per source, collection and extraction commands |
| `digest/` | Issues and what each one shared, selection rules, email templates, build and send |
| `data/` | Git-ignored: the SQLite database and extraction files |

## Docs map

| Where | What's there |
|---|---|
| [`HOWTO.md`](HOWTO.md) | Step by step: setup and the weekly routine to review and send the digest |
| [`CLAUDE.md`](CLAUDE.md) | How work gets done here, and how the files below fit together |
| [`PRIVACY.md`](PRIVACY.md) | Public privacy policy (pt-PT), linked from the Google consent screen |
| [`GOTCHAS.md`](GOTCHAS.md) | Pitfalls already hit. Check it before touching an area it covers. |
| [`IDEAS.md`](IDEAS.md) | Inbox of raw asks, by date |
| [`TASKS.md`](TASKS.md) | Task index and status |
| [`tasks/`](tasks/) | One file per task, plus `_TEMPLATE.md` |
| [`design/`](design/) | Design briefs (e.g. the [email brief](design/email-brief.md) for Claude Design) and the [logo](design/logo/) |
| [`CHANGELOG.md`](CHANGELOG.md) | What shipped |
