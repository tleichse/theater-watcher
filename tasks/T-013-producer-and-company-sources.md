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

## Proposed approach
1. TV producers: SP Televisão (SIC), RTP's main independent producers (Coral Europa, Ukbar,
   Stopline, Hop!, and others found during the check), and Plural's sister companies. For each,
   check for a casting or contact page, news or a feed, freshness, and `robots.txt`.
2. ICA "Projetos em Curso" and "Vistos de rodagem".
3. The DGArtes-funded companies: list their sites and check which post auditions.
4. Add the sources that pass to the registry, and run a real collect.

## Acceptance criteria
- [ ] Each producer and ICA page checked, with a verdict
- [ ] The DGArtes-funded company list checked, with a verdict per site
- [ ] Sources that pass are in the registry and collect without errors

## Implementation
