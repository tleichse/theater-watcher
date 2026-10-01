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
| T-002 | Research validated sources of casting opportunities in Portugal | in-progress | research | [T-002](tasks/T-002-casting-sources-research.md) |
| T-003 | Digest architecture: actions data model and email structure | done | architecture | [T-003](tasks/T-003-digest-architecture.md) |
| T-004 | Project skeleton and directory layout | done | repo | [T-004](tasks/T-004-project-skeleton.md) |
| T-005 | Data models and review admin | done | backend | [T-005](tasks/T-005-models-and-review-admin.md) |
