# School lists

Where the acting, theatre and film schools in [`../schools.csv`](../schools.csv) come from, and how to
look for new ones. It works like the other lists folders: a copy of each original list and a record
of what was skipped. To run it again, open Claude Code and say: *"Let's look for new schools,
following `collection/school_lists/README.md`."*

<!-- Format: "How to look for new schools" is the procedure; edit it when a step changes. Below it,
one `##` section per list, keyed by the ID used in the CSV's `lists` column. A refresh adds a new
section and never rewrites an old one; a later change is added as a dated note. -->

## `schools.csv` columns
Same as [`producers.csv`](../producer_lists/README.md#producerscsv-columns), with `kind` always
`school`. `collect` is `no` for a university's main homepage (its notices are admissions and
tenders) and for a school whose site another source already collects (ACE's site is collected as
the company Teatro do Bolhão).

## Why schools are contacts, not mainly sources
[T-012](../../tasks/T-012-film-school-sources.md) found that schools don't post their students'
castings on their own sites; those calls arrive through Coffeepaste and enCAST. Schools are here
because they're the people to contact (GROWTH #1: asking cinema and theatre departments to forward
calls), and because independent schools post workshops, which are `training` actions.

## How to look for new schools
1. Professional schools: the *Intérprete / Ator / Atriz* course page on escolasprofissionais.com
   lists every school that runs it. Higher education: the DGES course search for *Teatro* and
   *Cinema*. Independent schools: web search plus Cineguia's *Escola de Teatro* category.
2. Find and check each website, merge with all four CSVs by name, write the rows, run the tests,
   collect the new `sc-` sources.

## `manual-2026`
Read on 2026-10-01.
- **Professional schools with the Actor course**
  ([escolasprofissionais.com](https://www.escolasprofissionais.com/cursos/interprete-ator-atriz/)):
  ACE, Art'J (Jobra), Escola Profissional Nicolau Breyner (NB Academia), ETIC, EPABI, EPTC (Cascais),
  Balleteatro, EPATV, ETPM. The Lousã school's site wasn't found. NB Academia's robots.txt forbids
  crawling (T-002), so its `collect` is `no`.
- **Higher education:** ESTC, ESMAE, ESAD.CR, Universidade de Évora, Universidade do Minho, Lusófona,
  Católica Porto (Escola das Artes), ESCS, UBI, ESAP, ESEC. These are the ten film schools from T-012
  plus the theatre degrees on DGES.
- **Independent schools:** ACT, Conservatório Vocare, EVOÉ, Restart, World Academy, Lugar Presente.
  Chapitô is kept once, as a company in `companies.csv`.

## `arquivo-ensino`
- **What:** the higher-education and research sheet of the *Teatro em Portugal* open dataset (6
  rows). See the [venue lists](../venue_lists/README.md#arquivo-espacos-arquivo-festivais).
- **Copy:** [`arquivo-ensino.csv`](arquivo-ensino.csv). Read on 2026-10-01.
- Skipped as stale pages: the Centro de Dramaturgia Contemporânea page (2019), Évora's Artes Cénicas
  department page (2007, the current course page is used instead), and ESAD Leiria's old page (2019;
  ESAD.CR's current site is used).

## Cineguia (`cineguia`)
Three entries from Cineguia's *Escola de Teatro* category. Its *Formador área Audiovisual* category
(25 entries) was skipped: individual technical trainers (editing, camera, sound), not acting.
