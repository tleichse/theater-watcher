# T-015: An exhaustive database of everyone who posts opportunities

**Origin:** [IDEAS.md, 2026-10-01](../IDEAS.md#2026-10-01). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "to have all the possible contacts for casting, auditions and opportuinites for theatre,
> cinema, TV, publicity, dubbing, and training (all we have now) in Portugal. We want an
> exhaustive database." then "don't forget the rede de teatros"

## Repo context
- Before this task the database held the theatre companies (`companies.csv`, T-013) and the film
  and TV producers (`producers.csv`, T-013), loaded by `sync_sources` as `Organisation` rows and,
  where they have a website, as `site_watch` sources.
- `Organisation` had only a name, a website and a "validated" flag, so the contacts couldn't be
  told apart or filtered.
- T-002 and T-012 found that dubbing studios, talent agencies and schools rarely post public calls
  on their own sites. They're still the people to contact (GROWTH #1), so they belong in the
  database even when collecting them yields little.
- Rules that still apply: link-out and robots.txt (T-002), no Facebook or Instagram scraping
  (T-002), modelling and extras are out of audience (T-002).

## Deep dive: shape of the database
- **One CSV per family, same code path.** `companies.csv` (theatre companies), `producers.csv`
  (screen industry: producers, casting and agencies, dubbing and voice, funders), `venues.csv`
  (theatres, venues, festivals, commercial theatre producers) and `schools.csv` (acting, theatre and
  film schools). Each has a lists folder with the original copies, the skip record and the refresh
  procedure. `ORGANISATION_FILES` in `collection/sources.py` maps each to its source prefix
  (`co-`, `pr-`, `ve-`, `sc-`).
- **`Organisation.kind` and `Organisation.region`** are new, synced from the CSVs and filterable in
  the admin, so the database answers "every dubbing studio in the North" directly.
- **`collect` column:** a contact's website and whether to collect it are different questions. A
  venue whose site is the town council's homepage, a university homepage, a site whose robots.txt
  refuses us, or a page another source already collects keeps its website with `collect` set to
  `no`.
- **Individuals:** casting directors and agents filed as individuals are kept only when they have
  a professional website. Their emails and phone numbers are never stored; the website is the
  contact.

## Proposed approach
1. Rede de Teatros e Cineteatros (RTCP), the main gap the user named, into a new `venues.csv`.
2. Festivals (theatre and film), the national and Lisbon/Porto houses outside RTCP, and the
   commercial theatre producers.
3. Dubbing studios and voice agencies; casting companies, actors' agencies and casting directors;
   more producers (advertising, animation, production services).
4. Schools into a new `schools.csv`.
5. Funders, and the EU sources from [T-014](T-014-eu-funding-sources.md).
6. Check every website, merge across all files, collect every new source once, and fix what
   breaks.

## Acceptance criteria
- [ ] Every family above has a CSV with a lists README that records the source lists, the skips and
  the refresh steps
- [ ] Every organisation is in the database with a kind and, where known, a region
- [ ] Every new source has been collected once, and the failures are fixed or recorded
- [ ] Tests pass

## Implementation
**2026-10-01.**
- **Lists read:** RTCP (104 venues), the open dataset *Teatro em Portugal: websites e histórico no
  Arquivo.pt* on dados.gov.pt (62 active companies, 95 venues, 51 festivals, 6 higher-education
  entries, published August 2026), Cineguia Portugal (374 profiles in 13 categories: producers,
  production services, agencies, casting directors, agents, animation, film festivals, schools,
  funders), the wikidobragens studio list plus voice agencies, escolasprofissionais.com's Actor
  course, DGES theatre and cinema degrees, and hand-picked venues, producers and funders. The
  details and every skip are in the four lists READMEs.
- **Merging:** 789 candidates were checked (601 sites loaded), matched by name and by website within
  the same file, and folded into existing rows where they matched (235 merges, which added the list
  ID to `lists`). Two problems were found on the way:
  - The first city-to-region table split multi-word town names, so "Vila do Conde" became
    `centre`. It now matches whole names, longest first.
  - A website match across files merged different organisations that share a site (ESMAE and Teatro
    Helena Sá e Costa). Website matching is now limited to the same file.
- **Hand fixes:** duplicates under other names were folded (Formiga Atómica, Varazim, Cães do Mar,
  ASTA = albiASTA, Cendrev), and Cães do Mar and albiASTA got their websites. TNDM moved from
  companies to venues, Buzico to producers, and Chapitô is kept once, as a company. Four festivals
  that Cineguia files as "Individual" (Fantasporto among them) were added back.
- **Code:** `Organisation.kind` and `region` (migration `0005`), shown and filterable in the admin;
  `ORGANISATION_FILES` and `load_organisations(prefix)` replace the per-file loaders; the `collect`
  column; a test that names are unique across all four files and kinds and regions are known. A
  test that created "Teatro Nacional São João" by hand now uses a made-up name, since that venue is
  synced from the CSV.
- **EU sources (T-014)** were added in the same change: `ec-culture`, `perform-europe`,
  `on-the-move`.
