# Venue and festival lists

Where the theatres, venues, festivals and theatre producers in [`../venues.csv`](../venues.csv) come
from, and how to look for new ones. It works like [`../company_lists/`](../company_lists/README.md):
this folder keeps a copy of each original list and a record of what was skipped. To run it again,
open Claude Code and say: *"Let's look for new venues and festivals, following
`collection/venue_lists/README.md`."*

<!-- Format: "How to look for new venues" is the procedure; edit it when a step changes. Below it,
one `##` section per list, keyed by the ID used in the CSV's `lists` column, giving the publisher,
the original URL, the local copy, the date it was read, and what was skipped and why. A refresh adds
a new section with a new ID and never rewrites an old one; a later change is added as a dated
note. -->

## `venues.csv` columns
Same as [`producers.csv`](../producer_lists/README.md#producerscsv-columns): `name`, `kind`
(`venue`, `festival`, or `producer` for commercial theatre producers such as UAU), `region`,
`website`, `collect`, `lists`, `last_active`.

- `collect` is `no` when the website is worth keeping as a contact but shouldn't be collected: a
  town council's homepage (municipal tenders and notices would flood `/extract`), an agenda site, a
  page on a site another source already collects (a festival hosted on its company's site, the
  national theatres, which have hand-configured sources in `sources.py`).
- `last_active` is 2026 for everything on the current RTCP list (being credentialled is current
  activity), otherwise the latest year on the website.

## How to look for new venues and festivals
1. **Re-read the lists.** RTCP: page through `rtcp.pt/pt/espacos/?page=N`, then open each venue for
   its operator, NUTS III region and website, one request a second. The open-data lists are CSV
   downloads from dados.gov.pt.
2. **Check each website** (loads, latest year, final address after redirects).
3. **Merge** with all four CSVs by name and by website (within the same file), so one venue on
   several lists is one row; add the list ID to `lists` instead.
4. **Skip** music-only or dance-only houses, and anything with nothing after 2019 unless it's on the
   current RTCP list. Set `collect` to `no` per the rule above.
5. **Write the rows**, run `uv run python manage.py test` (it checks names are unique across all
   files), then `collect` the new `ve-` sources and record the yield in the active task file.

## `rtcp-2026`
- **What:** DGArtes, *Rede de Teatros e Cineteatros Portugueses*: 104 credentialled venues
  (Amarante joined in August 2026), each with its operating entity (usually the town council), NUTS
  III region and website.
- **Original:** [rtcp.pt/pt/espacos](https://www.rtcp.pt/pt/espacos/). The programmers' contact list
  is a PDF linked from the same site; it wasn't stored, because it lists people.
- **Copy:** [`rtcp-2026.json`](rtcp-2026.json). Read on 2026-10-01.
- NUTS III regions were mapped to ours: Grande Lisboa, Península de Setúbal, Oeste, Lezíria do Tejo,
  Médio Tejo and the Centro subregions are `centre`; Alentejo and Algarve are `south`.
- 73 of the venues' websites are town-council pages, kept with `collect` set to `no`.

## `arquivo-espacos`, `arquivo-festivais`
- **What:** *Teatro em Portugal: websites e histórico no Arquivo.pt*, an open dataset published
  for web preservation (August 2026): 95 theatre venues and 51 theatre festivals with websites.
  Its companies and higher-education sheets are recorded in the
  [company](../company_lists/README.md) and [school](../school_lists/README.md) lists.
- **Original:**
  [dados.gov.pt/datasets/teatro-em-portugal-websites-e-historico-no-arquivo-pt](https://dados.gov.pt/datasets/teatro-em-portugal-websites-e-historico-no-arquivo-pt)
- **Copies:** [`arquivo-espacos.csv`](arquivo-espacos.csv), [`arquivo-festivais.csv`](arquivo-festivais.csv).
  Read on 2026-10-01.
- 94 of the venues were already on the RTCP list. 48 festivals were added. Skipped as stale:
  Sementes (2017), FESTEA (2011). Some festivals have only a Facebook page or an archived link,
  so they're kept without a website.

## Film festivals (`cineguia`)
32 film festivals come from Cineguia Portugal's *Festivais de Cinema* category (see the
[producer lists](../producer_lists/README.md#cineguia)). Four of them (Fantasporto, Finisterra,
Shortcutz Lisboa, and the producer Cinekenta) are filed there as "Individual" and were first
dropped by the rule for individuals, then added back by hand.

## `manual-2026`
Venues and producers that no list covers, found by hand on 2026-10-01: the national theatres (TNDM
II, TNSJ, São Luiz, kept as contacts with `collect` set to `no`, since they're already sources),
Lisbon's main houses (Teatro do Bairro Alto, Maria Matos, CCB, Culturgest, Trindade, Tivoli, Villaret,
LU.CA, Casa do Artista, Cinema São Jorge, Teatro do Bairro), Porto's Batalha and Sá da Bandeira, and
the commercial theatre producers (UAU, Força de Produção, Filipe La Féria at the Politeama).
Skipped: Teatro Camões (the national ballet's house, dance), Teatro Nacional de São Carlos (opera),
Teatro Carlos Alberto (part of TNSJ, same site), Yellow Star Company (a "coming soon" page).

**Not looked at yet:** municipal cultural centres outside RTCP, cinema clubs (*cineclubes*), and
amateur theatre festivals beyond those in the open dataset.
