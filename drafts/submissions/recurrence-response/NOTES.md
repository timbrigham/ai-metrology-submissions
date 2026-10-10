# Candidate: recurrence response (Tim chose this on 2026-10-10)

**Status:** PARKED (2026-10-10). Design v2 and the references are done. It needs an example (a script over public agent trajectories, with a declared taxonomy and blind labelling) before a YAML is worth writing.

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

## Research results (2026-10-10). Starred quotes checked by metrology in the extracted text
**Overlap:**
- No SAME entry in the catalogue (147 entries) or in the open PRs. Weakly adjacent: Post-deployment Feedback, #22 Judge Health.
- ⚠ **Closest prior art, a preprint:** MIRAGE-Bench (Zhang et al., arXiv 2507.21017). ★"extract contextual snapshots at the third repetition", to assess whether the agent adjusts. It scores changes of degree (different parameters) as success. Cite it for candour.

**References (peer-reviewed):**
1. ★ Bouzenia, I. & Pradel, M., "Understanding Software Engineering Agents: A Study of Thought-Action-Result Trajectories," ASE 2025. arXiv 2506.18824; DOI unverified.
   - The degree/kind labels: Repetition = ★"The same action is taken again without modification with the same parameters (syntactically or semantically)"; Refinement = improves or extends; Divergence = ★"The action does not follow naturally from the previous one."
2. ★ Yang et al., "SWE-agent," NeurIPS 2024.
   - Recovery conditioned on recurrence: 90.5% eventual success for any edit, ★"This probability drops off to 57.2% after a single failed edit."

**Supporting:**
- Reflexion (NeurIPS 2023): its trigger is the same action and response for more than 3 cycles.
- AgentBench (ICLR 2024): repetition via Rouge-L.
- MAST / Cemri et al. (NeurIPS 2025 D&B): FM-1.3 step repetition, 15.7% of failures, kappa 0.88.
- Huang et al. (ICLR 2024): self-correction gains vanish without oracle labels. This is a validity warning.
- ★ Gu, Barr, Hamilton & Su, "Has the bug really been fixed?" (ICSE 2010, DOI 10.1145/1806799.1806812): "bad fixes comprise as much as 9% of all bugs". It supports the outcome arm.

## Design v1 (forced by the validity findings)
- **Rename:** "Repeated-Failure Adaptation", for agent systems (model plus scaffold).
- **Same failure** = the same ENVIRONMENT-emitted signature (check ID plus normalised error class), with no success on that check in between. Never the agent's or the designer's label.
- **Shape change** = a move to a different category in a CLOSED action taxonomy fixed before any data is seen: retry same locus / edit different locus / change the check / gather information / re-scope-ask-escalate / abandon. The same category with new parameters counts as degree. Labels are assigned blind to the recurrence count, with kappa reported, or by an LLM judge calibrated against humans.
- **Report:**
  1. the hazard P(kind change | k-th recurrence), and the median k;
  2. the LIFT over the kind-change rate on steps with no recurrence. Without it, a thrashing agent scores best;
  3. the **EFFECTIVENESS ARM**, which no rule can force: P(the same signature recurs within N steps | kind change) versus | degree change.
- **Data:** THIRD-PARTY public trajectories (SWE-agent trajectories, MAST-Data with 1,600+ traces, AgentBench) rather than ZeroParadox's private, curated DEFECTS.md. This fixes both "who chose the set" and the private-data problem.
- **ZeroParadox's role:** an illustration of the "rules on" condition only (R-RECUR, R-NOCONV, R-LOOPCAP). Never validating evidence. A rules-on versus rules-off ablation would measure the rule's effect.
- Loop-cap data (fix-introduced findings per round) stays a possible illustration of the effectiveness arm.

## v2 change (Tim, 2026-10-10): "change of shape" is implementation-specific
Tim: "change of shape" has to be "specific to the implementation ... specific to the line of thought being protected."

So there is no universal closed taxonomy. The method requires each implementation to DECLARE its own approach taxonomy, and the YAML specifies the declaration rules, not the categories. Examples:
- coding agent: retry same locus / different locus / change the test / gather information / escalate;
- proof work: tactic tweak / restructure the lemma / change the statement / prove a helper;
- prose claims (R-REVALIDATE's own list): redraft / measure the claim / restate as conjecture / delete.

**Declaration rules:**
- fixed BEFORE data is seen and published with the results;
- each category marked as degree or kind for that domain;
- labels assigned blind to the recurrence count, with agreement (kappa) reported.

**Validity:** an implementer-declared taxonomy reopens "who chose the set". The EFFECTIVENESS ARM audits it. If "kind" changes do not reduce recurrence of the same signature more than "degree" changes, the declared taxonomy is not capturing shape, and the result must report that. The outcome validates the definition, so a taxonomy cannot be chosen to flatter the agent.

## Data-source audit (metrology, read-only, 2026-10-10)
| source | span | session id | curated? | notes |
|---|---|---|---|---|
| MCP `http_calls.jsonl*` (gitRobot / sjv / verdictLedger) | ~28 h / ~11 d / ~9.5 h | yes | no | ROTATES BY DESIGN: 5 MB × 5 + current, oldest deleted (`mcpcommon/calllog.py:55-56`; "a rotating file cannot carry a claim about the past"). Raise `ZPLOG_MAX_BYTES` to keep more |
| gitRobot `git_ops.jsonl` | 2026-08-22 → now | NO | no | append-only. (Earlier said "test traffic mixed in": WRONG, those are real lane-worktree operations; see guard-coverage NOTES) |
| ZeroParadox `.claude-local/autobiography/` | 2026-06-01 → 10-08 | yes | **YES**: 13 saved sessions | selection bias ("who chose the set") |
| Claude Code `~/.claude/projects/C--Workspace-ZeroParadox/` | 2026-09-09 → 10-09 | yes | no: 43 sessions + 1,720 subagent transcripts, 2.6 GB | **only 30 days, matching Claude Code's default `cleanupPeriodDays`**. History is deleted daily unless that setting is raised |

## First count on the autobiography transcripts (proxy signature = tool + normalised first line of the error)
- 25 files, 13 sessions, 12,354 tool calls, 438 errored results, 313 "recurrences". Zero identical retries.
- ⚠ **The signature was too coarse:** "Exit code N" is 305 of 438 errors (PowerShell 245, Bash 60). Most "recurrences" were just "some command failed again", so the late-recurrence counts are an artifact.
- The meaningful environment signatures are the specific ones:
  - "String to replace not found in file" (25);
  - "BLOCKED: this command invokes git" (15);
  - "BLOCKED: ... runs a checker under tools/verify and truncates" (22).
  The BLOCKED ones are ZeroParadox guard-hook refusals, so they are guard-coverage data too.
- **Lesson for the definition:** "same failure" needs a SPECIFIC signature (failing command or check plus error class). A bare exit code is not a signature.
