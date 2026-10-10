# Candidate: Incident-Driven Guard Coverage (renamed 2026-10-10; formerly "verified agent containment")

> **PARKED (2026-10-10).** Design v1 and the references are done. It needs an example built in mcp-mayhem (a read-only tool over gitRobot's audit log plus an incident record) before a YAML is worth writing.

> ⚠ SUPERSEDED on 2026-10-10 by Tim's reframe, below. `SUPERSEDED-claimed-restriction-verification-rate.yml` is kept for history only and must not be submitted.

**Status:** idea. Implementation read on 2026-10-09. Overlap and reference check running.

## The metric (draft wording)
- An AI agent acts through mediated tools, and the system claims a set R of restrictions on what the agent can do.
- **Verified containment** is the fraction of R demonstrated by an executed negative test. Such a test:
  - attempts the forbidden action;
  - observes the refusal;
  - checks that the protected state is intact afterwards.
- A restriction that is configured but never seen to refuse counts as **unverified**. One whose action succeeded counts as **failed**.
- Companion figure, **audit completeness**: the fraction of agent operations that left an audit record, including clean passes and refusals. This keeps "judged clean" and "never ran" distinguishable.

## Implementation: gitRobot (mcp-mayhem, public, MIT)
**Executed negative tests** (`gitRobot/tests/test_tier1_refusals.py`): 18 parametrized cases.
- The cases are:
  - the `reset` hard/merge/keep family (5);
  - `checkout -- .`, `checkout -- file`, `switch -- .`, `restore` (4);
  - `clean` -f/-fd/-fdx/bare (4);
  - `stash` push/-u/pop/drop/bare (5).
- Each asserts:
  1. `RefusalError`;
  2. the uncommitted work survives (`_assert_work_survives`: the tracked edit and the untracked file are both intact).
- The reset tests also assert that the refusal names an alternative.
- ⚠ They run through the **library** (`robot.guard_tier1`), not through the agent-facing MCP tool.

**Structural absence checks** (`tests/test_tier3_and_absent_controls.py:107-168`):
- `FORBIDDEN_PARAMS` (force, no_verify, skip_gates, allow_dirty, repo, cmd, command, passthrough, argv, shell, hooks_path) must be absent from every public library method AND from every registered MCP tool. The tool list is introspected, not hand-kept.
- There is no raw passthrough tool.
- Gate-disabling flags (`--no-verify`, `--force-with-lease`, `core.hooksPath`) never appear in an argv position.
- The forbidden-flag table covers `--no-verify`, `--force`, `-f`, `-c`, `--git-dir`, `--work-tree` and `--exec-path`.
- This is verification by **inspection**, not by an executed attempt.

**Audit:** every Tier 1/2 call (refusals and clean passes included) appends to `data/git_ops.jsonl` (README "The audit log"). `test_a_refusal_is_audited_and_explainable` and `test_reads_are_not_audited` cover this.

**Nothing computes the rate today.** There is no manifest of claimed restrictions R, and no runner that maps each restriction to its verification and prints verified / unverified / failed.

## Design consequence (found by reading the tests)
The definition should keep three verification kinds distinct, the same pattern as evidence currency:
- **verified by execution**, per surface (library, agent-facing tool);
- **verified by absence** (a structural check that the capability does not exist on that surface);
- **unverified**.

Read strictly, gitRobot's Tier 1 restrictions are execution-verified at the library and absence-verified at the MCP surface. The metric should show that difference, not hide it.

## What an example needs (for the mcp-mayhem session, once the YAML is drafted)
1. A restriction manifest: the claimed R, each item tied to its surface(s).
2. A runner that executes or collects the verifications and prints per-restriction status and the rate.
3. Ideally, executed refusals through the MCP surface too, so that "every surface" can be met rather than only reported.
4. An AI-agent framing in the README: the `reset --hard` incident, where the agent truthfully reported "clean" after destroying work.

## Overlap (research agent, 2026-10-09): ADJACENT, not a duplicate
**Catalogue "Agent / Tool Abuse Testing"** is the main risk of being folded in.
- Its definition, which I checked verbatim: "Testing whether a system misuses connected tools or external actions through, e.g., unsafe tool selection, excessive agency, unauthorized action attempts, or harmful task execution."
- Its TEVV application is red teaming, and its listed tools include AgentDojo.
- **What distinguishes ours:** it measures whether the **enforcement layer refuses**, not whether the **agent misbehaves**.
  - The denominator is the system's own claimed restriction set R, not a set of adversarial cases.
  - There is no adversarial prompting, and the result is deterministic.
  - It is model-agnostic.
  - Say "containment of unauthorized action attempts, not their occurrence" in the first sentence.

**Other catalogue entries:** Defense Efficacy, Refusal Rate and Jailbreak Success Rate are different, because they concern the model. Nothing in the catalogue covers sandboxing, permissions, least privilege or audit logging.

**Open PRs:**
- **#20** (descriptor mutation) is closest in structure. It shares the "configured versus effective" move, but measures definition integrity, not enforcement. It already cites Jia & Harman, so we should not reuse that.
- **#16** (audit tamper detection) is ADJACENT to the audit-completeness figure only. It explicitly excludes records that were never written ("Does not measure resistance to agent-internal log fabrication"). Cite it as complementary.
- #8, #15, #17, #19, #23, #6, #21 and #22 are different.

## References (I checked the starred items myself: quote in the text, DOI/venue/pages in Crossref)
1. ★ **Martin, E. & Xie, T., "A Fault Model and Mutation Testing of Access Control Policies," WWW 2007, 667-676.** https://doi.org/10.1145/1242572.1242663
   - "Rule coverage is the number of covered rules divided by the number of total rules."
   - It is the analogous ratio, computed at the policy decision point.
2. ★ **El Kateb, D., El Rakaiby, Y., Mouelhi, T. & Le Traon, Y., "Access Control Enforcement Testing," AST 2013 (IEEE), 64-70.** https://doi.org/10.1109/IWAST.2013.6595793
   - "PEPs are generally implemented manually, which can introduce errors in policy enforcement and lead to security vulnerabilities."
   - "...verify for every sensitive access whether the policy is correctly enforced."
   - Specified versus actually enforced is our distinction exactly. It defines no ratio.
- Optional: NIST SP 800-192 (Hu, Kuhn, Yaga, 2017), verification and test methods for access-control policies. This is a NIST technical method, not governance. The agent quoted it, and I have not checked it.
- **Rejected:**
  - AgentDojo and ToolEmu: they measure behaviour, AgentDojo is already a tool of the catalogue entry, and ToolEmu emulates execution rather than executing.
  - R-Judge and Agent-SafetyBench: they concern risk awareness, and their venues are unverified.
  - Le Traon ISSRE 2007 and Mouelhi TAIC 2007: closed access, text unverified.
  - Saltzer & Schroeder: principles only.

**Draft candour sentence:** "To our knowledge no published work defines this ratio for AI-agent tool mediation. The references define the analogous rule-coverage ratio for access-control policies (Martin & Xie) and test that enforcement points actually deny (El Kateb et al.). This metric applies that idea at the agent's tool boundary and has not been independently validated."

## Framing (adopted)
"Claimed-restriction verification rate for agent tool mediation": of the restrictions a system claims on its agent's tools, the fraction shown to refuse when the forbidden action is actually attempted through every exposed surface, with protected state confirmed intact.
- It is the enforcement-point counterpart of rule coverage, applied at the agent's tool boundary.
- Keep the per-restriction report (verified-by-execution / verified-by-absence / unverified / failed) central, and the ratio secondary.
- **Known failure mode: a gameable denominator.** A narrow R inflates the score, so publish |R| and where it came from.
- Audit completeness is a SECONDARY figure, explicitly complementary to #16.

## Deferred (2026-10-09)
- **Audit completeness** (secondary figure) was cut from the YAML in the conciseness pass after NIST rejected #19 for length. It is a candidate follow-on, complementary to #16. The reviewed definition was: of the operations that the system claims to audit and that the harness performed (counted by the harness), the fraction with a matching audit record, refusals and permitted actions included.

## REFRAME (Tim, 2026-10-10, relayed by mcp-mayhem-48)
Tim: a finite attempt list implies "stops everything except…", which is the opposite of the claim. "It needs to be an iterative or ongoing process, not just a single point in time metric." The new measure is how well the guard set tracks what agents actually attempt, over time:
1. **Observed-pattern coverage:** the share of distinct observed risky patterns that have a guard AND a regression test.
2. **Time to guard:** first observation to the test that pins it.
3. **Residual risk:** the Good-Turing unseen mass, (patterns seen once) / (observations). Report it only above a stated volume.
4. **Trend:** new patterns per batch of sessions.
Caveats: it sees only attempts made through the tools, "distinct pattern" needs a classification rule, and it needs volume.

## Audit-log check (metrology, read-only, 2026-10-10)
- Source: `mcp-mayhem/.mcp-local/gitRobot/git_ops.jsonl`. 5,930 records from 2026-08-22 to 2026-10-10: 4,869 allowed, 817 started, 177 refused, 67 failed.
- The 177 refusals form 62 (op, detail) keys, 43 of them singletons. The kinds:
  1. gate failures (×42 pre-commit, ×30 ledger admission);
  2. operational conflicts;
  3. **risky attempts** (`-n` redirect ×7, `stage -A` ×2, `reset --hard` ×1);
  4. **benign reads refused** (tag, ls-tree, merge-base, fsck…).
  Test probes are also present in the production log.
- ⚠ **The refusal log contains only patterns that are already guarded.** The `+branch` force-push succeeded, so it is absent from the log. Coverage computed from refusals is therefore near 100% by construction. The observation source must be **incidents** (allowed operations later found harmful) plus kind-3 refusals. Incidents are rare, about 3 known, so volume is the main limit on the estimate.
- A companion the log supports today: the **false-refusal rate** (kind 4). Over-blocking pushes agents toward working around the guard.
- Leads to verify:
  - Good, I. J. (1953), "The population frequencies of species and the estimation of population parameters", Biometrika;
  - Böhme, M. (2018), "STADS: Software Testing as Species Discovery", ACM TOSEM.
- Recommended to Tim: split containment off as a later, separate submission with its own tag. Pending his decision.

## Working definition draft v0 (metrology, 2026-10-10). Pending the research agent, NOT yet a YAML
**Observation.** An event $e$ = (time, session, tool, operation, arguments, outcome) that is one of:
- (i) an **incident**: an operation the tool ALLOWED that review later judged harmful (e.g. the `+branch` force-push);
- (ii) a **risky refusal**: a refused attempt at an action the guard exists to stop (e.g. `reset --hard`, the `-n` repo redirect, `stage -A`).

Excluded and reported separately:
- gate failures and operational conflicts;
- **benign refusals** (harmless actions blocked), which feed the false-refusal companion;
- test probes, identified by actor or run id.

**Pattern.** A declared, versioned classification function $\kappa(e)$ maps each observation to a pattern id, e.g. (tool, operation, normalised risky feature of the arguments). Changing $\kappa$ requires recomputing history; the version is reported.

**At time $T$:**
- $K(T)$: the distinct patterns observed so far.
- $G(T) \subseteq K(T)$: patterns that have (a) a guard that refuses them, and (b) a regression test at revision $T$ that replays the original observation through the entry point the agent uses, asserts the refusal, and passes.
- **Coverage** $= |G(T)|/|K(T)|$, reported with both counts. Undefined if $K(T) = \emptyset$.
- **Time to guard**, per pattern: from its first observation to the first revision where it is in $G$. Report the median over guarded patterns and the age of each pattern still unguarded.
- **Discovery trend:** new patterns per window (per $N$ agent sessions, or per week), with the cumulative curve.
- **Residual estimate:** $f_1/n$, where $f_1$ is the number of patterns observed exactly once and $n$ the number of observations. This is the Good-Turing estimate of the probability that the next observation is a new pattern. Report it ONLY when $n \ge n_{min}$ (threshold to be set from the literature), always with $f_1$ and $n$ shown.
- **Companion, false-refusal rate:** benign refusals / all refusals in the window.

**Known validity issues to state:**
- Refusals are already-guarded patterns, so discovery comes from incidents, and incidents are rare. The estimate may never reach $n_{min}$ for a small deployment, and the method must say so rather than report it.
- It only sees what happens through the tools.
- $\kappa$ decides everything: too fine inflates $f_1$, too coarse hides variants.
- It assumes the agent population and tasks are roughly stationary within a window.

**Existing evidence of the loop**, each observed, then guarded and tested:
- the `+branch` force-push (77c6d09);
- `reset --hard` (gitRobot README);
- ZeroParadox's .NET relative-path writes.

## Research results (2026-10-10). Quotes checked by metrology in the extracted text; DOIs checked in Crossref
**Overlap:** no duplicate.
- Adjacent catalogue entries: "Agent / Tool Abuse Testing" (it generates observations and defines no metric) and "Post-deployment Feedback" (the incident input stream, with nothing on the absorption rate).
- ⚠ The false-refusal companion is ALREADY in the catalogue (FRR-f / FRR-p). Drop it and cite those entries instead.

**References:**
1. ★ Böhme, M. (2018). "STADS: Software Testing as Species Discovery." ACM TOSEM 27(2), 1-52. https://doi.org/10.1145/3210309
   - "The Good-Turing estimator [49] is computed as the number of singletons divided by the number of samples (i.e., generated test inputs)."
   - "the sample coverage C(n) = 1 - U(n) measures the probability that the n + 1th generated test input belongs to an already discovered species."
2. ★ Böhme, M., Liyanage, D., & Wüstholz, V. (2021). "Estimating Residual Risk in Greybox Fuzzing." ESEC/FSE '21, 230-241. https://doi.org/10.1145/3468264.3468570
   - Blackbox estimators "systematically and substantially under-estimate the true risk" under adaptive sampling.
- Also: Good (1953), Biometrika 40(3-4), the origin of the estimator. Ozment (2007), QoP, the critique of vulnerability-discovery-model assumptions; he counts "detection events".

## Design changes the literature forces (v1)
1. **Headline = a probability about the NEXT session, not a share of past patterns.** The share of observed patterns that are guarded tends to 100% by construction. Report the sample coverage, i.e. the estimated probability that the next observed pattern is already guarded.
2. **Incidence model, with the session as the sampling unit** (STADS Eq. 28-29, U ≈ Q1/V). Count a pattern once per session in which it appears; Q1 = patterns seen in exactly one session, V = sessions. Repeated refusals of one guarded pattern must not inflate n.
3. **Reset windows.** Adding a guard changes the sampling process: an incident becomes a refusal, and agents adapt. Following FSE21's reset estimator, estimate only within windows of a fixed agent, tool and guard version, and restart the counts at each version change.
4. **Minimum volume is our own stated choice.** No source gives a number. Justify the threshold (e.g. require f2 > 0, citing the MSE < 1/n bound) and say so. Below it, report counts only.
5. **Time-to-guard** is a plain duration statistic with no reference behind it, so present it as such.
6. **Discovery trend** normalised by sessions (Ozment).
7. **Drop** the coverage share as a headline and the false-refusal companion (it is in the catalogue).

**Minimal honest claim (agent's draft):** "Within a fixed agent, tool and guard version, and over what the detection process can observe, this estimates the rate at which observed risky-action patterns are absorbed into regression-tested guards, and bounds the probability that the next observed pattern is new. It says nothing about patterns the detection process cannot see, and it is invalid across version changes or when detection effort shifts."

**Feasibility at Tim's scale:** about 3 incidents plus a handful of risky refusals is far below any defensible threshold. The honest example shows the METHOD running on the real log: counts, time-to-guard and the trend, with the estimate correctly withheld as below threshold. It must not invent a probability.
