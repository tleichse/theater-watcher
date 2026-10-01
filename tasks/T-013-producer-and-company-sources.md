# T-013: TV and film producers and DGArtes-funded companies as sources

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "would it be important to include also sources from the portuguese main tv channels, through
> their corresponding film companies and so on?" (agreed to do "after" the first issue)

Re-prioritised as opportunity #3 in [GROWTH.md](../GROWTH.md) on 2026-10-01 ("start with 1.
from yout recommendation").

## Repo context
- Plural (TVI's producer) is already two sources: an always-open form and production news
  ([T-007](T-007-collectors.md)).
- The DGArtes list of 33 funded theatre structures is in
  [T-002](T-002-casting-sources-research.md) (public-sector deep dive) as the "watch list".
- ICA was switched off because "filmes produzidos" lists finished films
  ([T-008](T-008-extraction.md)). Its "Projetos em Curso" and "Vistos de rodagem" pages are
  candidates for upcoming productions.
- The parked T-002 question about whether VSI Lisbon was the studio the user meant belongs
  here.

## Deep dive: where the funded-company list comes from (2026-10-01)
The user asked how to get the companies "funded by dgartes or other culture mechanisms", keep
a list, and save their websites as sources.

**Official lists used** (DGArtes "Resultados dos Programas de Apoio",
[`/pt/node/484`](https://www.dgartes.gov.pt/pt/node/484)):
- **Apoio Sustentado, Teatro, bienal 2025–2026:** 33 entities. The names come from the notice
  [`/pt/noticia/8177`](https://www.dgartes.gov.pt/pt/noticia/8177), and the regions from the
  decision table `decisaofinal_anexoiv_signed.pdf`. The notice lists *Teatro Animação de
  Setúbal* and the table lists *Teatro do Silêncio*. Neither appears in the other, so both are
  kept.
- **Apoio Sustentado, Teatro, quadrienal 2023–2026:** 55 entities marked "Apoiada" in
  `anexo2_b_ata_8_teatro_quadrienal_decisao_final.pdf`. The PDF truncates long names, so each
  row was mapped to its public name, and checked against the PDF where a name was ambiguous:
  one row is *Teatro do Montemuro* (Associação Cultural Desportiva e Recreativa do Fôjo), not
  ACERT as first guessed.
- Two companies are in both (Jangada, ACTA), so there are **87 companies** in total.

**Where it lives:** `collection/companies.csv` (name, region, programme, website). Regions use
our five values: "Grande Lisboa", the Península de Setúbal, and the Oeste are `centre`, and the
Açores are `islands`.

**Finding websites**, in this order:
1. Domains guessed from the name (`.pt`, `.com`, `.org`, `.net`), plus ones remembered. A site
   is accepted only if the page contains the company's distinctive words, and then every title
   was read by eye. Seven false matches were rejected (a Galician company, a parked domain, a
   forestry association, an Italian hotel, a campsite, a suspended account, and an unrelated
   "Electrico Inc").
2. Web search for the rest (TEP, TEC, Projecto Ruínas, Cendrev, Escola de Mulheres, João
   Garcia Miguel, and others), with each result loaded to check.
3. The **official DGArtes entity directory** (`/pt/vnode/4`, filter Teatro, supported since
   2023). Each entity page lists the company's website and region. It's read once, slowly,
   respecting `Crawl-delay: 10`.

**Directory crawl result (2026-10-01):** 66 entities. It filled 8 of the 31 gaps: ACTA
(`actateatro.pt`), ESTE, Teatromosca (now on Weebly), Penetrarte (the "84" blog), Escola de
Mulheres, Teatro das Beiras, Projecto Ruínas, and Astro Fingido (moved from `.pt` to
`astrofingido.com`, found by search). The last four had been left blank in step 1 because the
work network's web filter blocks them (see [GOTCHAS](../GOTCHAS.md)). A web search confirmed
they're live. This leaves **64 of 87** with a website. Still blank:
- Teatro do Eléctrico: its listed `teatrodoelectrico.pt` no longer resolves, and search finds
  no other site.
- Teatro do Noroeste: the directory lists `tmsm.pt`, the municipal theatre it's resident in.
  That's a venue, not the company's site.
- Cendrev, Loup Solitaire, Filandorra: in the directory, but with no website listed.
- The other 18 (mostly new in the 2025–26 biennial) aren't in the directory yet.

**Search pass on the rest (2026-10-01):** web search found 16 more, so **80 of 87** now have
a website. Six of them are behind the work network's filter and were accepted on the strength of
search results (Loup Solitaire at `lobosolitario.pt`, Urze, Krisálida, Terra Amarela,
Trimagisto, Razões Pessoais). Notable mappings: Addingtroubles is the legal entity behind
**Plataforma285**, Teatreia is **TEatroensaio**, Enlama is **LAMA Teatro**, Leirena's own
`.pt` domain isn't indexed but its WordPress blog is active, and `cendrev.pt` doesn't resolve
from here while `cendrev.com` is current. In step 1, Urze and Hotel Europa had been rejected
because of false matches on guessed domains. Their real sites are `urzeteatro.com` and
`hoteleuropateatro.com`. Seven have only social media: Pracena, albiASTA, Filandorra, Cães do
Mar, One Hundred Stages, and the two above.

The decision PDF puts Teatro do Eléctrico in Algarve, while the directory says Lisbon (it's
based in Amadora). The CSV keeps the PDF's value.

**How they're collected:** each company with a website becomes a source (`co-<slug>`, tier
A) built from the CSV, with the new `site_watch` adapter. It reads the RSS feed if the homepage
advertises one (skipping comment feeds), otherwise it follows the homepage's own-domain links.
Both paths use the wide `INSTITUTION_KEYWORDS` filter. `sync_sources` also creates every
company as an `Organisation` with `validated = True` (the flag T-003 designed for "on the
DGArtes list"), and `/extract` is told to use the company's exact name as the organisation for
`co-` sources.

**Other funding mechanisms, not done yet:** the *Rede de Teatros e Cineteatros Portugueses*
2026–2029 decision (about 80 credentialled venues), the DGArtes *Programa de Apoio a
Projetos* winners (one-off projects, many by individuals), Fundação GDA's supported shows,
and municipal programmes (Lisboa, Porto). Also: the **quadrennial cycle ends in 2026**.
DGArtes published the 2027–2030 renewal list (`lista_entidades_sustentados_renovacao_30out25.pdf`),
and the CSV should be refreshed from it in January 2027.

**Beyond the funded list (asked 2026-10-01: companies "from all around the country"):** no
single current national register exists. These are the lists found:
- **Centro de Dramaturgia, Universidade de Coimbra:** "Companhias profissionais de teatro em
  Portugal (1974-)", a PDF with 93 companies (88 marked active), each with city, years and
  website. Roughly 60 aren't in `companies.csv`. It was last updated around 2015, so many of its
  links are stale and some companies have closed. It's 26 Lisboa, 22 Porto, and the rest spread
  across the country.
- **DGArtes entity directory** without the year filter: about 70 theatre entities, almost all
  already covered. There's no gain from it.
- **ARTHE (ceteatro.pt):** 20 historic decentralisation companies with current links. They're
  a subset of the above.
- **UNIMA Portugal:** a 2019 list of puppet theatre companies and projects.
- **Performart members:** an employers' association. It mixes venues, festivals and companies.
- **Wikipedia's "Companhias de teatro de Portugal" category.** It includes historic companies.
- Not yet looked at: the DGArtes *Apoio a Projetos* results. They're annual PDFs of one-off
  grants, which bring in the smaller and newer companies that are most likely to hold open
  calls.

## Deep dive: making discovery part of the weekly run (asked 2026-10-01)
The user asked how to make this crawl part of `/collect-extract`, so the run covers "all the
important sources covering producers, theater companies, national theatres, and other players".

**What changes and how often.** The lists of *who might post* (DGArtes decisions, APIT, GEDIPE,
the Film Commission directory) change a few times a year. The *posts* change every week. Re-reading
every registry and every profile each Monday is slow and mostly finds nothing. Also, deciding
whether a new name belongs takes judgement (is it a modelling agency? an individual? is the site
stale?), so it can't be a purely mechanical step.

**Options:**
1. *Weekly full re-crawl inside `collect`.* Always current, but it adds minutes to every run, and
   rows would change in tracked CSVs without anyone looking.
2. *A `discover` step that diffs, plus Claude curating the diff (recommended).* A `discover`
   command re-reads the machine-readable registries (APIT and GEDIPE pages, the Film Commission
   API, the DGArtes entity directory) and writes only what's **new or gone** compared with the
   two CSVs to `data/discover/candidates.json`. It opens profile pages only for new entities.
   `/collect-extract` gets a step 0: run `discover` at most once a month (skipped if the last run
   was under 30 days ago). If there are candidates, Claude applies the lists READMEs' rules (check
   the site, check freshness, skip categories), adds the rows that pass and the skip reasons, and
   reports them so the user can review the diff before committing. Then it collects as usual, so
   new sources are collected in the same run.
3. *Discovery from the posts themselves.* `/extract` already names the poster of every call. An
   organisation that posts on Coffeepaste or enCAST but isn't in either CSV is exactly the kind of
   player no registry lists (small producers, independent casting directors). `discover` can list
   these too (organisations on actions that aren't in a CSV and have no source), as candidates
   for a site check. This works alongside option 2.

**Coverage beyond producers and companies.** National theatres (TNSJ, TNDM, São Luiz) are
hand-written in `sources.py`, because each one needs its own news-page config. The natural next
registry is the *Rede de Teatros e Cineteatros Portugueses* (about 80 credentialled venues), which
would fit a third CSV (`venues.csv`) on the same code path. Film schools are T-012, EU funding is
[T-014](T-014-eu-funding-sources.md), and dubbing studios are listed as not yet looked at in
[`producer_lists/README.md`](../collection/producer_lists/README.md).

**Recommendation:** options 2 and 3 together, monthly. Waiting for the user's go-ahead.

## Proposed approach
1. TV producers: SP Televisão (SIC), RTP's main independent producers (Coral Europa, Ukbar,
   Stopline, Hop!, and others found during the check), and Plural's sister companies. For each,
   check for a casting or contact page, news or a feed, freshness, and `robots.txt`.
2. ICA "Projetos em Curso" and "Vistos de rodagem".
3. The DGArtes-funded companies: list their sites and check which post auditions.
4. Add the sources that pass to the registry, and run a real collect.

## Acceptance criteria
- [ ] Each producer and ICA page checked, with a verdict (producers done 2026-10-01; ICA pages not yet)
- [ ] The DGArtes-funded company list checked, with a verdict per site
- [ ] Sources that pass are in the registry and collect without errors

## Implementation
**Funded companies (2026-10-01).** `collection/companies.csv` holds the companies, one row each.
Each row with a website becomes a `co-` source through the `site_watch` adapter, and
`sync_sources` creates an `Organisation` for every row. 80 of the 87 funded companies have a
website. The deep dive above records how they were found.

**Unfunded companies from the Coimbra list (2026-10-01).** The user clarified that "actors"
means *actors' own collectives*, wanted companies from all over the country, and asked to keep
the source lists so the company list can be checked and updated later. What changed:
- 22 companies from the Coimbra list were added (Teatro do Frio, Ensemble, Comédias do Minho,
  Companhia Maior, Arena Ensemble, NAPALM, and others). Teatro do Noroeste got its page on the
  municipal theatre's site (`tmsm.pt/teatrodonoroestecdv/`), which is the company's own page and
  not the venue's programme. That makes **109 companies, 103 of them collected**. The skip
  record (closed, Facebook only, stale) is in the lists README.
- The CSV gained a `lists` column naming which source lists include each company. `programme`
  is blank for unfunded companies, and `sync_sources` now marks an organisation **validated
  only when `programme` is set**, so "validated" still means "on a DGArtes list", as T-003
  designed it. Before this change every row was validated.
- The original documents are now saved in `collection/company_lists/`: both DGArtes PDFs, the
  Coimbra PDF, and the directory crawl. Its README describes each list and what was skipped.
  The refresh steps are in `HOWTO.md` ("refresh the company list").
- First collect: Dois Pontos 14 and EclipseArte 19 (mostly old blog posts, which `/extract`
  drops), Inestética 4, NAPALM 3, Oficina 3, Teatro do Noroeste 3. Five sites fail only because
  of the work network's filter (Assédio, Companhia da Esquina, Ensemble, ENTREtanto, Teatro do
  Elefante; see GOTCHAS).
- Not done yet for actors' collectives: the DGArtes *Apoio a Projetos* results, which list the
  small one-off groups that the Coimbra list (last updated around 2015) misses.

**Project-grant companies and the new "validated" rule (2026-10-01).** The user asked for the
DGArtes *Apoio a Projetos* lists, and said that every company found with activity in the last
two years counts as validated. What changed:
- Three decisions were read and saved: Criação e Edição 2025, Criação 2026, and Procedimento
  Simplificado 2026. **84 organisations were added**; 33 have a website and are collected. That
  makes 193 companies and 136 collected sources. Individuals were left out, because the user
  wants collectives.
- `companies.csv` gained `last_active` (the year of the latest activity found: a funding
  decision or dated content). `sync_sources` now validates an organisation when that year is
  within the last two years (`ACTIVE_YEARS` in `collection/collect.py`). This replaces the
  earlier "has a `programme`" rule, and funded companies still qualify through their funding
  year. 190 of the 193 are validated. The exceptions are Cassefaz (2023), ENTREtanto and Teatro
  do Elefante (no dated activity found).
- Parsing note: the 2026 PDF writes "Não Apoiada" with a capital A. A case-sensitive filter let
  158 rejected rows through, which showed up as a mismatch with the announced count. The README's
  procedure now says to check the count every time.
- The full repeatable procedure is in `collection/company_lists/README.md`, as the user asked.
  HOWTO points to it.
- First collect: Má-Criação 4, Fogo Lento 1, Ondamarela 1. 14 sites fail only because of the work
  filter. **OUTRO fails for real:** its homepage links to a members-only `/portal` (401), and
  `site_watch` stops the whole source when one followed link fails. That's left open for the
  user to decide.
- *Follow-up, same day:* the user agreed that `site_watch` should skip a followed link that
  returns an HTTP error and carry on with the rest of the site. The homepage failing still fails
  the source. OUTRO now collects (1 new listing).
- *Follow-up, same day:* `collect` now runs `sync_sources` first. Before, a company added to the
  CSV without a manual sync was silently never collected, and "validated" only aged when someone
  synced. The weekly routine was never told to sync; only setup and the lists README mentioned it.
- *Follow-up, same day:* `collect` now groups the sites blocked by the work network's filter
  into one line at the end, instead of listing each in red (`blocked_by_network_filter` in
  `collection/collect.py`). The certificate check stays on, because getting around the filter
  goes against the network owner's policy.
- *Follow-up, same day:* the first `/extract` over the new sources gave 5 draft actions from 109
  listings (most were old blog posts). It also found garbled accents on two sites, so
  `Fetcher.get` now decodes undeclared UTF-8 correctly (see GOTCHAS). The 4 affected listings
  were repaired in place.

**Producers (2026-10-01).** The user asked what happens to "the other contacts" now that theatre
companies have their own CSV, then said to go ahead and "really dig into what other producers may
exist in Portugal", with the CSV going straight into the database. What changed:
- **`collection/producers.csv`**, on the same code path as `companies.csv`. `load_producers()` reads
  it, `company_sources(..., prefix='pr-')` turns each row with a website into a `site_watch`
  source, and `sync_sources` creates or updates every row as an `Organisation`, validated by
  `last_active`. `collect` runs `sync_sources` first, so the CSV reaches the database on every run
  without a separate step. The CSV adds a `kind` column (`producer`, `casting`, `dubbing`) and has
  no `programme`. `/extract` uses the producer's name as the poster for `pr-` sources, as it does
  for `co-`.
- **Three lists, merged by website domain:** GEDIPE's members (65), APIT's current members (55),
  and the Film Commission's directory read through its WordPress API: producers tagged *Ficção*
  (146) and entries tagged *Casting* (27). After merging, 223 organisations; 188 rows were kept.
  The copies, the skip record and the repeatable procedure are in
  [`collection/producer_lists/README.md`](../collection/producer_lists/README.md), which HOWTO now
  points to.
- **First collect over 160 producer sites:** 81 listings from 20 sites. Most producer homepages
  link to no casting or news page, so `site_watch` finds nothing there. That's expected: producers
  mostly cast through casting companies and agencies. Real-looking finds: Hand Creative Chain's
  "Casting" page, Sardinha em Lata's "Candidaturas", Filmesdamente's workshops, a CRIM contest.
  Eight sites were then blanked (see the lists README), which left 152 collected. Their 29
  unextracted listings were marked skipped.
- **Two fixes found by that run:**
  - A dead post in a company or producer feed (SP Entertainment's had a 404) failed the whole
    source. `site_watch` already skipped dead links it follows itself, but not posts reached
    through a discovered feed. It now passes `skip_failed_detail` to the RSS adapter. The
    hand-configured feeds (ACT, DGArtes, GDA) keep failing loudly, as an existing test expects.
  - Removing a website from a CSV left its `Source` active, failing every collect. `sync_sources`
    now deactivates any source that's no longer configured (see GOTCHAS).
- **The SIC verdict from T-002 still holds:** SP Televisão's site has no casting page. Broadcasters
  (RTP, SIC, TVI) weren't added as sources (reason in the lists README).
- The user then asked how to make this discovery part of `/collect-extract`. The options and the
  recommendation are in the deep dive above, pending the user's decision.
- Tests: 3 new (producers file, a dead feed post, deactivating a dropped source), 81 in total, all
  pass.
