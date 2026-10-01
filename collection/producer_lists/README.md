# Producer lists

Where the producers and casting services in [`../producers.csv`](../producers.csv) come from, and how
to look for new ones. It works like [`../company_lists/`](../company_lists/README.md) for theatre
companies: this folder keeps a copy of each original list and a record of what was skipped. To run
the whole process again, open Claude Code and say: *"Let's look for new producers, following
`collection/producer_lists/README.md`."*

<!-- Format: "How to look for new producers" is the procedure; edit it when a step changes. Below
it, one `##` section per list, keyed by the ID used in the CSV's `lists` column, giving the
publisher, the original URL, the local copy, the date it was read, and what was skipped and why.
A refresh adds a new section with a new ID (e.g. `apit-2027`) and never rewrites an old one; a
later change to an old section is added as a dated note. -->

## `producers.csv` columns
- `name`: the public name, used as the organisation name. It must not repeat a name in any of the
  four organisation CSVs (a test checks).
- `kind`: `producer` (film, TV, advertising or animation production company), `casting` (casting
  company, actors' agency or casting director), `dubbing` (dubbing studio or voice agency), or
  `funder` (a body that funds or runs open calls).
- `region`: `north`, `centre`, `south` or `islands`, from the Film Commission directory or the
  Cineguia profile's town. Blank when no list gives one, or when the directory lists several.
- `website`: the organisation's site. Blank if there's none, or if it no longer loads.
- `collect`: blank to collect the website as a `pr-<slug>` source; `no` to keep it as a contact
  only (robots.txt refuses, the site is broken, a mirror, a news site, or another source already
  collects it).
- `lists`: the IDs of the lists below that include it, separated by `;`.
- `last_active`: the most recent year of activity found: membership of the current APIT list,
  the year the Film Commission profile was last updated, or the latest year on the homepage
  (ignoring © lines).

`sync_sources` (which `collect` runs first) turns every row with a website (and `collect` not `no`)
into a `pr-` source using the `site_watch` adapter, and creates or updates every row as an
`Organisation` with its `kind` and `region`, validated when `last_active` is within the last two
years. It's the same code path as `companies.csv`, `venues.csv` and `schools.csv`.

## How to look for new producers
1. **Re-read the lists.** APIT and GEDIPE are short web pages; the Film Commission directory is
   read through its WordPress API (`/wp-json/wp/v2/entity`), taking entities tagged *Ficção*
   (`produtoras=240`) and *Casting* (`outros-servicos=256`), then opening each profile for its
   website. Wait at least a second between profile requests. Save each list in this folder.
2. **Merge by website domain**, so one company on several lists is one row.
3. **Check each website**: does it load, the latest year on the page, a feed. On the work
   network, `SSLError` and 403 pages are the filter (see [GOTCHAS](../../GOTCHAS.md)), not the
   site. A domain that doesn't resolve, or a 404 on every variant, is gone: keep the row with a
   blank website.
4. **Skip** what isn't a place that casts actors: associations, broadcasters (their sites are too
   big for `site_watch`), distributors, equipment, stunts, locations, individual crew, and
   modelling agencies (out of audience). Skip sites with nothing after 2019 unless the company is
   on the current APIT list. Record each skip below.
5. **Write the rows**, run `uv run python manage.py test`, then `collect` the new `pr-` sources and
   record the yield in the active task file.

## `gedipe`
- **What:** GEDIPE, the collective rights society for film and audiovisual producers. Its members
  and beneficiaries: 65 rows, with websites. The page carries a 2021 footer, so membership isn't
  counted as recent activity.
- **Original:** [gedipe.org/site_gedipe/main/associados](https://www.gedipe.org/site_gedipe/main/associados)
- **Copy:** [`gedipe.json`](gedipe.json). Read on 2026-10-01.

## `apit-2026`
- **What:** APIT, the association of independent TV producers. 55 current members, shown as logos
  linking to each site (a few link to an email address only). Membership counts as activity in
  2026.
- **Original:** [apitv.com/os-nossos-associados](https://www.apitv.com/os-nossos-associados/)
- **Copy:** [`apit-2026.json`](apit-2026.json) (links only; names were taken from each site's
  title). Read on 2026-10-01.

## `pfc-directory`
- **What:** Portugal Film Commission, *Production Guide*: 146 producers tagged *Ficção* and 27
  entries tagged *Casting* (158 after merging overlaps), each with region and website.
- **Original:** [portugalfilmcommission.com/en/entities](https://portugalfilmcommission.com/en/entities/)
- **Copy:** [`pfc-directory.json`](pfc-directory.json). Read on 2026-10-01.

### What came of the three lists (2026-10-01)
223 organisations after merging; **188 rows** in `producers.csv` (179 producers, 8 casting
companies, 1 dubbing studio), **160 with a website**, 121 validated.

Not added:
- **Not a place that casts:** AGICOA (rights body), APIT itself, GDA Cooperativa (Fundação GDA is
  already a source), NOS Lusomundo (distributor), Cinemate (equipment), Mad Stunts, Page
  (locations), Photoguerra (underwater filming), two Warner Bros sites.
- **Broadcasters:** RTP, SIC, TVI. Their sites are too large for `site_watch`, and their fiction
  is made by producers on this list. Plural is already collected (`plural-casting`,
  `plural-news`).
- **Individuals:** Paula Afonso (fixer), Gerardo Fernandes, Cláudia Correia, Sandra Santos.
- **Modelling agencies** (out of audience): Elite Lisbon, Models Factory, Models Lab.
- **Stale sites:** Briskman (2015), Films4You (2006), Livremeio (2007), Até ao Fim do Mundo (2016).
- **Gone:** Methodical Albatross, Popsec Studio, Lusco Fusco Animation; Bang! Bang! has no site.
- **Duplicates:** HOP Filmes = HOP Films; the APIT email-only entries for Duvideo, Endemol, SP
  Filmes and Teresa Guilherme (SP Filmes is SP Televisão); `cdi.com.pt` (an empty page) next to
  CDI's `comunhaodeideias.com`.

Kept with a blank website because the domain no longer resolves or returns 404: Arquipélago Raro
Filmes, Colossal Studios, Em Relevo, Ministério dos Filmes, PRETOS, Unlimited Content, Madstudios,
NBFX, Oficina de Filmes, Ventoencanado, Zulfilmes.

*Note, 2026-10-01 (after the first collect):* eight more websites were blanked, so **152** rows are
now collected. Ukbar (its WordPress shows an error page), Beactive and Hibrid Pictures (the domains
stopped resolving), and Ocidental Filmes (401) couldn't be reached. Coral Europa's robots.txt and
The Makkina's firewall refuse the collector, and those are respected. Vitec is Azores TV's news
site, not calls, and Hiperfocal's blog mirrors Miranda Filmes' post for post. Recheck Ukbar and
Coral on the next refresh: they're among the biggest fiction producers.

**Not looked at yet:** dubbing studios (the [wikidobragens](https://wikidobragens.fandom.com/pt/)
list of about 45 Portuguese studios, plus voice agencies like ZOV), advertising producers outside
the Film Commission directory, and casting directors who work on their own.

*Note, 2026-10-01 (later):* with the new `collect` column, the eight sites blanked after the first
collect got their websites back where the site still exists (Ukbar, Coral, The Makkina, Vitec,
Hiperfocal, Ocidental), with `collect` set to `no`. Beactive and Hibrid stay blank (their domains
don't resolve).

## `cineguia`
- **What:** Cineguia Portugal, a public directory of film, TV and advertising professionals
  resident in Portugal. 374 profiles from 13 categories: *Produtora* (203), *Produtora-Services*
  (67), *Agências* (37), *Festivais de Cinema* (32), *Formador área Audiovisual* (27), *Diretor de
  Casting* (25), *Agentes* (19), *Produtora de animação* (18), *Escola de Teatro* (6), and a few
  TV channels, funders and one dubbing studio. Only the name, categories, town and website were
  kept; the profiles' emails and phone numbers weren't stored.
- **Original:** [cineguiaportugal.pt](https://www.cineguiaportugal.pt/) (`?c=<category>`, profiles
  at `?a=<id>`). robots.txt disallows only admin paths. Read one page a second.
- **Copy:** [`cineguia.json`](cineguia.json). Read on 2026-10-01.
- **Added:** about 130 new producers (79 more were already on the GEDIPE, APIT or Film Commission
  lists and got `cineguia` added to `lists`), 37 casting companies and agencies, 3 funders, 1
  dubbing studio. Festivals went to [`venues.csv`](../venue_lists/README.md) and schools to
  [`schools.csv`](../school_lists/README.md).
- **Skipped:** 30 individuals with no website (mostly casting directors and assistants: a name
  alone isn't a usable contact, and it's personal data); 25 technical trainers (editing, camera,
  sound); 11 modelling agencies (Blu, Central, DXL, Eclipse, Elite, Face, Fashion Studio, Karacter,
  Models Factory, Models Lab, Only Fashion); 2 TV-channel staff; 15 stale sites (Ambar, Basilisco,
  Hit Management, Other Features, PAHD, Pipsqueak, Zoe Films Europe and others; nothing after 2019).

## `manual-dubbing-2026`
Dubbing studios and voice agencies, read on 2026-10-01. The starting point was the
[wikidobragens](https://wikidobragens.fandom.com/pt/) studio category (about 45 studios, many
historic) plus the voice agencies found in T-002 and by search. **23 added**, among them Iyuno, VSI
Lisbon, 112 Studios, Audio In, BlueLab, Buggin Media, DLM International, Estúdios Origami, On Air,
Pim Pam Pum, PSB, Santa Claus, Somnorte, Sound Station, SoundTrap, Via Satélite, ZOV, Addvoices,
Voz-Off, Locutores.com.pt and Voices & Media Solutions. Not added: closed studios (Dialectus 2013,
Xangrilá 2014, Tobis, and Matinha, which is now Iyuno), studios with no site found (Citysom,
Graficine, Quevídeo, Trigital, Videoplano and others), guessed domains that belong to someone else
(a domain for sale, a fruit shop, a Spanish school, a music school, an engineering firm),
Cinemágica (a "coming soon" page), ZOO Digital (no Portuguese operation found), and stale sites:
Estúdios Rangel (2018), VOZ ON (2008), Novaga (2004), Vozes Mágicas (2016).

## `manual-funders-2026`
The main funders and open-call bodies, as contacts: DGArtes, Fundação GDA, Europa Criativa (Desk
Portugal), Culture Moves Europe, Perform Europe and Iberescena have `collect` set to `no` (each is
already a hand-configured source in `sources.py`, or its site can't be read); Fundação Calouste
Gulbenkian and SPA (Sociedade Portuguesa de Autores) are collected. ICA came from Cineguia.
