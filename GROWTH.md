# Growth opportunities

What would make theater-watcher **the** digest every actor in Portugal reads. Ranked by impact.
Analysed 2026-10-01 from the first issue's data.

<!-- Format: a dated "Where we stand" snapshot, then the ranked opportunities table, then the
sequencing. Each opportunity links to the task that works on it once one exists. This file
never holds status (that's TASKS.md) or the reasoning for one piece of work (that's the task
file). Re-rank by adding a new dated snapshot instead of rewriting old ones. -->

## Where we stand (2026-10-01)
- First run: **153 listings collected → 11 actions extracted → 10 in issue #1**.
- Issue #1 had **zero castings** in Teatro, Cinema, Televisão, and Publicidade. The only
  theatre calls found (TNSJ ×2, enCAST ×1) had closed or were closing too soon. The issue was
  filled by 3 workshops, 3 funding calls, 1 voice job, 1 always-open form, and 2 items in
  Últimos dias.
- **The core promise, open castings for film, TV, and advertising, is the gap.** Keywords
  aren't the bottleneck: they only pre-filter 4 of the 16 sources, and an LLM
  ([T-008](tasks/T-008-extraction.md)) judges everything that gets through.
- Constraint that shapes everything: **every call must name who posted it**
  ([T-006](tasks/T-006-traceable-poster.md)). That rules out the anonymous aggregators, where
  most of the advertising volume is.

**Update (2026-10-01, after [T-012](tasks/T-012-film-school-sources.md)):** film schools
don't publish their students' castings on their own sites. Those calls already reach us
through Coffeepaste and enCAST, or stay in Facebook and Instagram groups. So #2 adds no new
sources, and getting more student castings depends on #1 (asking cinema departments to
forward calls to a submission channel). #1 moves up.

## Opportunities, ranked

| # | Opportunity | Why it matters | Effort | Task |
|---|---|---|---|---|
| 1 | **Get calls sent to us: become the place to post** | Most castings never reach a public website: casting directors and producers send them to agencies, or post on Instagram and WhatsApp. A free "Publique a sua audição" form or address for casting directors, producers, theatres, and schools brings in calls no one else has, and it's traceable by design. | Medium (form + outreach) | — |
| 2 | **Film schools and student productions** | ESTC, Lusófona, ESAD, ESMAE, Católica, and others produce dozens of shorts every term, and each one casts actors. It's the fastest way to fill **Cinema**. Mostly unpaid or expenses-only, so they need clear labels. | Low–medium (new sources) | [T-012](tasks/T-012-film-school-sources.md) |
| 3 | **TV and film producers, and DGArtes-funded companies** | TV producers (SP Televisão, Coral, Ukbar, Stopline…) and the 33 funded theatre companies post their own calls and news of upcoming productions. That feeds **Televisão**, **Teatro**, and **No radar**. | Medium (~40 sites, most fit existing adapters) | [T-013](tasks/T-013-producer-and-company-sources.md) |
| 4 | **Speed: the weekly rhythm misses short calls** | Many castings open and close within days (the known gap in [T-003](tasks/T-003-digest-architecture.md) step 2). A short mid-week "Fecha em breve" alert, or a second weekly issue, catches them. Being first is what makes people check *this* email. | Low (pipeline exists) | — |
| 5 | **Trust as the brand** | Fake castings are a known problem (TVI publicly warned about fake *Morangos com Açúcar* castings), and so is paying to apply. "Every call names who posted it, no pay-to-apply, paid or unpaid always stated" is a promise no aggregator makes. Make it visible in every issue. | Low (wording + design) | — |
| 6 | **Relevance for each reader** | Region, age, gender, and pillar are already stored on every action. Letting readers choose ("só Norte", "só Dobragem") keeps the email relevant as it grows. | Medium (needs subscriber management) | — |
| 7 | **Distribution** | Today there's one recipient. Growth means proper sign-up (an EU email provider with double opt-in, the "later" column of T-003), a public archive of past issues to share, and partners who forward it: Fundação GDA, Plateia, the CENA-STE union, acting schools. | Medium–high | — |
| 8 | **Measure it** | Clicks per opportunity and per pillar, and readers' "did you apply?" answers, show which sources earn their place. | Low–medium | — |

## Sequencing
1. **Now:** #2 and #3. They're cheap with the collectors and `/extract` already built, and
   they target the empty pillars directly.
2. **Then:** #1, a submission channel plus outreach to the 10–20 main casting directors and
   producers. That's the long-term edge, because those calls aren't online anywhere else.
3. **Before inviting other readers:** #5, so the trust promise is visible, and #7, so sign-up
   and GDPR are handled. Growing the audience before the castings are there would bring
   readers to a thin email.

**Tradeoff to decide deliberately:** #1 and #7 turn a personal tool into a small service,
with GDPR obligations, outreach, and maintenance, and probably a hosted server instead of the
user's PC.
