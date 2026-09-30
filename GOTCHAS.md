# Gotchas

Pitfalls we've already hit, so we don't rediscover them. Check the topic you're about to touch.

<!-- Format: entries are grouped under a `##` heading per topic (area of code or kind of problem),
not by date. Each entry is a `###` heading with a symptom-style title, then what goes wrong
and why, then a **Fix:** line. Where a mistake happened again, add a **Recurred:** line naming
each date and task. Entries are only added or amended, never deleted. If one stops applying,
add **Obsolete since YYYY-MM-DD:** with the reason. -->

## Repository & paths

### Project name is spelled two ways
The GitHub repo and this folder are `theater-watcher` (American spelling), but the local parent
folder is `theatre-watcher` (British spelling). If you type a path from memory, you'll get one of
them wrong. Found while bootstrapping the repo ([T-001](tasks/T-001-bootstrap-doc-system.md)).
**Fix:** use `theater-watcher` everywhere inside the project, in code, docs, and package names.
Copy absolute paths from the environment instead of retyping them.
