# T-004: Project skeleton and directory layout

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "consider T-003. What are the next steps? Can we just figure rapidly a robust and simple
> directory management strucutre and start with implementation?"

## Repo context
- The design is complete in [T-003](T-003-digest-architecture.md): Django + Django admin,
  SQLite, `jinja2` + premailer for the email, Gmail SMTP, extraction through a Claude Code
  project command, and everything run by hand once a week on the user's Windows PC.
- This is step 1 of T-003's *Proposed approach*. Steps 2–7 (models, collectors, extraction,
  digest builder, send, `run_week`) are each a candidate for their own task.
- No code yet. Machine has `uv` 0.9 and Python 3.12/3.13 available (the default `python` on
  PATH is 3.9, which is too old for current Django).

## Deep dive: directory layout
One Django project with **one app per pipeline stage** from T-003 step 4. Each app owns the
tables that stage writes, so a reader can find code by asking "which stage is this?".

```
theater-watcher/
├── pyproject.toml, uv.lock   # dependencies, managed by uv
├── manage.py
├── .env.example              # copy to .env (git-ignored)
├── config/                   # Django project: settings, urls
├── catalog/                  # sources, organisations, actions + the review admin
├── collection/               # raw_listings, one adapter per source, collect + extract export/import commands
├── digest/                   # digests, digest_items, selection rules, Jinja email templates, build/send commands
├── data/                     # git-ignored: db.sqlite3, extraction export/import files
└── .claude/commands/         # the Claude Code extraction command (added with the extraction task)
```

Options considered:
- **A single app** holding everything: fewer files now, but `models.py` and `admin.py` would
  mix three unrelated concerns, and the admin review screens would sit next to scraping code.
- **One app per table**: too fine-grained. Six apps for six tables, with most of them just a
  model.
- **One app per stage** (chosen): three apps, each with one clear job, and it matches the
  pipeline that T-003 already validated.

Every app keeps the standard `startapp` shape, so they all look the same. Code that belongs to a
stage goes into a module inside that app (for example `collection/adapters/<source>.py`), not a
new top-level folder.

## Proposed approach
1. Pin Python 3.12 with uv, and add Django and `python-dotenv`.
2. `startproject config .`, then `startapp` for `catalog`, `collection`, and `digest`.
3. Settings: secrets and debug come from `.env`, SQLite in `data/`, `TIME_ZONE =
   "Europe/Lisbon"` with `USE_TZ` (UTC stored, Lisbon shown, per T-003), and the admin in
   pt-PT.
4. `.gitignore` and `.env.example`, plus run steps in `README.md`.
5. Verify: `check`, `migrate`, and the admin loads at `localhost`.

## Acceptance criteria
- [x] `uv sync` and `uv run python manage.py migrate` work from a fresh clone
- [x] The three apps exist and are installed
- [x] The admin loads in European Portuguese
- [x] No secrets or database files are tracked by git
- [x] `README.md` has the run steps and the layout map

## Implementation
**2026-10-01:** built as planned. uv pinned Python 3.12 and resolved Django 6.1.1. Settings read
`DJANGO_SECRET_KEY` (required) and `DJANGO_DEBUG` from `.env` via `python-dotenv`, and the
database lives at `data/db.sqlite3`. The admin uses `LANGUAGE_CODE = 'pt'`, which in Django is
European Portuguese (`pt-br` is Brazilian). Its login page was checked: "Utilizador",
"Palavra-passe". The `startapp` defaults (`views.py`, `tests.py`) were left in so the three apps
share the standard shape. `.claude/commands/` isn't created yet; it comes with the extraction
task.
