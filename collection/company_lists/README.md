# Company lists

Where the theatre companies in [`../companies.csv`](../companies.csv) come from. This folder keeps
a copy of each original list, so it can be rechecked if the publisher changes or removes it, and
a record of what was decided for each company that wasn't added.

<!-- Format: one `##` section per list, keyed by the ID used in the CSV's `lists` column. Each
section gives the publisher, the original URL, the local copy, the date it was read, and what
was skipped and why. A refresh adds a new section with a new ID (e.g. `dgartes-quadrienal-2027`)
and never rewrites an old one. The steps for a refresh are in HOWTO.md. -->

## `companies.csv` columns
- `name`: the company's public name, used as the organisation name.
- `region`: one of `north`, `centre`, `south`, `islands`. "Grande Lisboa", the Península de
  Setúbal and the Oeste count as `centre`.
- `programme`: the DGArtes funding programme, or blank if the company isn't funded. A
  non-blank value makes the organisation **validated**.
- `website`: the site that's collected. If it's blank, the company is kept on record but not
  collected.
- `lists`: the IDs of the lists below that include the company, separated by `;`.

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
