# Working with Claude on theater-watcher

This file is loaded automatically every session. Read `README.md` next; it's the map of the
project. Everything else below is how the repo's documentation system works and when to use
each part. The markdown files in this repo are the project's memory. A chat session doesn't
survive between conversations, but the repository does.

## The documentation system

Each file has exactly one job, and no fact lives in two places: if a second file needs a fact,
it links to it instead of copying it. Each file's own internal format is described in a short
preamble at the top of that file, so read the preamble before you edit the file.

| File | Its one job | When to touch it |
|---|---|---|
| `README.md` (recursive: any major folder with several sub-areas gets its own) | What this is, how to run it, and a map to deeper docs | Read it first. Update it when the project's shape changes. |
| `HOWTO.md` | Operator steps for setup and the weekly run (collect, extract, review, build, send) | Update a step in the same change that alters a command or admin screen it describes |
| `GOTCHAS.md` | Pitfalls already hit, so nobody hits them again | Scan the topic headings before touching an area. Add or amend an entry, in the same change, whenever something non-obvious costs time. |
| `IDEAS.md` | Raw asks, kept close to how they were said, grouped by date | Append whenever someone asks for a change to the project, before any work starts |
| `TASKS.md` | Thin index: ID, title, status, area, link | The only place a task's **status** lives |
| `tasks/T-XXX-slug.md` | Durable record of one unit of work: context, decisions, plan, what actually happened | Create it at promotion (copy `tasks/_TEMPLATE.md`) and keep it current while the work happens |
| `CHANGELOG.md` | Outward-facing history of what shipped | Add it in the same change that flips a task to `done` |

## How work flows

1. **Ask**: append it to `IDEAS.md` under today's date, close to how it was said.
2. **Promote** (when the work is picked up): take the next ID, create the task file (ask quoted,
   repo context, open questions, proposed approach, acceptance criteria), add a row to
   `TASKS.md`, and append `→ T-XXX` to the inbox entry.
3. **Work**: resolve open questions in place (strike them through and add the answer). The
   *Implementation* section records what was actually built, including where it diverged from
   the plan. Never edit *Proposed approach* to make it look like it matched reality.
4. **Done**: check off the acceptance criteria, flip the status in `TASKS.md`, and add one
   `CHANGELOG.md` bullet, all in the same commit.

A later change to an ask that was already promoted gets a **new** dated inbox entry that ends
with `→ folded into T-XXX`. Old entries are never rewritten.

### What skips the flow
Use the flow only for things a future session or another person would otherwise have to
rediscover. These skip it: questions and explanations, typo or doc fixes, and refactors with no
change in behavior. A fix that users will notice but that is too small to need a task still gets
a changelog bullet. Anything that only matters until the current task ends goes in the
in-session todo list, not in a file.

### Where knowledge goes
Project knowledge (pitfalls, decisions, conventions) goes in these repo files, **not** in
Claude's private per-user memory. The repo is shared with other people and other machines, and
private memory is not. Private memory is only for things about how the user likes to work.

## Design rules
- **One fact, one home.** Status lives in `TASKS.md`. Reasoning and history live in the task
  file. The original ask lives in `IDEAS.md`.
- **Indexes stay thin.** If an edit to an index is growing past a line, that text belongs in the
  linked file instead.
- **Logs are append-only in spirit.** Inbox and gotcha entries are added to or amended, never
  deleted. When a gotcha no longer applies, mark it obsolete instead of removing it.
- **State the why.** Write "this broke because X, found while doing Y", not a bare fix, so a
  reader can judge whether it applies to their situation.
- **Established patterns are the single source of truth.** If a style guide or catalog of
  patterns exists, check it before inventing something new, and update it in the same change
  when a new pattern is deliberately added. Ask before adding a new visual or structural
  pattern when an established one should be used instead.

## Language
- **Anything the end users see** (the digest email and any UI) is written in **European
  Portuguese (pt-PT)**. Never Brazilian Portuguese: write *equipa*, *ecrã*, *telemóvel*, and
  *a fazer*, not *time*, *tela*, *celular*, or *fazendo*.
- **Everything else is in English**: code, identifiers, comments, commit messages, and the docs
  in this repo, including `CHANGELOG.md`.

## Code conventions
- Every unit of the same kind (module, package, feature area) follows the same internal shape.
  Match what existing units do; don't invent a new layout without precedent.
- Put new logic where the existing pattern already puts equivalent logic. Don't move it
  because another arrangement looks cleaner.
- Match existing naming and interfaces so new code can't be told apart from what's already
  there.
- Default to no code comments unless one explains a non-obvious *why*.

## Collaboration
- For exploratory or opinion questions, give a short recommendation with the main tradeoff.
  Don't implement until the user agrees.
- Don't add error handling, abstractions, or scope beyond what's asked. No speculative
  future-proofing.
- Confirm before destructive or hard-to-reverse actions (force-push, `reset --hard`, deleting
  branches or files, amending pushed commits). Approving one of these doesn't approve the next.
