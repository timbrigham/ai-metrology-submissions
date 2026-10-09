# PR #19: Paired-Control Selectivity Test for Non-Measurement

- PR: https://github.com/usnistgov/ai-metrology-submissions/pull/19 (submitter halvrenofviryel / Phionyx; Tim has no connection)
- Reviewer gap (jphall663, 2026-09-15): Scientific Grounding "Partial". Wants "independent or peer-reviewed support if available".
- Status: `comment.md` has had two adversarial rounds (both REVISE, with every finding applied). **Not posted.** It waits for Tim's OK, and Tim posts it himself.

## Evidence
- Defect: in ZeroParadox `tools/verify/batch.py`, `check_ssot` returned `True` when `ssot.json` was absent.
  - Entered the tracked tree in `36a5de5` (2026-08-15).
  - Last buggy commit: `09129065f280a0a8765d5cfb1a28663feb911fe2` (L1015-L1020).
  - Fixed in `28f78173bfe68419d3265753b4b323c35c0b2ca9` (L1122-L1134).
  - Both commits are on public origin/main.
- Re-running the harness with `python -I harness/pair.py <exported tools/verify> harness/fixtures`:
  - before: control True / uncovered False / degenerate **True**
  - after: control True / uncovered False / degenerate False
  - Export each commit with `git archive <sha> tools/verify | tar -x -C <dir>` from C:\Workspace\ZeroParadox.
  - `fixtures/degenerate/` deliberately does not exist.

## Review findings worth remembering
- Never link the ZeroParadox repo root. Its GitHub description ("formal ontology of the bottom element ⊥") reads as grand theory in a NIST thread. Use line permalinks only.
- Always disclose that the evaluator is Tim's own code.
- This is a retrospective known-answer test (the fix landed 09-06 and the PR opened 09-14). Never imply that the procedure found the bug.
- Under the YAML's applied_definition, the fixed gate's bare `False` is "another status", so the case still FAILS. It would be FAIL, not INCONCLUSIVE.
- Call this "independent review" or "replication evidence", never "peer review".
