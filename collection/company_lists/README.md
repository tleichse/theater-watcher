# Company lists

Where the theatre companies in [`../companies.csv`](../companies.csv) come from, and how to look
for new ones. This folder keeps a copy of each original list, so it can be rechecked if the
publisher changes or removes it, and a record of what was decided for each company that wasn't
added. To run the whole process again, open Claude Code and say: *"Let's look for new theatre
companies, following `collection/company_lists/README.md`."*

<!-- Format: "How to look for new companies" is the procedure; edit it when a step changes. Below
it, one `##` section per list, keyed by the ID used in the CSV's `lists` column, giving the
publisher, the original URL, the local copy, the date it was read, and what was skipped and why.
A refresh adds a new section with a new ID (e.g. `dgartes-quadrienal-2027`) and never rewrites an
old one; a later change to an old section is added as a dated note. -->

## `companies.csv` columns
- `name`: the company's public name, used as the organisation name. Where the legal name is
  different (Addingtroubles is Plataforma285), use the name people know it by.
- `region`: one of `north`, `centre`, `south`, `islands`. DGArtes uses NUTS II regions: Norte →
  `north`; Centro, Grande Lisboa, Península de Setúbal, Oeste e Vale do Tejo → `centre`; Alentejo
  and Algarve → `south`; Açores and Madeira → `islands`.
- `programme`: the DGArtes *sustained* funding programme (two-year or four-year), or blank.
  One-off project grants don't go here; they go in `lists`.
- `website`: the site that's collected. If it's blank, the company is kept on record but not
  collected (usually because it only has Facebook or Instagram).
- `lists`: the IDs of the lists below that include the company, separated by `;`.
- `last_active`: the year of the most recent sign of activity found: a funding decision, a show,
  or dated content on its site. Blank if none was found.

**Validated** organisations are the ones with `last_active` in the last two years (in 2026 that's
2024 or later). `sync_sources` sets this flag every time it runs, so a company drops out of
"validated" as its year ages, unless someone rechecks it (step 9 below).

## How to look for new companies
This is a session with Claude Code. The user decides which lists to use, and Claude Code does
the steps and reports back. Steps 1 and 9 are the user's call; Claude Code does the rest.

1. **Pick the lists.** Places to look, from most to least useful:
   - DGArtes, "Resultados dos Programas de Apoio"
     ([`/pt/node/484`](https://www.dgartes.gov.pt/pt/node/484)) and the news under "Notícias".
     *Apoio Sustentado – Teatro* decisions come out every two or four years (the next four-year
     list covers 2027–2030). *Apoio a Projetos* decisions come out every year, usually July to
     September. There are three kinds: *Criação* (and *Edição*), *Procedimento Simplificado*,
     and *Programação*. Creation is the most useful, because those are the groups that cast
     actors.
   - The Coimbra list (below). It's only worth rechecking if the university updates it.
   - Not used yet: the *Rede de Teatros e Cineteatros* decision (venues, not companies), UNIMA
     Portugal (puppetry), Performart members, Fundação GDA's supported shows, and the Lisboa and
     Porto municipal programmes.
2. **Save the original.** Download each decision into this folder as `<id>.pdf`, using an ID
   like `dgartes-projetos-criacao-2027`. Add a section for it below with the URL and today's
   date. DGArtes asks for `Crawl-delay: 10`, so wait 10 seconds between requests to its site.
3. **Extract the supported theatre rows.** Run `pdftotext -enc UTF-8 -raw <id>.pdf out.txt`.
   Use `-raw`, not `-layout`: the tables wrap long names across lines, and only `-raw` keeps one
   row per application, starting with its ID number. Keep the rows whose decision is "Apoiada" or
   "Proposta para apoio", matched **case-insensitively**, and drop "Não Apoiada" and "Não
   proposta". The 2026 PDF writes "Não Apoiada" with a capital A, and a case-sensitive filter let
   158 rejected rows through. Keep the rows in the area *Teatro*, and *Cruzamento disciplinar*
   when the project is theatre. **Check the count** against the number DGArtes announced (e.g. 54
   theatre projects in the 2026 creation call) before going on.
4. **Keep organisations, not people.** Drop applicants who are individuals (a person's full
   name). They rarely have a site, and the user wants collectives. Also drop music, dance-only and
   publishing-only applicants.
5. **Match against `companies.csv`.** Compare by name, keeping in mind that the funding list uses
   the legal name. Known pairs: Addingtroubles = Plataforma285, Enlama = LAMA Teatro, Teatreia =
   TEatroensaio, Associação do Fim do Teatro = Companhia Mascarenhas-Martins, ASTA = albiASTA,
   Colectivo 84 = Penetrarte. If the company is already there, add the new ID to `lists` and raise
   `last_active`.
6. **Find each new company's website.**
   - First try likely domains (`<name>.pt`, `.com`, `.org`, and `teatro<name>`). Accept a domain
     only if the page mentions the company's name. Then read every title, because guesses hit
     homonyms: a Finnish bank, a Brazilian group, a hotel, a pet blog.
   - For the rest, web-search `"<name>" teatro` and open the result to check that it's the
     company.
   - Check freshness: the most recent year on the page (ignore © footers), or `<updated>` in a
     blog's feed. A site with nothing after 2019 is stale, so record it as a skip.
   - **On the work network**, some sites fail with `SSLError: self-signed certificate` or a 403
     "Access Notification". That's the corporate filter, not the site (see
     [GOTCHAS](../../GOTCHAS.md)). Confirm those by search, and keep them.
7. **Add the rows.** Fill in every column: `region` from the list's NUTS II region, `programme`
   only for sustained funding, `website` blank if there's only social media, `lists`, and
   `last_active` (the decision's year, or a later year if the site shows one). Record every
   company that wasn't added, and why, in the list's section below.
8. **Check it works.** Run `uv run python manage.py sync_sources`, then `uv run python manage.py
   test`, then `uv run python manage.py collect --source co-<slug>` for the new ones. Failures from
   the work filter are expected. Anything else is a real problem, so look into it or note it in
   [IDEAS.md](../../IDEAS.md).
9. **Recheck old companies (now and then).** Find rows whose `last_active` is about to leave the
   two-year window, and look for newer activity (site, news, a new funding list). Then update the
   year, or leave it so the company stops being validated.
10. **Record and commit.** Note what was done in the active task file (or a new one), add an
    [IDEAS.md](../../IDEAS.md) entry for the ask, and commit.

## `dgartes-bienal-2025`
- **What:** DGArtes Apoio Sustentado, Teatro, two-year 2025–2026. 33 funded entities.
- **Original:** notice [`/pt/noticia/8177`](https://www.dgartes.gov.pt/pt/noticia/8177) for the
  names, and the decision table
  [`decisaofinal_anexoiv_signed.pdf`](https://www.dgartes.gov.pt/sites/default/files/decisaofinal_anexoiv_signed.pdf)
  for the regions. Both come from the "Resultados dos Programas de Apoio" page
  ([`/pt/node/484`](https://www.dgartes.gov.pt/pt/node/484)).
- **Copy:** [`dgartes-bienal-2025.pdf`](dgartes-bienal-2025.pdf). Read on 2026-10-01.
- The notice and the table disagree on one entity each (Teatro Animação de Setúbal and Teatro do
  Silêncio). Both are kept.

## `dgartes-quadrienal-2023`
- **What:** DGArtes Apoio Sustentado, Teatro, four-year 2023–2026. The 55 rows marked "Apoiada".
- **Original:** `anexo2_b_ata_8_teatro_quadrienal_decisao_final.pdf`, from the same results page.
- **Copy:** [`dgartes-quadrienal-2023.pdf`](dgartes-quadrienal-2023.pdf). Read on 2026-10-01.
- The PDF truncates long names, so each row was mapped to the company's public name. One row is
  Teatro do Montemuro, not ACERT.
- **Due for refresh in January 2027:** DGArtes has published the 2027–2030 renewal list
  (`lista_entidades_sustentados_renovacao_30out25.pdf`).

## DGArtes entity directory (websites only)
- **What:** DGArtes's public page for each funded entity, giving its website and region
  ([`/pt/vnode/4`](https://www.dgartes.gov.pt/pt/vnode/4), area Teatro). It's not a list of its
  own: it holds about 70 theatre entities, almost all already on the two lists above.
- **Copy:** [`dgartes-directory.json`](dgartes-directory.json), 66 entities, crawled on 2026-10-01
  following the site's `Crawl-delay: 10`.

## `coimbra`
- **What:** Centro de Dramaturgia, Universidade de Coimbra, *Companhias profissionais de teatro
  em Portugal (1974-)*. It has 92 companies, each with city, years active, website and a short
  description. It's the only nationwide list that also covers unfunded companies, but it was
  last updated around 2015.
- **Original:**
  [uc.pt/org/centrodramaturgia/10/diretorio_companhias/teatro_profissional](https://www.uc.pt/org/centrodramaturgia/10/diretorio_companhias/teatro_profissional)
  (a PDF, despite the URL).
- **Copy:** [`coimbra.pdf`](coimbra.pdf). Read on 2026-10-01.
- 34 were already in the CSV (from DGArtes) and 22 were added. The rest weren't added:
  - **Closed or changed field:** Mundo Perfeito (closed 2015), .lilástico (1999–2005), Útero (a
    dance company since 2011), Companhia Teatral do Chiado (in liquidation; its domain now hosts
    spam), O Cão Danado (domain suspended). REFLEXO is a duplicate of Teatro Reflexo.
  - **Active but only on Facebook or Instagram:** Casa Conveniente, Palco 13, Teatro Carbono, A Má
    Companhia, Ao Cabo Teatro, Teatro Tapa Furos, Bica Teatro, Teatro Bruto, Teatro Fórum de
    Moura, ASTA (that's albiASTA, already in the CSV; its blog is private).
  - **Site gone, nothing newer found:** D'As Entranhas, Jangada de Pedra, Teatro ao Largo, Gato
    que Ladra (`gatoqueladra.pt` doesn't load), Pim Teatro, Teatro Reactor, Teatro Reflexo.
  - **Site stale (nothing since 2019 or earlier):** Casa da Esquina, A Máquina Agradável, O Nariz,
    Ninho de Víboras, Palmilha Dentada, Panmixia, Pequeno Palco de Lisboa, Ponto Teatro, Projecto
    Teatral, Propositário Azul, Teatro Plástico, Teatro TOITOI, Truta, Utopia Teatro.
- *Note, 2026-10-01 (later):* Casa Conveniente, Palmilha Dentada and Propositário Azul were then
  added without a website, because they're on the project-grant lists below. `last_active` was
  left blank for O ENTREtanto TEATRO and Teatro do Elefante, because their sites are behind the
  work filter and search found no dated activity, so they aren't validated. Cassefaz's latest
  activity is 2023.

## `dgartes-projetos-criacao-edicao-2025`
- **What:** DGArtes Apoio a Projetos 2025, *Criação e Edição* (circus, dance, theatre, street
  arts, cross-disciplinary). 161 projects were supported across all areas. 120 rows are
  supported theatre (or cross-disciplinary) rows, and 68 of those organisations are now in the CSV.
- **Original:** announcement [`/pt/node/8909`](https://www.dgartes.gov.pt/pt/node/8909), decision
  [`pap25_criacaoeedicao_anexoii_2projetodecisao.pdf`](https://www.dgartes.gov.pt/sites/default/files/pap25_criacaoeedicao_anexoii_2projetodecisao.pdf).
- **Copy:** [`dgartes-projetos-criacao-edicao-2025.pdf`](dgartes-projetos-criacao-edicao-2025.pdf).
  Read on 2026-10-01.

## `dgartes-projetos-criacao-2026`
- **What:** DGArtes Apoio a Projetos 2025 call, decided in 2026, *Criação* (street arts, circus,
  dance, theatre). 84 supported, 54 of them theatre. 38 theatre rows parsed (the rest are
  cross-disciplinary or were filed under other areas), and 25 of those organisations are now in the CSV.
- **Original:** announcement [`/pt/node/10252`](https://www.dgartes.gov.pt/pt/node/10252),
  decision
  [`decisao_final_anexoii_criacao_artes_de_rua_circo_danca_e_teatro.pdf`](https://www.dgartes.gov.pt/sites/default/files/decisao_final_anexoii_criacao_artes_de_rua_circo_danca_e_teatro.pdf).
- **Copy:** [`dgartes-projetos-criacao-2026.pdf`](dgartes-projetos-criacao-2026.pdf). Read on
  2026-10-01.

## `dgartes-projetos-simplificado-2026`
- **What:** DGArtes Apoio a Projetos, *Procedimento Simplificado* (small grants of up to 5,000 €),
  decided on 2026-07-23. 142 supported across all areas, 36 of them theatre. Most are individuals, and 11 organisations are now in the CSV.
- **Original:** announcement [`/pt/noticia/10102`](https://www.dgartes.gov.pt/pt/noticia/10102),
  decision
  [`anexo_1_procedimento_simplificado_decisaofinal_23072026.pdf`](http://www.dgartes.gov.pt/sites/default/files/anexo_1_procedimento_simplificado_decisaofinal_23072026.pdf).
- **Copy:** [`dgartes-projetos-simplificado-2026.pdf`](dgartes-projetos-simplificado-2026.pdf).
  Read on 2026-10-01.

### What came of the three project lists (2026-10-01)
- **84 organisations added**, all with `last_active` 2025 or 2026, so all are validated. **33
  have a website** and are collected. Examples: Teatro GRIOT, Teatro da Cidade, Má-Criação, Grua
  Crua, Teatro Nacional 21, Tremor Teatro, Lobby Teatro, Saaraci, A Bolha, Teatro Maizum, Mochos
  no Telhado, Fogo Lento. Ten companies already in the CSV got the project IDs added to `lists`.
- **Added without a website** (only social media, or nothing found): the remaining ~50, for
  example auéééu, Estado Zero, Royal Teatro Livre, Ritual de Domingo, Sociedade das Primas,
  Segundas Intenções, Cia Mnemos, As Divas da Aldeia, Ressurrectos, Teatro do Interior.
- **Not added:** individual applicants (about 85 across the three lists); Trypas Corassão (a
  music and performance duo); Cotão (it produces other artists' work); Medusa Material (nothing
  found); music, dance-only and publishing-only applicants.
- **Known collection problem:** OUTRO (`outro.pt`) links to a members-only `/portal` page. The
  link matches the keywords, the page returns 401, and the whole source fails. *Fixed the same day:* `site_watch` now skips a followed page that fails.
