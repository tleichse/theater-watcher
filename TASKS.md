# Tasks

The only place a task's status lives. Everything else about a task is in its own file.

**Lifecycle:** `new` (promoted, not started) → `in-progress` → `done`. Two more states:
`blocked` (waiting on an answer or on something outside the repo; the task file says what) and
`dropped` (decided against; the task file says why).

**IDs:** use the next unused number, zero-padded (`T-001`). If two branches take the same ID, the
one merged later renumbers its task.

| ID | Title | Status | Area | File |
|---|---|---|---|---|
| T-001 | Bootstrap the documentation system | done | repo | [T-001](tasks/T-001-bootstrap-doc-system.md) |
| T-002 | Research validated sources of casting opportunities in Portugal | done | research | [T-002](tasks/T-002-casting-sources-research.md) |
| T-003 | Digest architecture: actions data model and email structure | done | architecture | [T-003](tasks/T-003-digest-architecture.md) |
| T-004 | Project skeleton and directory layout | done | repo | [T-004](tasks/T-004-project-skeleton.md) |
| T-005 | Data models and review admin | done | backend | [T-005](tasks/T-005-models-and-review-admin.md) |
| T-006 | Require a traceable poster on every shared action | done | backend | [T-006](tasks/T-006-traceable-poster.md) |
| T-007 | Collectors for every source on the final list | done | collection | [T-007](tasks/T-007-collectors.md) |
| T-008 | Extraction: raw listings to draft actions via Claude Code | done | collection | [T-008](tasks/T-008-extraction.md) |
| T-009 | Digest builder: selection rules and email rendering | done | digest | [T-009](tasks/T-009-digest-builder.md) |
| T-010 | Send through Gmail and the weekly run command | blocked | digest | [T-010](tasks/T-010-send-and-weekly-run.md) |
| T-011 | Email visual design: brief for Claude Design | blocked | design | [T-011](tasks/T-011-email-design-brief.md) |
