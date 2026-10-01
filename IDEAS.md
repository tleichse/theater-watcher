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
- Answers to T-007's open points: "2. twice a week 3. yes, public" (collect twice a week;
  the GitHub repo is public, so its URL works as the collector's contact) → folded into
  [T-007](tasks/T-007-collectors.md) and [T-003](tasks/T-003-digest-architecture.md)
