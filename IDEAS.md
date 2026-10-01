# Ideas inbox

Raw asks, captured close to verbatim so nothing said in passing gets lost.

<!-- Format: one `##` heading per date (YYYY-MM-DD), with the newest date at the bottom. Entries are
appended in the order they were said. Never rewrite an entry. When one is promoted, append
` → [T-XXX](tasks/T-XXX-slug.md)`. If an ask that was already promoted changes, add a new entry under
today's date that ends with `→ folded into T-XXX`. -->

## 2026-09-30

- "Start up the repository considering claude-working-style. First, try to find any pitfalls and
  optimization opportunities for the workflow. Then, apply it"
  → [T-001](tasks/T-001-bootstrap-doc-system.md)
- "the idea behind the the theatre watcher is to gather all the oportuinities for working in
  Theatre, Cinema (movies / series / documentaries), TV (soap operas), but also for marketing
  sketches (TV and radio) and dubbing  in Portugal. The idea is to have a weekly digest (an
  email) sent to people with info on new opportungities for castings in the pillars dfined
  (Theatre, Cinema, TV, Marketing and Dubbing). We can gather info from validated sources in
  Portugal. We first need to make a complete search on that."
  → [T-002](tasks/T-002-casting-sources-research.md)
- "some other sources are alse dgartes and maybe also gepac" → folded into
  [T-002](tasks/T-002-casting-sources-research.md)
- "before committing, i want to think about the architecture of this dgiest. I think we will
  need a database of so called "actions" that define the entries that I want to share with the
  people that will get the digest. What are the main info that is importatn? One thing that i
  have in mind is that we need to now what opportuinites were already shared, when, when were
  they published and when do they end / until when it is necessary to do something about it
  (for example, an application). As i said, i want to format an email in jinja with an artistic
  and colorful design following a design system (I will create that using claude design), and
  only the actions that are still open will appear in the digest. What is the strucutre you
  recommend for this digest? I want to have the pillars i talked about in separate sections of
  the email. Actions cna also be training possibilities, free or paid. It would be important to
  also gather that info. What do you recommend more? et's think in steaps. ask question for
  validation whenever needed."
  → [T-003](tasks/T-003-digest-architecture.md). Finding sources for training is folded into
  [T-002](tasks/T-002-casting-sources-research.md).

## 2026-10-01

- "consider T-003. What are the next steps? Can we just figure rapidly a robust and simple
  directory management strucutre and start with implementation?"
  → [T-004](tasks/T-004-project-skeleton.md)
- Answers to T-002's open points: "1. yes 2. no, just use it 3. Find them. 4. Let'sgo!" (approve
  link-out; don't ask Coffeepaste/enCAST; find Marketing and Dubbing sources; research training
  sources) → folded into [T-002](tasks/T-002-casting-sources-research.md)
- "let's go. As for training, some studios as "VS Digital Media" in lisbon are great for
  training. Can we find something there? It would be great if we could categorize the
  opportunities by geography (north, center (including Lisbon), south, or national)"
  → [T-005](tasks/T-005-models-and-review-admin.md) for the geography field; the training
  lead is folded into [T-002](tasks/T-002-casting-sources-research.md)
- "one thing that i really need is that the sources of the action have to be traceable. You
  have to know who is posting." → [T-006](tasks/T-006-traceable-poster.md); it also settles
  the becasting question, folded into [T-002](tasks/T-002-casting-sources-research.md)
- "how do we make a first run now? ist here something missing? Do we have to work on more
  sources?" then "let's do all sources we have at the moment. I have to show value from the
  very beginning. Let's create the necessary tasks-"
  → [T-007](tasks/T-007-collectors.md), [T-008](tasks/T-008-extraction.md),
  [T-009](tasks/T-009-digest-builder.md), [T-010](tasks/T-010-send-and-weekly-run.md)
- "would it be important to include also sources from the portuguese main tv channels, through
  their corresponding film companies and so on?" Then, asked whether to do it now or after the
  first issue: "after". Not promoted yet. When it's picked up, check ICA's "Projetos em Curso"
  and "Vistos de rodagem" pages too (see [T-008](tasks/T-008-extraction.md)).
  → [T-013](tasks/T-013-producer-and-company-sources.md)
- Answers to T-007's open points: "2. twice a week 3. yes, public" (collect twice a week;
  the GitHub repo is public, so its URL works as the collector's contact) → folded into
  [T-007](tasks/T-007-collectors.md) and [T-003](tasks/T-003-digest-architecture.md)
- "go on with the task. I just tried the creating the html and it pretty good already. How do you
  suggest apporaching the design question, to get something that i like best?" then "Do the
  brief for the chat with Claude Design, and also build what is needed to do the link with the
  email account." → [T-011](tasks/T-011-email-design-brief.md) for the brief; the email link
  is [T-010](tasks/T-010-send-and-weekly-run.md)
- Chose sending through the Gmail API (quoting the proposed option), asked "would it have
  associated costs?", then "let's work!" → folded into [T-010](tasks/T-010-send-and-weekly-run.md)
- "is the extraction work being done only via keywords? I want to have an LLM do that. Can't
  claude do it in a weekly action?" then "for these sources widen the keywords to look for.
  Regarding the scheduled action, do i need to have the PC open?" → keywords folded into
  [T-007](tasks/T-007-collectors.md); the scheduled weekly run is
  [T-010](tasks/T-010-send-and-weekly-run.md)'s `run_week`
- "Find the biggest opportunities for growth for this digest? Is it in terms of sources?
  Keywords? I want ot make this digest the one that everyone goes to." then "write an md with
  these opportunities, and start with 1. from yout recommendation." → [GROWTH.md](GROWTH.md);
  recommendation 1 → [T-012](tasks/T-012-film-school-sources.md) and
  [T-013](tasks/T-013-producer-and-company-sources.md)
- "i would suggest that you also look for the remaining sources and also look for actors and
  theat companies that also may be looking for actors. One may be astro fingido, for example. I
  want them from all around the country. Is there any list of theatre companies?" → folded into
  [T-013](tasks/T-013-producer-and-company-sources.md)
- "i mean actors' own collectives. let's go. go ahead with the coimbra list. I would like to save
  the dgartes and coimbra sources so that i can check them later and also update the list."
  → folded into [T-013](tasks/T-013-producer-and-company-sources.md)
- "yes, do that. All companies that you found and have contents from the last 2 years are
  validated, you can consider that." (go through DGArtes *Apoio a Projetos*; "validated" now
  means recent activity, not only DGArtes funding) → folded into
  [T-013](tasks/T-013-producer-and-company-sources.md)
- "yes" (to making `site_watch` skip a followed page that fails, so OUTRO's members-only page
  doesn't fail the whole site) → folded into [T-013](tasks/T-013-producer-and-company-sources.md)
