# T-001: Bootstrap the documentation system

**Origin:** [IDEAS.md, 2026-09-30](../IDEAS.md#2026-09-30). Status and area are in [TASKS.md](../TASKS.md).

## Original ask
> "Start up the repository considering claude-working-style. First, try to find any pitfalls and
> optimization opportunities for the workflow. Then, apply it"

## Repo context
- The repo had one commit: a `README.md` containing only `# theater-watcher`, with no trailing
  newline. There was no code and no stack chosen yet.
- `claude-working-style-template.md` (untracked) is the source template. It describes seven
  kinds of file: orientation README, pitfalls log, root instructions, idea inbox, task index,
  task files, and changelog.
- The remote is `github.com/tleichse/theater-watcher`. The local parent folder is spelled
  `theatre-watcher` (see [GOTCHAS](../GOTCHAS.md#project-name-is-spelled-two-ways)).
- Windows, with `core.autocrlf=true`.

## Open questions
- ~~What does theater-watcher actually do?~~ **Answer (2026-09-30):** a weekly email digest of
  casting opportunities in Portugal across five pillars. Written into `README.md`. The
  follow-up work is [T-002](T-002-casting-sources-research.md).
- ~~Should the template file be kept once it's applied?~~ **Answer (2026-09-30):** nothing is
  deleted without confirmation. Its content now lives in `CLAUDE.md` and in the file preambles,
  so keeping it would give those facts a second home. Deletion is recommended but waits for the
  user. **Update (2026-09-30):** the user confirmed it, and the file was deleted.

## Deep dive: pitfalls and optimizations found in the template

| # | Issue | Type | Resolution |
|---|---|---|---|
| 1 | The task-file header holds **status**, and so does the index. That breaks the template's own "one fact, one home" rule, and the two copies will drift. | Pitfall | The header has only the origin link and points to `TASKS.md` for status and area. |
| 2 | Only `CLAUDE.md` is loaded automatically. The other files are only read if something says *when* to read them. Without explicit triggers, the inbox and gotchas stop being used. | Pitfall | `CLAUDE.md` has a "When to touch it" column and a numbered flow with concrete triggers. |
| 3 | Pasting the whole template into `CLAUDE.md` costs about 3k tokens every session, mostly on format specs that only matter when a given file is edited. | Optimization | Each format spec lives in a short preamble at the top of the file it governs, which is read exactly when that file is touched. `CLAUDE.md` keeps only the map, the flow, and the rules. |
| 4 | The full inbox → task → index → changelog ceremony for every small request adds friction that tends to kill the system. | Pitfall | Added an explicit "What skips the flow" rule. Small user-visible fixes still get a changelog bullet. |
| 5 | The changelog is organized by release, but the project has no versioning. | Pitfall | Headings are dated until versions exist, then switch to `vX.Y.Z (date)`. |
| 6 | Gotchas "never deleted" means entries go stale and mislead once a tool or library changes. | Pitfall | Obsolete entries are marked `Obsolete since <date>` instead of being deleted. |
| 7 | Claude also has private per-user auto-memory, which competes with the repo files as a place to put project knowledge. Anything written there never reaches collaborators. | Pitfall | Rule: project knowledge goes in the repo. Private memory is only for how the user likes to work. |
| 8 | Two branches promoting at once can take the same task ID. | Pitfall (minor) | The branch merged later renumbers its task (noted in the `TASKS.md` preamble). |
| 9 | The lifecycle states weren't defined, so there was no way to record "we decided not to" or "waiting on someone". | Gap | Defined `new / in-progress / blocked / done / dropped`. |
| 10 | A task file template didn't exist, so every task file would be structured from memory. | Optimization | Added `tasks/_TEMPLATE.md`. |

Considered and rejected: a SessionStart hook that prints `GOTCHAS.md`. It isn't needed while the
file is small, and adding it would be speculative.

## Proposed approach
1. Write a condensed `CLAUDE.md` with the map, triggers, flow, and rules.
2. Rewrite `README.md` as an orientation doc with a map.
3. Create `GOTCHAS.md`, `IDEAS.md`, `TASKS.md`, `tasks/_TEMPLATE.md`, and `CHANGELOG.md`, each with
   a format preamble.
4. Dogfood the system: log this request as the first inbox entry, promote it to T-001, and
   finish it with a changelog entry.

## Acceptance criteria
- [x] Every template role has a file, and each file's format is documented once, in that file.
- [x] No fact is duplicated across files (status only in the index).
- [x] `CLAUDE.md` says when each file must be read or updated.
- [x] T-001 went through the full flow: inbox → task → index → changelog.

## Implementation
Built as proposed. Added one gotcha found along the way: the project name is spelled two ways.
The README's "what this is" line is still an open question for the user.
