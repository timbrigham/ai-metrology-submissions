# Candidate: Incident-Driven Guard Coverage (renamed 2026-10-10; formerly "verified agent containment")

> **PARKED (2026-10-10).** Design v1 and the references are done. It needs an example built in mcp-mayhem (a read-only tool over gitRobot's audit log plus an incident record) before a YAML is worth writing.

> ⚠ SUPERSEDED on 2026-10-10 by Tim's reframe, below. `SUPERSEDED-claimed-restriction-verification-rate.yml` is kept for history only and must not be submitted.

**Status (original, superseded):** idea, 2026-10-09. See the PARKED banner above.

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
  Three deliberate 'not-allowed' calls against the live server are also present (real calls, not test output; see the correction below).
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
- deliberate probe calls, identified by actor or run id. NOTE: lane-worktree records are real work, never exclude them as test traffic.

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

## Feasibility prototype on the real gitRobot log (metrology, read-only, 2026-10-10)
Source: `mcp-mayhem/.mcp-local/gitRobot/git_ops.jsonl`, actor=mcp. (The original run wrongly excluded the Temp lane-worktree repos as test traffic and counted 154 refusals; the true number is 177. See the correction.)
- **No session identifier in the log.** `actor` is mcp or reaper, `pid` is the server process (many sessions each), and `run_id` exists only for gate runs. The incidence model (the session as unit) is NOT computable. Calendar day was used as a stand-in: V = 49 days.
- ~~Test traffic is mixed in: 1,308 records come from Temp test repos.~~ WRONG: see the correction below.
- **My first κ pass was wrong twice:**
  - the "force-push" bucket (11) was all evidence-ledger admission refusals. ZERO force-push attempts were ever refused, consistent with the `+branch` hole, which succeeded;
  - the "-n repo redirect" bucket (8) was all BENIGN: `git log -n 25` (count), `git grep -n` (line numbers), `rev-parse --git-dir` (prints a path). **This is a gitRobot false-refusal bug, reported to mcp-mayhem-48.**
- **Real risky refusals:** 3 in 7 weeks (`reset --hard` ×1, `stage -A` ×2). With about 3 known incidents, n ≈ 6, far below any defensible threshold.
- **False refusals are the richer signal:** 26 benign reads refused as not allow-listed, plus the 8 `-n` refusals. The catalogue's FRR-f / FRR-p cover model prompts, not tool actions.

**Consequences:**
1. The definition survives. The forecast is correctly WITHHELD at this scale, so an example would show counts and time-to-guard only.
2. The instrument needs three changes before it can carry the metric: (a) record the MCP session id per call; (b) [withdrawn: the "test traffic" premise was wrong, see the correction]; (c) a structured incident record (today incidents live only in prose).
3. The κ errors show why the definition must require a declared, reviewed classification rule.

**CORRECTION 2026-10-10 (verified by metrology after mcp-mayhem-48 flagged it):** the 1,308 git_ops records with an `AppData\Local\Temp\gitrobot-worktrees\<lane>` repo are NOT test traffic. They are real ZeroParadox operations in gitRobot's lane worktrees (626 commit, 461 stage, 217 attest, 4 unstage; actor mcp; 2026-09-20 → 10-09). Filtering them out discarded real evidence. They include 23 refusals (20 gate, 3 operational, 0 risky), so all 177 refusals are real, not 154. The "3 risky refusals" figure STANDS. The 3 'not-allowed' calls were deliberate live calls, not test-suite output. The test suite does not write to the production log (GITROBOT_DATA is unset).

## Instrumentation landed (2026-10-13): consequences for this metric
- Use `refusal_class` (d94f093), not regex, as κ's first cut. Only `policy` refusals are risky-attempt observations. Precedence (published in mcpcommon/vocabulary.py): operational if waiting or changing state clears it; gate if changing content or evidence does; otherwise policy. `allowlist` is the read allow-list only, and is the false-refusal signal.
- ⚠ Exclude `op=attest` refusals: they are the hook asking whether it may skip its second run, not an agent attempting anything (mcp-mayhem-48's reviewer). Counting them would inflate gate.
- Classes that differ from a naive reading: a push with '+' or ':' is policy; a push to a non-local branch name, or without a reason, is operational; "not a worktree" is policy if a foreign path exists, operational if the path has vanished.
- `session` and `surface` (abdb679) supply the sampling unit. Rows before abdb679 / d94f093 lack these keys: absent means "before the field existed", never "unknown". Analyse pre- and post-field windows separately.
- **Incident register** (0808754): SJV consumer `incidents`, store `mcp-mayhem/.mcp-local/incidents/incidents.json` (private).
  - CLI: `sjv --data <file> --consumer incidents --collection incidents apply|validate|view summary`.
  - Verbs: add_incident (open/wontfix), set_guarded (guard_commit, regression_test and guarded_at together; only from open), annotate.
  - Times are UTC and ordered (observed ≤ detected ≤ guarded). pattern_id = <tool>.<operation>.<shape> under pattern rule "1".
  - Seeded with 2 incidents, both guarded. It shows no OPEN incidents yet, which is a statement about the recorded incidents, not about coverage.

## YAML rev 2 (2026-10-13), after adversarial review (REVISE, 6 blocking)
- **B1 fixed:** the estimator is $Q_1/n$ with n = sessions in the window, including empty ones (FSE21 Eq. 22, Good-Turing; verified in the text). The earlier "Q1/V" mis-cited STADS: there V = "the sum of all entries in the incidence matrix" (total incidences), verified. The invented "f2>0" withhold was replaced by n ≥ 100 from Robbins' bound "mean squared error ... less than 1/n" (quoted in STADS; verified), applied by analogy.
- **B2:** items 1-3 are cumulative; only item 4 is windowed.
- **B3:** incidents with an unknown session count toward K and G only; an unknown occurrence time gives a lower bound, excluded from the median.
- **B4:** the guard set is declared; only logging guards contribute refusal observations.
- **B5:** failure mode on versions.
- **B6:** removed the unverifiable "44 vs 62".
- Length cut from 879 words. FSE21's "reset estimators systematically overestimate and exhibit a high variance" is now disclosed (verified).

## Prerequisites before the example can make the YAML true
1. **Register fix (mcp-mayhem-48):**
   - INC-0001 occurred through a SHELL before gitRobot existed; its registered regression test replays through gitRobot `read`. Under the definition it is NOT in G unless the shell-layer guard (ZeroParadox `block_git_gh.ps1` + its test) is the recorded guard.
   - INC-0002 has detected_at = guarded_at (found while building a harness, not an agent attempt).
   - DC-71 ×3 still to be recorded.
2. **New instrumentation (needs Tim's approval):** log VERSIONS per session (gitRobot commit, hook commit, MCP clientInfo name and version). Without them, windows cannot be computed from the data.
3. **Data reality (2026-10-13):** since abdb679 / d94f093 there are 0 agent sessions, 0 policy refusals, and only reaper rows. `session` is the HTTP mcp-session-id (a connection, not a conversation). The ZeroParadox shell hooks log nothing.
4. **Wait for the DC-71 guard** (zeroparadox session, confirming the settings change with Tim). It gives the only exact time-to-guard: observed 2026-10-04.

## Minimum worked example (reviewer's spec, adopted)
- A stdlib tool in mcp-mayhem at a release tag. Inputs: audit JSONL, register JSON, pattern-rule version, a guard-set manifest (gitRobot + ZeroParadox hooks: repo, whether it logs, its test) and window boundaries. Output: JSON + text for items 1-4, every withheld value with its reason.
- A PUBLIC fixture: a redacted extract of the real policy-refusal rows and register entries, with checksums. One command reproduces the YAML's numbers. (`.mcp-local` is private.)
- A real-data section stated as-is: K and G with sources; unguarded patterns with ages; time-to-guard exact values and flagged lower bounds; post-field n; Û withheld (n<100).
- A SYNTHETIC replay (labelled synthetic, seeded, 1,000 replicates): about 30 Zipf-distributed patterns, about 2,000 sessions, a guard added after first sight with injected lag, and a probability shift at each guard. Report:
  - Û bias and coverage against the true expected-new rate, within windows and pooled;
  - the withhold rate at n<100;
  - recovery of the injected lags.
  This answers "no evidence the method works".
- The YAML Example field: at most 60 words, one line real plus one line synthetic, from the tagged run.

## Tim's approvals (2026-10-13 Q&A), sent to mcp-mayhem-48
- Instrumentation item 5, VERSIONS per session (gitRobot commit, MCP clientInfo name and version, ZeroParadox hook commit if available): **Yes**.
- Public fixture: **redacted real extract + synthetic replay**. Keep only timestamps, op, refusal_class, pattern id, hashed session and versions. No file contents, args or private paths.
- Correct INC-0001 to name the shell-layer guard (block_git_gh.ps1 + its test): **Yes**. The register forbids rewriting a guard, so mcp-mayhem-48 picks the method (annotate or supersede).
- Sequence: item 5 → the example (tool + fixture + synthetic + README + review) → the DC-71 guard lands (zeroparadox session, confirming settings.json with Tim) → final numbers → verification → a NEW tag (name: Tim's call).

## Register state and corrections (2026-10-13)
- DC-71 RECORDED by mcp-mayhem-48 (Tim approved): INC-0003/0004/0005, open, pattern `powershell.dotnet-file-write.relative-path` (rule "1"). The register holds 5 entries (2 guarded, 3 open) and validates.
  - detected_at is a sourced UPPER bound (11d10ad 2026-10-04T20:26:20Z for occurrences 1-2; the 01:44Z restore for occurrence 3).
  - observed_at is null for all three, since only dates are known.
- ⚠ CORRECTION to my earlier claim that the DC-71 guard would give "the only exact time-to-guard": it will NOT. observed_at is null, so time-to-guard is a lower bound from detection. EVERY real incident is currently a lower-bound case, so the synthetic replay carries the "the method works" evidence.
- INC-0001 fix: a new verb `correct_guard`, with an append-only `guard_history` (reason, when, and the entry point the superseded guard covered). The tool reads the CURRENT guard for G and time-to-guard; history is provenance. The new guard is ZeroParadox block_git_gh.ps1 + its test (read-only lookup).
- Item 5: the ZeroParadox hook commit will be null (gitRobot can't see it). Guard versions come from the guard-set manifest input, and the example README will say so.
- Order: item 5 → correct_guard → the example. Tim confirmed "Yes, build it" in mcp-mayhem-48's session.

## DC-71 GUARD LANDED and VERIFIED (2026-10-13)
- ZeroParadox: 6312942 (hook, 12:11:14Z) → 36df2f5 (follow-up, 12:26:49Z) → merged into `illustrated` as b6bae57 at 2026-10-13T12:33:42Z, the moment it became active for agents. Registered in .claude/settings.json for both shells.
- Verified by metrology from a clean `git archive b6bae57` export: test_block_dotnet_relative_write.ps1 reports "ALL 25 CONTROLS BEHAVED", exit 0, including DC71-2/DC71-3 (the incident shape) and 7 mutation checks.
- Proposed to mcp-mayhem-48: set_guarded for INC-0003/4/5 with guard_commit b6bae57, guarded_at 12:33:42Z, regression_test …::DC71-2/3. Tim confirms there. observed_at stays null, so time-to-guard is a lower bound from detection.
- The first complete worked loop: observed → recorded open → guard built → tested → guarded. When marked, the register is 5 guarded / 0 open.

## INC-0003/4/5 MARKED GUARDED, verified (2026-10-13)
- mcp-mayhem-48 wrote it with Tim's approval in that session. Metrology read `.mcp-local/incidents/incidents.json` directly (read-only): 5 entries, all `guarded`, 0 open.
- INC-0003/4/5: guard_commit b6bae57fbc6eb4cd2bc8f20e8a311991c986aff3, guarded_at 2026-10-13T12:33:42+00:00, regression_test `tools/verify/claude_hooks/test_block_dotnet_relative_write.ps1::DC71-2`. These match the proposal. A note on each names the implementation commits, DC71-3, the same entry point, the lower bound and the accepted gaps (python/node, scripts written then run, -EncodedCommand, the [IO.FileInfo] relative shape).
- The earlier note on each entry still says "guard specified but unbuilt". The notes are append-only and the newer note supersedes it, so this is not an error.
- Pattern-level time-to-guard for `powershell.dotnet-file-write.relative-path`, a LOWER bound measured from its first detected_at (2026-10-04T20:26:20Z): **8 d 16 h 07 m**. Per-incident: INC-0003/4 the same, INC-0005 4 d 10 h 50 m (from 2026-10-09T01:44Z). Every real case is a lower bound, so the median is withheld.
- INC-0001 still names gitRobot 77c6d09 (it replays through `read`), pending `correct_guard` to ZeroParadox block_git_gh.ps1 and its test. Until then the guarded share depends on how that guard is counted; the example must use the corrected guard.
- Also reported by mcp-mayhem-48: the ZeroParadox check_hashes.py repin is done (30a444b, narrowed in b2d36be), and Tim declined the gitRobot worktree-hint change. Neither affects this metric.
- Next, in order (mcp-mayhem-48): the item 5 review fixes → correct_guard for INC-0001 → the worked example.

## Item 5 VERIFIED; INC-0001 test gap; guarded_at rule (2026-10-13)
- Item 5 (versions) is mcp-mayhem f813216, equal to origin/main. gitRobot was restarted at 14:23:30Z, after the commit.
  - Every row now carries `versions`: gitrobot_commit (read at import), gitrobot_dirty, client_name, client_version, consumer_hook_commit (always null).
  - Metrology verified:
    - Clean clone: test_audit_attribution + test_push_async **30/30**.
    - Clean `git archive` export: **567/568**. The failure is test_the_cli_reports_no_client: gitrobot_commit is None because an archive has no .git. The code is correct; the test assumes a checkout. Asked mcp-mayhem-48 to skip or adjust it and to say in the example README that versions need a git checkout. Not blocking.
- ⚠ INC-0001 GAP (found by mcp-mayhem-48, confirmed read-only by metrology):
  - ZeroParadox block_git_gh.ps1 (872811c, 2026-08-23T14:22:18Z) denies all direct git, but test_block_git_gh.ps1 contains no "reset" control.
  - So no regression test replays the observed action, and INC-0001 is not in G under the definition until one exists.
  - Chosen: (a), one `git reset --hard` → DENY control plus a mutation check. The zeroparadox session has queued it for the next tooling batch, after the wave 3 push; Tim sees it first. They will send the commit and merge SHAs and times, the control id and the suite line. mcp-mayhem-48 then runs correct_guard (verb being built).
- RULE (metrology → mcp-mayhem-48): guarded_at = the FIRST moment at which both the guard and a same-entry-point regression test are in place on the branch agents use. This matches DC-71 (merge b6bae57).
  - YAML item 2 now reads "to the first commit at which both the guard and its regression test are in place".
  - Validators: schema OK, inspect OK. The applied text is now 831 words.
  - For INC-0001 the guard came ~18h after detection, and the tested guard about 52 days later. The example README reports both; the gap is what the metric exists to show. 872811c goes in the correct_guard note as provenance, not as G.
- Consequence: the register is 4 of 5 entries in G until the reset control lands; patterns |G|/|K| = 2/3 (git.reset.work-destroying is pending).

## Example review round 1: YAML-side items (2026-10-13, from mcp-mayhem-48)
The example is built but not committed. A fresh adversarial review found code issues (mcp-mayhem-48 is fixing them) and these YAML items:
1. **Estimate vs bound: FIXED in the YAML.**
   - Item 4 is renamed "Unseen-pattern estimate".
   - The target is now named: $U_n$, the expected number of patterns absent from the window's n sessions that appear in the next one. $U_n$ bounds the probability (Markov), and $\hat U$ is an estimate of that bound, not a guarantee.
   - Patterns seen only in earlier windows count as absent, so the estimate errs high for never-seen patterns.
   - The grounding line now says "erring high, the safe side here" instead of "conservative for a bound".
   - Schema check OK; 867 words.
2. **Real data exercises little.** K=3, 0 policy refusals, all time-to-guard values are lower bounds (median withheld), and n=0 for item 4 because no session carries versions yet. The real-data line will read roughly "2/3 guarded; median withheld; Û withheld (n=0)". Items 2 and 4 are shown only on synthetic data, and the README says so. DECIDED (Tim, 2026-10-13): **submit once the example is verified, framed honestly**; do not wait for data.
3. **Synthetic results are being redone.** v1 reported 0.989 coverage, but it was mostly trivial: 63% of windows had truth=0; where truth>0 it was 0.970; against the in-window target it was 0.537. v1 also logged every pre-guard attempt as a refusal, which real logging cannot see.
   - v2: pre-guard attempts appear only as incidents recorded with probability r; guards that don't log; coverage reported only where truth>0, with a cluster-bootstrap CI; both targets named.
   - **Never quote v1 numbers.**
4. **Window restarts.** The manifest carries one version per guard, so a window can restart at most once per guard. mcp-mayhem-48 will either add a version history or add a caveat, and will say which; if it's a caveat, add it to known_failure_modes.
5. INC-0002 has detected_at = guarded_at; the tool flags it as "detected at fix time".
6. ZeroParadox is a PUBLIC repository (visibility checked by mcp-mayhem-48), so naming it, DC-71 and its SHAs in the fixture is fine.
- Held local commits in mcp-mayhem: 8851b35 (correct_guard) and b77a76f (the release-zip test fix). They ship with the example after review and Tim's OK. No tag yet.
