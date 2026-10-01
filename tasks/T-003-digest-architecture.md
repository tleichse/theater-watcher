# T-003: Digest architecture: actions data model and email structure

**Origin:** [IDEAS.md, 2026-09-30](../IDEAS.md#2026-09-30). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "before committing, i want to think about the architecture of this dgiest. I think we will
> need a database of so called "actions" that define the entries that I want to share with the
> people that will get the digest. What are the main info that is importatn? One thing that i
> have in mind is that we need to now what opportuinites were already shared, when, when were
> they published and when do they end / until when it is necessary to do something about it
> (for example, an application). As i said, i want to format an email in jinja with an artistic
> and colorful design following a design system (I will create that using claude design), and
> only the actions that are still open will appear in the digest. What is the strucutre you
> recommend for this digest? I want to have the pillars i talked about in separate sections of
> the email. Actions cna also be training possibilities, free or paid. It would be important to
> also gather that info. What do you recommend more? et's think in steaps. ask question for
> validation whenever needed."

## Repo context
- No code or stack yet.
- The source list and the "link-out" legal policy come from
  [T-002](T-002-casting-sources-research.md). The digest carries only facts plus a link to the
  original, never copied descriptions, images, or contact details.
- Language rule (`CLAUDE.md`): anything users see is in pt-PT. Code and the data model are in
  English.
- The user will build the design system with Claude Design, and the email will be rendered with
  Jinja.

## Open questions
Validated step by step with the user. Answers are recorded here in place.

- ~~When an action has already been sent and is still open, what happens to it in the next
  digest?~~ **Answer (2026-09-30):** it repeats every week until it closes. New actions get a
  "Novo" badge and are listed before the older open ones.
- ~~Must a person approve each action before it goes out?~~ **Answer (2026-09-30):** yes.
  Everything collected lands as `pending_review`, and only `approved` actions are eligible.
- ~~Where does training go?~~ **Answer (2026-09-30):** in a separate "Formação" section after
  the pillar sections, with each item tagged by pillar.
- ~~When does an action with no deadline expire?~~ **Answer (2026-09-30):** 30 days after
  publication, and the reviewer can override it per action.
- ~~Does an action in "Últimos dias" also stay in its pillar section?~~ **Answer (2026-09-30):**
  no, it moves. It appears only in "Últimos dias", with its pillar badge.
- ~~How are always-open application forms shown?~~ **Answer (2026-09-30):** as a compact
  "Candidaturas permanentes" list of links near the footer of every issue.
- ~~What does an empty pillar section show?~~ **Answer (2026-09-30):** it shows "Sem novidades
  esta semana". All five pillar sections always appear.
- ~~Do grants, residencies, and funding calls belong in the digest?~~ **Answer (2026-09-30):**
  yes, in their own "Apoios e oportunidades" section, limited to performing arts. This adds
  `grant` to `actions.kind`.
- ~~How do raw listings become structured actions?~~ **Answer (2026-09-30):** LLM-assisted.
  Claude fills in the fields and writes the pt-PT summary, and everything is still reviewed.
- ~~Where does review happen?~~ **Answer (2026-09-30):** in Django admin, which makes Django the
  backend.
- ~~Who manages subscribers?~~ **Answer (2026-09-30):** an EU-based email provider (sign-up,
  double opt-in, unsubscribe, consent records). This removes the `subscribers` table from
  step 1: the list lives in one place, at the provider.
  *Deferred 2026-09-30:* v1 is local with a single recipient (see below), so no email
  provider for now. This answer applies once there are other subscribers.
- ~~Can it run locally at no cost?~~ **Answer (2026-09-30):** yes, and it should. The only
  recipient for now is the user. Everything runs on the user's PC with SQLite, and there are no
  paid services.
- ~~How is extraction done without paying for the API?~~ **Answer (2026-09-30):** a Claude Code
  project command, run at the start of the weekly review, fills in the draft actions. It uses
  the user's existing Claude plan, so it costs nothing extra. (This refines the earlier
  "LLM-assisted" answer.)
- ~~How is the digest delivered?~~ **Answer (2026-09-30):** Gmail SMTP from the user's own
  account, using an app password.
- ~~How are collection and sending triggered?~~ **Answer (2026-09-30):** by hand, with one
  weekly run. Nothing is scheduled.
- ~~Which send day?~~ **Answer (2026-09-30):** Monday morning, Europe/Lisbon.

## Deep dive: steps
1. **Actions data model**: what an action is, its fields, its dates, and its sharing history.
2. **Digest selection rules**: what counts as open, new, or closing soon.
3. **Email structure**: sections, card anatomy, and constraints of rendering email.
4. **Pipeline**: collect → normalise → review → store → render → send.
5. **Stack and hosting.**

## Deep dive: step 1, actions data model (validated 2026-09-30)

| Table | Holds |
|---|---|
| `sources` | Name, URL, trust tier (A/B/C/signal), collection method (rss/sitemap/html), active flag. These are the sources from T-002. |
| `organisations` | Who is casting or offering, plus a `validated` flag (e.g. on the DGArtes funded-company list) |
| `actions` | One opportunity each (fields below) |
| `digests` | One row per issue: number, `sent_at`, subject |
| `digest_items` | `digest_id`, `action_id`, section, position, `was_new`. **The only record of what was shared, and when.** |
| ~~`subscribers`~~ | ~~Email, `consent_at`, `confirmed_at`, `unsubscribed_at`~~. **Removed 2026-09-30:** the email provider owns the list (see step 4). |

Sharing history lives in `digest_items`, not in a flag on the action, because an action
appears in several issues while it stays open (see the "repeats" answer above).

**`actions` fields:**
- **What it is:**
  - `kind`: `casting` | `audition` | `training` | `grant` | `signal` (`grant` added
    2026-09-30 with the "Apoios" answer; it covers grants, residencies, and funding calls)
  - `pillar`: `theatre` | `cinema` | `tv` | `marketing` | `dubbing`
  - `title` and `summary`: pt-PT, written by us, never copied (T-002's link-out policy)
- **Who and where:**
  - `organisation_id`
  - `location` and `remote` (for self-tape or online)
  - `region` *(added 2026-10-01, defined in [T-005](T-005-models-and-review-admin.md))*
  - Profile: `age_min`, `age_max`, `gender`, `languages`
- **Money:**
  - `pay`: `paid` | `unpaid` | `expenses` | `unknown`, plus `fee_text`
  - For training: `price_eur` (0 means free) and `format` (`in_person` | `online`)
- **Dates** (stored in UTC, shown in Europe/Lisbon):
  - `published_at` (nullable)
  - `first_seen_at` (always known)
  - `deadline_at` (nullable; a deadline given as a date only counts until 23:59 Lisbon time)
  - `event_start` and `event_end`
  - `always_open`
  - `expires_at`, calculated: the deadline if there is one, otherwise the event start,
    otherwise `(published_at or first_seen_at) + 30 days`. The reviewer can override it. It's
    the only field the digest checks to decide whether an action is open.
- **Traceability:**
  - `source_id` and `source_url` (the link-out)
  - `fingerprint`: a hash of the normalised title, organisation, and deadline, used to catch
    the same action posted on two sources
  - `last_seen_at`
  - `status`: `pending_review` | `approved` | `rejected` | `expired` | `withdrawn`

## Deep dive: step 2, selection rules (validated 2026-09-30)
For an issue sent at time *T* (the scheduled send time):
- **Eligible:** `status = approved`, `expires_at > T + 24h`, and `kind != signal`. The 24-hour
  margin keeps out anything that closes before a reader could act on it.
- **Signals** only go to "No radar". Actions with `always_open` only go to "Candidaturas
  permanentes".
- **Novo:** the action has no row in `digest_items` from an earlier issue.
- **Últimos dias:** `expires_at ≤ T + 7 days`. These actions are moved here from their own
  section, not duplicated.
- **Order within a section:** new actions first, then older open ones, each group by
  `expires_at` ascending.
- **Known gap:** an action that is found and closes within the same week is never sent.
  The review step flags these so the gap is visible.

## Deep dive: step 3, email structure (validated 2026-09-30)
1. **Header:** issue number, date, and a line such as "Esta semana: N novas, M a fechar".
2. **Últimos dias:** any kind except signals, closing within 7 days
3. **Teatro · Cinema · Televisão · Publicidade · Dobragem:** always all five, with "Sem
   novidades esta semana" when a section is empty
4. **Formação:** training, tagged by pillar, with a free or paid badge
5. **Apoios e oportunidades:** grants and residencies, performing arts only
6. **No radar:** announced productions where castings are likely soon
7. **Candidaturas permanentes:** a compact list of links, not cards
8. **Footer:** unsubscribe, privacy notice, the sources we use and how we choose them

**Card anatomy:** pillar badge, "Novo" badge, title, organisation, a row of key facts
(place · pay · ages), a deadline chip ("Fecha em 3 dias" / "Candidaturas até 12 out"), and a
"Ver e candidatar" button linking to `source_url`. *Amended 2026-10-01:* the key facts
also carry a region badge ([T-005](T-005-models-and-review-admin.md)). The visual design
comes from the user's design system.

**Rendering constraint:** email clients (Outlook especially) don't support CSS variables or
flexbox, handle web fonts unreliably, and change colours in dark mode. The design system needs
an **email version**: fixed colour values, fallback fonts, and table-based layout. Jinja fills
in the content, and premailer inlines the CSS or MJML compiles the layout. Every email also
gets a plain-text version.

## Deep dive: step 4, pipeline (validated 2026-09-30)
1. **Collect (daily):** one adapter per source (RSS, sitemap, or HTML). It respects
   `robots.txt` and its crawl delay, identifies itself with a user-agent string that includes
   a contact URL, and writes to `raw_listings`. Raw text is deleted after about 60 days, since
   we shouldn't keep copies of source text.
2. **Extract:** Claude turns each raw listing into a draft action: fields, a pt-PT summary,
   and a fingerprint for dedup. Only sources that haven't opted out of text and data mining
   are processed (T-002 legal policy, point 6).
3. **Review (Django admin):** approve, reject, edit, merge duplicates, or override
   `expires_at`. Actions that close before the next send are flagged.
4. **Build (weekly):** apply the step 2 rules, render with Jinja (`jinja2` used directly, not
   Django's template engine), inline the CSS, and produce HTML plus plain text. A preview goes
   to the user.
5. **Send:** push the rendered issue to the email provider as a campaign to the subscriber
   list, then write `digests` and `digest_items`.

**Amended 2026-09-30 (v1 runs locally at no cost):**
- **Collection** is weekly and run by hand, not daily. The "known gap" in step 2 gets wider:
  a listing that opens and closes within one week is missed, even if the source was
  collected the week before.
- In **Extract**, "Claude" means Claude Code running a project command, not API calls.
- **Send** goes through Gmail SMTP to the single recipient set in `.env`, not to an email
  provider.

**Amended 2026-10-01:** `collect` runs **twice a week**, by hand: on Monday as part of the
weekly run, and once mid-week (for example on Thursday). Coffeepaste only shows about the
last 5 days of posts ([T-007](T-007-collectors.md)), so a weekly run would miss some. The
mid-week run only collects. Extraction and review still happen once, on Monday.

## Deep dive: step 5, stack and hosting (validated 2026-09-30)
| Concern | v1 choice (local, free) | Later, if other people subscribe |
|---|---|---|
| Runtime | The user's Windows PC. Python, Django, and Django admin at `localhost`. | EU VPS or PaaS |
| Database | SQLite (a single file) | PostgreSQL |
| Extraction | A Claude Code project command. It exports the new `raw_listings`, Claude Code writes the structured drafts, and a command imports them as `pending_review`. | Claude API (Batch) if unattended runs are needed |
| Rendering | `jinja2`, then premailer, producing HTML plus plain text | Same |
| Delivery | Gmail SMTP with an app password (needs 2-step verification), to the recipient in `.env` | An EU email provider (e.g. Brevo) handling subscribers and consent |
| Triggering | One command run by hand on Monday morning | Cron or a scheduler |
| Secrets | `.env`, git-ignored | The host's secret store |

**The weekly run (Monday morning):**
1. `collect`
2. Extract, using the Claude Code command
3. Review in the admin
4. `build_digest`, which sends a preview (the user is the only recipient, so the preview is the
   issue itself)
5. `send_digest`, which records `digests` and `digest_items`

## Proposed approach
1. **Project skeleton:** Django project, SQLite, `.env` handling, `.gitignore`.
2. **Models and admin:** `sources`, `organisations`, `actions`, `raw_listings`, `digests`, and
   `digest_items` (step 1), plus review screens in Django admin: approve/reject actions,
   filters, and a flag for actions that close before the next issue.
3. **Collectors:** one adapter per source on the T-002 final list, starting with the ones
   that have RSS feeds (São Luiz, Plural, DGArtes, Film Commission, TV news), then the HTML
   ones (Coffeepaste, TNSJ, TNDM) and the sitemap one (enCAST).
4. **Extraction:** a Claude Code project command plus export and import management commands.
   The prompt enforces the link-out policy and pt-PT.
5. **Digest builder:** the step 2 selection rules, and Jinja templates following the step 3
   structure. It uses placeholder styling until the user's design system (from Claude Design,
   in an email version) is ready.
6. **Send:** Gmail SMTP, and recording the issue in `digests` and `digest_items`.
7. **`run_week`:** one command that chains all of the above.

Each step is a candidate for its own task.

## Acceptance criteria
- [x] Data model validated
- [x] Selection rules validated
- [x] Email structure validated
- [x] Pipeline validated
- [x] Stack and hosting validated

## Implementation
**2026-09-30:** a design task, so nothing was built. All five steps were validated with the user
in one session. The biggest change from the first draft: the user asked whether v1 could run
locally at no cost. That moved the stack from VPS + PostgreSQL + email provider + Claude API
to PC + SQLite + Gmail SMTP + Claude Code. The data model came out of it smaller, with no
`subscribers` table.
