# Candidate: recurrence response (Tim chose this on 2026-10-10)

**Status:** idea. Overlap and reference research is running.

## The idea (Tim)
A good AI engine should have rules that challenge the SHAPE of how it is measuring or working when the same failure recurs, rather than patching harder. ZeroParadox already does this:
- R-RECUR escalates by count: 1st = instance, 2nd = class plus detector, 3rd = the trigger is wrong, 4th+ = build a checker;
- R-NOCONV: "a check that misses 3x changes SHAPE";
- R-REVALIDATE: "a sentence fixed 3x is a claim defect".
The containment redesign of 2026-10-10 was this rule firing live.

## Data that exists (read-only check, 2026-10-10)
- `ZeroParadox/tools/verify/selfheal.py` (public). It counts recurring process and agent-behaviour shapes, with THRESHOLD = 3. "Suggests; never corrects."
- `ZeroParadox/.claude-local/DEFECTS.md` (1.6 MB, ~1,335 rows) and `DEFECT_CLASSES.md` (~149 headings) are **PRIVATE**.
  - selfheal.py's own comment: publishing them needs a preamble and both adversary gates.
  - The records are prose-heavy, not structured.
- Relevant class names: DC-26 "THE FIXER WROTE THE FIX'S ONLY CONTROL"; DC-27 "THE METRIC IS SATISFIED AND THE PROPERTY IS UNTOUCHED".

## The validity trap, raised up front (per the new memory rule)
- ZeroParadox's rules FORCE a shape change at counts 2, 3 and 4. Measuring that its agents change shape at those counts measures rule compliance: true by construction.
- A non-circular candidate measures the OUTCOME instead: after a patch versus after a shape change, did the failure recur, and how soon?
- Or it measures agents WITHOUT such rules: do they change shape unprompted?
- The decision waits on the research.
