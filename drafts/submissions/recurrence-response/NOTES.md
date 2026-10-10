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

## Loop capping (Tim, 2026-10-10: "We implemented loop capping in zeroparadox for a reason")
- R-LOOPCAP (`ZeroParadox/tools/process/review-loop-cap.md`): "The gates will always find something. Stopping is a decision about SEVERITY, not a wait for silence." BEDROCK gets up to 5 rounds and ORDINARY gets 2. The caps are authoritative in `tools/verify/gate_round.py`.
- **The measured reason** (review-gates.md, quoting R-LOOPCAP's cost line): "three of the last four bedrock findings were introduced by the previous round's fix". Iterating is not neutral, because fixes create new defects.
- Also measured, 2026-08-01: "four of the next round's six editorial findings landed in the one file no gate had yet seen", which existed only because it was edited after the gates finished.
- Data: per-round notes in `.claude-local/notes/gate_round*_*.md` and `gate_round.json`. PRIVATE.

## The non-circular outcome measures this suggests
1. **Convergence:** findings per round. Do they fall, or plateau?
2. **Fix-introduced defect share:** of round k+1's findings, the fraction caused by round k's fix. It measures the cost of patching harder, independent of any count-forcing rule.
3. **Shape-change effectiveness:** after a forced change of approach (cap, checker, re-scope), does the failure class recur?

**Reference leads, UNVERIFIED:**
- Śliwerski, Zimmermann & Zeller, "When do changes induce fixes?" (MSR 2005, the SZZ algorithm);
- Yin, Yuan, Zhou, Pasupathy & Bairavasundaram, "How do fixes become bugs?" (ESEC/FSE 2011).
