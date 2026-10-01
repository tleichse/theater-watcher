# T-002: Research validated sources of casting opportunities in Portugal

**Origin:** [IDEAS.md, 2026-09-30](../IDEAS.md#2026-09-30). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "the idea behind the the theatre watcher is to gather all the oportuinities for working in
> Theatre, Cinema (movies / series / documentaries), TV (soap operas), but also for marketing
> sketches (TV and radio) and dubbing  in Portugal. The idea is to have a weekly digest (an
> email) sent to people with info on new opportungities for castings in the pillars dfined
> (Theatre, Cinema, TV, Marketing and Dubbing). We can gather info from validated sources in
> Portugal. We first need to make a complete search on that."

## Repo context
- There's no code yet. The project was just bootstrapped
  ([T-001](T-001-bootstrap-doc-system.md)).
- This task is research only. Choosing a stack, a way to collect listings, and a way to send
  email are left to later tasks.

## Open questions
- ~~What counts as **"validated"**? Proposal: a source is validated if the organisation behind
  it is named and it states its own calls (tiers A and B below). Tier C is included only with
  deduplication and a visible "via <site>" label, or left out entirely.~~
  **Answer (2026-09-30):** the proposal is agreed. Only tiers A and B count as validated. A tier C
  source can be included only if it's deduplicated and labelled "via <site>". That's decided per
  source when the final list is fixed.
  **Amended 2026-10-01:** the user made traceability a hard rule: "you have to know who is
  posting". Tier C sources (anonymous posters) are now excluded outright, and every action
  must name its poster before it's approved, enforced in
  [T-006](T-006-traceable-poster.md).
- ~~Who are **the people** receiving the digest: professional actors, beginners, parents of
  child actors? This decides whether extras, modelling, and children's castings belong in the
  digest. Those make up most of the volume on the tier C aggregators.~~
  **Answer (2026-09-30):** professional actors. Extras, modelling, promoter and children's
  castings, and non-acting roles, are out of scope. That removes most of the tier C volume.
- ~~**Legal:** do the site terms allow automated collection, and can listings be republished in
  an email? The recipient list will also need GDPR consent and unsubscribe handling. These
  must be answered before building the collector.~~
  **Partly answered (2026-09-30):** researched in the legal-check deep dive below, which
  proposes a "link-out digest" policy. Still needed: the user's sign-off on that policy and a
  decision on whether to contact Coffeepaste and enCAST for permission.
  **Answer (2026-10-01):** the link-out policy is approved. Coffeepaste and enCAST will **not**
  be asked for permission; they're used as they are. That drops point 4 of the policy. The
  remaining *Ryanair*-style risk is low: Coffeepaste publishes no terms, and enCAST's terms
  allow fair linking.
- ~~Should Facebook groups be covered? They carry a lot of volume, but automated access breaks
  Meta's terms. Options: leave them out, or have a person curate them by hand.~~
  **Answer (2026-09-30):** leave them out for now.
- How should **Marketing and Dubbing** be covered, given that no public source is left for
  them after the verification pass? **Answer (2026-10-01):** "Find them": research dedicated
  sources (step 5 below).
- Where do **training** opportunities come from (folded in from T-003)? **Answer
  (2026-10-01):** research them now (step 6 below).
- ~~To give Marketing more volume, should **becasting's advertising category** be admitted as
  tier C, labelled "via becasting" and deduplicated, which the validated-source rule allows?
  It has no AI opt-out in `robots.txt`, but its terms forbid copying, so facts and a link only.
  Or should the section stay thin?~~ **Answer (2026-10-01):** no. Its posters are anonymous,
  which breaks the traceability rule (see the "validated" answer above). The Marketing
  section stays thin.
- Is **VSI Lisbon** the "VS Digital Media" the user meant? If not, which studio was it?

## Deep dive: source catalogue (first pass, 2026-09-30)

**Trust tiers:**
- **A, primary:** the organisation that is casting publishes the call itself.
- **B, curated board:** a board with editorial control where each call names who posted it.
- **C, open aggregator:** calls are often anonymous, repeated across several sites, and mixed
  with modelling and extras work.
- **Signal:** not a casting call, but an early sign that a production is coming, which
  usually means castings will follow.

### Cross-pillar boards
| Source | Tier | Notes |
|---|---|---|
| [Coffeepaste — Classificados](https://www.coffeepaste.com/en/classificados/) | B | The main board for the Portuguese arts community. Its categories include `Audição / Casting` and `Oportunidade`. It's active: 15 posts on 29–30 Sep 2026, including a PT-PT voice call. No RSS feed or API was found. |
| [enCAST.pro — Portugal](https://www.encast.pro/castings/portugal) | B | Free to join. Each call names who posted it and whether it's paid. Low volume (7 open calls), and some are for shoots outside Portugal. |
| [becasting.pt](https://www.becasting.pt/castingo) (formerly Casting.com.pt, part of an international network) | C | High volume, with categories for Cinema/Ficção, Teatro, TV, Rádio, and Voz off. Posters are anonymous. Free, with a paid VIP tier. Mixes in music-teacher and modelling calls. |
| [PortalCastings](https://www.portalcastings.com/) / [Castings24](https://www.castings24.com/) (same operator) | C | Free to apply. Sources are not named. Heavy on advertising and events. |
| [SeekCasting](https://www.seekcasting.com/) | C | Aggregator. Not checked in detail yet. |
| Facebook groups (e.g. "CASTINGS PORTUGAL", "CASTING ATORES E FIGURANTES") | C | High volume but can't be collected automatically. See the open questions. |

### Theatre
| Source | Tier | Notes |
|---|---|---|
| [Teatro Nacional São João](https://www.tnsj.pt/pt/noticias/) | A | Announces auditions as news posts, and candidates apply by email (e.g. the Nelson Rodrigues audition, May 2025). |
| [Teatro Nacional D. Maria II](https://www.tndm.pt/) | A | Has an auditions page, but `/pt/audicao/` returned 404 on 2026-09-30. The current location still needs to be found. |
| [Teatro São Luiz — Open Call](https://www.teatrosaoluiz.pt/espetaculo/open-call-audicoes/) | A | Open calls published as show pages |
| Independent companies (e.g. Companhia de Teatro O Sonho) | A | They mostly post on Coffeepaste, so covering Coffeepaste covers most of them. |

### Cinema (films, series, documentaries)
| Source | Tier | Notes |
|---|---|---|
| Casting directors, e.g. [Patrícia Vasconcelos / ACT](https://act-escoladeactores.com/act/team/patricia-vasconcelos/), [Mansarda](https://mansarda.pt/fundadores/) | A | Mostly cast through agencies. Public calls are rare and appear on their sites or social media. |
| [ICA — Filmes Produzidos 2026](https://ica-ip.pt/pt/tabelas/filmes-produzidos-2026/) | Signal | The official list of productions |
| [Portugal Film Commission — Notícias](https://portugalfilmcommission.com/noticias/) | Signal | Announces shoots, including international productions filming in Portugal |

### TV (soap operas)
| Source | Tier | Notes |
|---|---|---|
| [Plural Entertainment — Atores](https://pluralentertainment.com/casting-figuracao/atores/) / [Figuração](https://pluralentertainment.com/casting-figuracao/figuracao/) | A | Produces TVI's soap operas. These are standing application forms, not calls for specific roles, so the digest should list them as "always open", not as new. |
| [SP Televisão](https://pt.linkedin.com/company/sp-televisao) | A | Produces SIC's soap operas. No public casting page found; its castings get covered in the press. |
| TV press: [atelevisao.com](https://www.atelevisao.com/), [Zapping-TV — casting](https://www.zapping-tv.com/tag/casting/), [MAGG — casting](https://magg.sapo.pt/tag/casting) | Signal/B | Report new soap operas and occasional open castings, e.g. a TVI call for cooks and SIC's *Destino Maior* in pre-production. |

### Marketing (TV and radio ads and sketches)
| Source | Tier | Notes |
|---|---|---|
| Agencies: [Crowd](https://www.crowd.pt/), [Valente Produções](https://valentep.com/), [People Stars](https://www.peoplestars-agency.com/castings), [Make Me A Star](http://makemeastar.pt/pt/folhacastings/) | A/B | Several publish public casting sheets (People Stars `/castings`, Make Me A Star `folhacastings`). Most advertising work is cast only among an agency's own represented talent. |
| Production companies (e.g. [Krypton](https://www.briefing.pt/noticias/a-krypton-na-producao-de-services-e-tropa-de-elite/), Produções Fictícias) | A | Cast through agencies and casting directors. Public calls are rare. |

### Dubbing
| Source | Tier | Notes |
|---|---|---|
| Studios: Iyuno Portugal (ex-Matinha; Disney's official PT-PT studio), Pim Pam Pum, Cinemágica, Som Norte | A | Cast from a pool of voices they already know. No public casting pages found. |
| Voice agencies: [Soundtrap Productions](https://www.soundtrap-productions.net/en/castings-and-voice-agency-services-in-portugal/), [VOZ ON](https://vozon.pt/) | A | Represent voice talent and run castings for their own roster |
| Occasional public calls on Coffeepaste and [becasting voz off](https://www.becasting.pt/pages/303-casting-voz-off) | B/C | Rare but real, e.g. "Procura-se voz em português europeu", 2026-09-30 |

### Adjacent (not casting calls)
- [Fundação GDA](https://www.fundacaogda.pt/concursos-2026-consulte-as-datas/): funding and
  training competitions for professional performers. These could be an optional section of
  the digest.
- CENA-STE (the performers' union; website not checked) and Plateia (the association
  of performing-arts professionals): no casting boards found. They may be useful as
  distribution partners.

### Key findings
1. **The pillars aren't equally public.** Theatre and independent film have many public calls.
   Soap operas, advertising, and above all dubbing are cast mostly through closed agency or
   studio pools. A digest built from public sources alone will be thin on Marketing and
   Dubbing, which needs to be said openly or covered by agency partnerships.
2. **Most volume is on tier C.** The same calls get reposted across aggregators, so
   deduplication is required.
3. **Signals add value.** Upcoming productions from ICA, the Film Commission, and the TV
   press would let the digest say "castings likely soon" before any call appears.
4. **None of the sources checked has an RSS feed or API.** Collecting means scraping HTML,
   which makes the legal question above a blocker.

## Deep dive: verification pass (2026-09-30)

Checked `robots.txt`, the terms of use, and any machine-readable feeds for every source, and
opened each source that hadn't been checked yet. Where this section disagrees with the
first-pass catalogue above, this section is the more recent one.

| Source | robots.txt | Terms of use | Feed / structure | Verdict |
|---|---|---|---|---|
| Coffeepaste | Allows everything | None published (only a privacy policy and an editorial statute) | No RSS. Listings are server-rendered HTML at `/en/classificado/<slug>/`. | **Include.** Ask for permission (see policy). |
| enCAST.pro | Public pages allowed. It blocks only SEO crawlers and says it welcomes "AI crawlers that read this file". | No rule on scraping. Linking is allowed "if done fairly". Estonian law. | `sitemap-castings.xml` | **Include** |
| TNSJ | Allows everything | Only a privacy policy | `sitemap.xml`. Auditions are posted as news. | **Include** |
| TNDM | Blocks only system folders | The conditions page covers ticketing only | The site was relaunched, so the old `/pt/…` URLs return 404 even though search engines still list them. Auditions and internships (e.g. the 2026 performer internships, applications 15 Apr–15 May) are announced under `/noticias`. | **Include** via `/noticias` |
| Teatro São Luiz | Allows everything | Only a privacy policy (EGEAC) | RSS at `/feed/` | **Include** |
| Plural Entertainment | Allows everything | Only a privacy policy | RSS at `/feed/` | **Include** as a standing "always open" entry |
| People Stars | Allows everything | — | The page looks active, but the latest open call had its deadline on 12/11/2024, and the history runs 2022–2024. Applying requires signing up with the agency first. | **Exclude:** stale, and cast from its own talent pool |
| Make Me A Star | Allows everything | — | Latest entry 10/02/2024. About 80% advertising, many aimed at "new faces", about 40% confidential. | **Exclude:** stale, and not aimed at professionals |
| becasting.pt | Blocks some search and pagination URLs | Operated by Event&Com in Paris under French law. Members may not copy or reproduce content. | — | **Exclude:** tier C, anonymous posters, mostly out of scope for professionals |
| PortalCastings / Castings24 | **Blocks AI and training crawlers** (GPTBot, ClaudeBot, CCBot, Google-Extended…) and allows everything else | Operated by Identiffysuccess Lda (Lisbon). No rule on scraping. | `sitemap.xml`. Castings24 is only a landing page for PortalCastings. | **Exclude:** tier C, sources not named, and it has opted out of AI use |
| SeekCasting | — | — | **Unreachable** on 2026-09-30: timed out from here and connection refused through a second network | **Exclude.** Check again later. |
| ICA (production list) | None (404) | — | HTML tables | **Include** as a signal |
| Portugal Film Commission | Allows everything | — | RSS at `/feed/` | **Include** as a signal |
| atelevisao / Zapping-TV / MAGG | Allow everything | MAGG: all rights reserved, and any use needs consent. atelevisao's terms couldn't be loaded (connection reset). | RSS feeds, including `zapping-tv.com/tag/casting/feed/` and `magg.sapo.pt/tag/casting/feed/` | **Include** as signals, **headline and link only** |

**Proposed final source list:** Coffeepaste, enCAST, TNSJ, TNDM, São Luiz, and Plural as
casting calls. ICA, the Film Commission, and the three TV news sites as "castings likely soon"
signals. Every tier C source is out. Marketing and Dubbing have **no remaining public source**
other than the occasional Coffeepaste or enCAST post. Covering them would need agreements with
agencies and studios. That's a product decision for a later task.
*Addendum (2026-09-30):* the public-sector deep dive below adds the DGArtes funded-company
watch list and, optionally, the DGArtes `oportunidade` feed.

## Deep dive: public-sector sources, DGArtes and GEPAC (2026-09-30)

The user suggested these on 2026-09-30. Neither one publishes castings. Both fund, regulate, or
study the sector, so what they're useful for is different:

| Source | What it publishes | Access | Verdict |
|---|---|---|---|
| [DGArtes: `oportunidade` tag](https://www.dgartes.gov.pt/pt/taxonomy/term/123) | Third-party open calls: residencies, festivals, prizes, grants. Several a week, and active (10 items 28 Aug–23 Sep 2026). Mostly visual arts or international, with some performing arts (e.g. calls from theatre festivals). | **RSS** at `/pt/taxonomy/term/123/feed`. `robots.txt` asks for `Crawl-delay: 10`. The site-wide `/pt/rss.xml` is stale (newest item 2022). | **Include**, but in an optional "Apoios e oportunidades" section filtered to performing arts, not among the castings |
| [DGArtes: support results](https://www.dgartes.gov.pt/pt/node/484) | The lists of theatre companies that receive state funding, e.g. 33 theatre structures in the 2025–26 biennial sustained support. | HTML news pages and notices | **Use as a watch list.** A company on this list is a named, funded producer (tier A by definition). Their sites and posts are where theatre auditions come from. This is also a concrete way to define "validated" for theatre. |
| [DGArtes: open calls](https://www.dgartes.gov.pt/pt/vnode/1) | Funding programmes for companies (sustained support, projects) | HTML | **Exclude:** these are aimed at companies, not actors |
| [GEPAC](https://www.gepac.gov.pt/) | Cultural statistics and strategy. The Fundo de Fomento Cultural notices ([`/fundo-fomento/avisos`](https://www.gepac.gov.pt/fundo-fomento/avisos)), e.g. the cultural merit projects call, open 14 Sep–6 Oct 2026. Recruitment for its own civil-service posts. | The site is a Nuxt app that renders in the browser, so fetching it returns no content and collecting from it would need a headless browser or its internal API. There's no `robots.txt` (404). | **Exclude for now:** it has no castings and costs a lot to collect. The funding calls reach people through Cultura Portugal and DGArtes anyway. |
| [Cultura Portugal (Ministry of Culture portal): *Criar › Apoios*](https://culturaportugal.gov.pt/pt/criar/) | Aggregates funding, prizes, and open calls from across the Ministry, including third-party calls | HTML (Umbraco CMS). `robots.txt` blocks only system folders. No RSS found. | **Optional:** it overlaps with the DGArtes feed, so it's only worth adding if we build the "Apoios" section |

Note: the Registo dos Profissionais da Área da Cultura (RPAC) is managed by
[IGAC](https://www.igac.gov.pt/servicos/catalogo-de-servicos/registo-dos-profissionais-da-area-da-cultura-e-cancelamento),
not GEPAC. It's a registry of professionals, not a source of opportunities.

## Deep dive: legal check (2026-09-30)

*This is research, not legal advice. Before a public launch, and especially before any
monetisation, a Portuguese lawyer should review it.*

**Laws and cases that apply:**
- **Copyright:** CDADC art. 7(1)(a) excludes from protection "notícias do dia e relatos de
  acontecimentos diversos com carácter de simples informações". Facts such as role, dates,
  place, and deadline aren't protected. The descriptive text of a listing, and any photos,
  may be.
- **Database right:** DL 122/2000, which transposes Directive 96/9/EC, lets the maker of a
  database that took substantial investment prohibit the extraction or reuse of a *substantial
  part* of it. The test from [CJEU C-762/19 *CV-Online Latvia*](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A62019CA0762)
  (2021), a case about a meta search engine for job ads, is whether the reuse puts the maker's
  investment at risk of not being recouped. A service that indexes listings and **sends
  traffic back** to the source is on the safe side of that test. A service that **replaces**
  the source is not.
- **Terms as a contract:** [CJEU C-30/14 *Ryanair v PR Aviation*](https://www.lexology.com/library/detail.aspx?g=892f2083-6557-4314-9cad-900d710d67c3)
  (2015) held that a database with no IP protection can still restrict scraping through its
  terms of use. So what each site's terms say matters, as recorded in the table above.
- **Text and data mining:** DL 47/2023 transposes the DSM Directive 2019/790. Its mining
  exception doesn't apply where the rightholder has opted out in a machine-readable way. A
  `robots.txt` that blocks AI crawlers, like PortalCastings', should be treated as that
  opt-out. This matters if listings are ever classified or summarised with an LLM.
- **Press publishers' right** (DSM art. 15, via DL 47/2023): news sites may control reuse
  beyond hyperlinks and very short extracts. For the TV news sites that means **headline and
  link only**.
- **Personal data in listings** (GDPR): calls often name casting directors and give their
  emails. Copying those into an email we send out means processing them. Linking to the
  source avoids that.
- **Subscribers:** GDPR arts. 6(1)(a) and 7, plus Lei 41/2004 art. 13.º-A, which requires
  prior express consent for email to individuals and a way to refuse in every message. The
  supervisory authority is the CNPD.

**Proposed operating policy (the "link-out digest"):**
1. The digest carries only **facts**: pillar, role or project title, location, dates, whether
   it's paid, the deadline, and the source's name with a **link to the original**. It never
   copies descriptive text, images, or contact details, and people always apply at the
   source.
2. The collector respects `robots.txt`, identifies itself with a user-agent string that
   includes a contact URL, fetches at a low rate (daily at most), and uses RSS or sitemaps
   where they exist.
3. Sources that reserve their rights (PortalCastings, becasting) are excluded, as the table
   above already does. News sites get headline and link only.
4. Ask the main sources for written permission: **Coffeepaste** (which has no terms at all)
   and **enCAST**. Their OK removes the *Ryanair*-style contract risk, and it can lead to a
   partnership.
5. Subscribers: double opt-in, a pt-PT privacy notice naming who controls the data, an
   unsubscribe link in every email, and a stored record of each consent.
6. Only run an LLM over content from sources that haven't opted out of mining.

## Deep dive: Marketing, Dubbing, and training sources (2026-10-01)

Steps 5 and 6 below. Every site was loaded directly (`curl` status code, `robots.txt`, feed
check), per the gotcha about stale search results.

**The user's lead, "VS Digital Media":** the only company by that name is a UK SEO agency
with no link to Portugal. The Lisbon dubbing studio the user most likely meant is
**[VSI Lisbon](https://www.vsi.tv/lisbon)** (VSI Group, in Carnaxide). Its page offers **no
training, workshops, or voice calls**, only occasional office jobs, so it's not a source.
*To confirm with the user that this is the studio they meant.*

### Training
| Source | Region | What it offers | Access | Verdict |
|---|---|---|---|---|
| [ACT Escola de Actores / Act4all](https://act-escoladeactores.com/act/proximos-workshops/) | Centro (Lisboa) | Short paid workshops for adults, about 14 upcoming: camera and casting technique (international workshop 29–31 Oct 2026), film and TV acting, multi-camera TV, **dubbing** ("Dobragem: Voz, Postura e Práticas"), improv. | **RSS** at `/feed/`, active (latest item Aug 2026). `robots.txt` has no rules. | **Include** (tier A) |
| [Conservatório Vocare](https://conservatoriovocare.pt/formacoes) | Norte (Porto) | DGERT-certified short courses: **Dobragem para animação** (3 × 16 h levels, Level I 26–27 Sep 2026) and **Locução para Rádio e Publicidade**. | HTML. No feed (`/feed/` is a 404 page). `robots.txt` blocks only system folders. | **Include** (tier A). One of the few sources for Dubbing and Marketing skills. |
| [Coffeepaste — Formação category](https://www.coffeepaste.com/en/classificados/) | All | Several training posts a week (7 of the 15 newest listings on 30 Sep), mostly dance, movement, and AEC teaching jobs. | Already a source. | **Include** through the existing collector, filtered to acting, voice, and camera |
| [Fundação GDA](https://www.fundacaogda.pt/) | Nacional | Support calls for performers (theatre and dance shows, short films) and the **Contratação+** database that connects actors aged ≤30 or 60+ with film and TV producers. | **RSS** at `/feed/`, active (Sep 2026). `robots.txt` allows everything. | **Include** for "Apoios e oportunidades" |
| [EVOÉ](https://evoe.pt/) | Centro (Lisboa) | Acting school. Its RSS feed lists comedy and improv shows, not courses. | RSS for shows only | **Exclude**: the feed is the wrong content, and courses run all year |
| [ACE / Teatro do Bolhão](https://ace-tb.com/) | Norte (Porto) | Multi-year professional course (it includes 50 h of acting for camera) | HTML | **Exclude**: an enrolment programme, not a weekly opportunity |
| [World Academy](https://www.worldacademy.pt/cursos/workshops/espetaculos-e-eventos/locucao-e-dobragens/) | Centro (Carnaxide) | Voice-over and dubbing course, €280 | HTML | **Exclude**: stale, its only edition was Feb–Mar 2025 |
| NB Academia | Centro | Acting school | `robots.txt` has `Disallow: /` | **Exclude**: it opted out of crawling |

### Dubbing
- **Studios cast from their own pools and publish no calls.** Checked: VSI Lisbon, 112
  Studios, and Iyuno Portugal (formerly SDI Media / Matinha, the largest). Pim Pam Pum's site
  renders in the browser, so fetching it returns no content. Cinemágica (Gaia) didn't respond. The
  Vozes Mágicas voice agency's blog is from 2008.
- What does reach the public: **voice calls on Coffeepaste** ("Procura-se voz em português
  europeu", 30 Sep 2026) and **enCAST** (a dubbing project in Lisbon looking for voice
  impressionists). Both are already sources, so extraction just has to tag them `dubbing`.
- Training for the pillar comes from ACT and Vocare (above).

### Marketing
- **Advertising castings run through talent agencies that cast from their own pools.** Klip,
  Crowd, Absoluteface, and Blast only offer sign-up forms. Valente Produções has a
  `/castings` page, but it has no active calls (latest April 2026), and the calls are mixed
  with "new faces" and babies. That's the same pattern as People Stars, which was excluded.
- The open advertising calls sit on the **tier C aggregators** already excluded (becasting,
  PortalCastings, Make Me A Star). becasting currently lists several advertising calls (Lisbon
  and Porto), but they come from anonymous posters and are mixed with children's and extras
  work.
- What reaches the public through validated sources: occasional advertising and
  social-campaign calls on **enCAST** (Porto and Lisbon, actors 25–40) and Coffeepaste. These
  are already sources, so extraction tags them `marketing`.

**Finding:** no validated public source is dedicated to Marketing or Dubbing. Both pillars will
be fed by enCAST and Coffeepaste posts plus training (ACT, Vocare), so expect "Sem novidades
esta semana" in those sections most weeks. The options to fill them out are product decisions,
listed in the open questions.

## Proposed approach
1. Web search in Portuguese and English for each pillar, plus the cross-pillar platforms.
2. Open the key sources to check they're active, who posts, and whether applying costs money.
3. Put together a tiered catalogue with notes on how each source can be accessed.
4. Review it with the user, answer the open questions, and fix the final source list.
5. *(Added 2026-10-01.)* Search specifically for **Marketing** (ad and radio-spot casting:
   advertising-casting agencies, production companies, voice-over agencies) and **Dubbing**
   (dubbing studios and their voice-test calls) sources, verify each with the same checks as
   the verification pass, and add them to the catalogue.
6. *(Added 2026-10-01.)* Search for **training** sources across the five pillars (free and paid
   workshops, masterclasses, courses), verify them the same way, and add them to the
   catalogue.

## Acceptance criteria
- [x] Sources found for each of the 5 pillars
- [x] Each source has a trust tier and notes on access
- [x] The user has reviewed the catalogue and settled what "validated" means
- [x] The legal and terms-of-service position on collection and republishing is settled
- [x] Verified sources found for Marketing and Dubbing, or a recorded finding that none exist
- [x] Verified training sources in the catalogue
- [ ] Final source list agreed. It becomes the input to the collector task (not yet created).

## Implementation
**2026-09-30:** first pass done: steps 1–3. Each source above was found by web search. These
were opened and checked directly: Coffeepaste, becasting, PortalCastings, and enCAST. Not
checked yet: SeekCasting, TNDM's current audition page, the People Stars and Make Me A Star
casting sheets, and each site's terms and `robots.txt`.

**2026-09-30 (later):** finished the verification pass and the legal check (both deep dives
above). What changed from the first pass:
- People Stars and Make Me A Star turned out to be stale (latest calls 2024), so they're out.
- SeekCasting was unreachable.
- TNDM's site was relaunched, so auditions are now found through `/noticias`.
- Found RSS feeds for São Luiz, Plural, the Film Commission, and the TV news sites.

Once the tier C sources were dropped, Marketing and Dubbing were left with no dedicated
public source. That's recorded as a product decision for later.

**2026-09-30 (later):** checked DGArtes and GEPAC at the user's suggestion (see the
public-sector deep dive). Neither publishes castings. DGArtes turned out to be useful in two
ways: a live `oportunidade` RSS feed, and its lists of funded theatre companies, which can be
the watch list that defines "validated" for Theatre. GEPAC was left out: its site renders in
the browser, and its content (funding notices, statistics) overlaps with DGArtes and Cultura
Portugal.

**2026-10-01:** did steps 5 and 6 (see the Marketing, Dubbing, and training deep dive).
Added three training and support sources (ACT, Vocare, Fundação GDA), and Coffeepaste's
Formação category comes through the existing collector. Dubbing and Marketing turned out to
have no dedicated public source: studios and agencies cast from their own pools. The user's
"VS Digital Media" lead was probably VSI Lisbon, which publishes nothing usable.
