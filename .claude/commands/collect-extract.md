---
description: Collect new listings from every source, then extract them into draft actions (theater-watcher weekly run, T-010)
---

Run the first half of the Monday routine for **theater-watcher** in one go.

1. **Collect.** Run `uv run python manage.py collect` with a long timeout (it can take over 10
   minutes, because it waits between requests to the same site). When it ends, report in a few
   lines:
   - the total of new and updated listings, and the sources that brought the most;
   - the "blocked by the work network's filter" line, as a count only (those sites are fine and
     come through from another network);
   - every source shown as a real failure, with its error.

   If `collect` itself crashes, stop and report. Don't extract.
2. **Extract.** Follow every instruction in `.claude/commands/extract.md` exactly, as if the
   user had typed `/extract`, until nothing is left.
3. **Report.** End with the extraction totals from `/extract`, then one line pointing to the
   next step: review the drafts in the Django admin (HOWTO step 3).
