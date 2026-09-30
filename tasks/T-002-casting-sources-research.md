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
- ~~Who are **the people** receiving the digest: professional actors, beginners, parents of
  child actors? This decides whether extras, modelling, and children's castings belong in the
  digest. Those make up most of the volume on the tier C aggregators.~~
  **Answer (2026-09-30):** professional actors. Extras, modelling, promoter and children's
  castings, and non-acting roles, are out of scope. That removes most of the tier C volume.
- **Legal:** do the site terms allow automated collection, and can listings be republished in
  an email? The recipient list will also need GDPR consent and unsubscribe handling. These
  must be answered before building the collector.
- ~~Should Facebook groups be covered? They carry a lot of volume, but automated access breaks
  Meta's terms. Options: leave them out, or have a person curate them by hand.~~
  **Answer (2026-09-30):** leave them out for now.

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

## Proposed approach
1. Web search in Portuguese and English for each pillar, plus the cross-pillar platforms.
2. Open the key sources to check they're active, who posts, and whether applying costs money.
3. Put together a tiered catalogue with notes on how each source can be accessed.
4. Review it with the user, answer the open questions, and fix the final source list.

## Acceptance criteria
- [x] Sources found for each of the 5 pillars
- [x] Each source has a trust tier and notes on access
- [x] The user has reviewed the catalogue and settled what "validated" means
- [ ] The legal and terms-of-service position on collection and republishing is settled
- [ ] Final source list agreed. It becomes the input to the collector task (not yet created).

## Implementation
**2026-09-30:** first pass done: steps 1–3. Each source above was found by web search. These
were opened and checked directly: Coffeepaste, becasting, PortalCastings, and enCAST. Not
checked yet: SeekCasting, TNDM's current audition page, the People Stars and Make Me A Star
casting sheets, and each site's terms and `robots.txt`.
