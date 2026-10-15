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

## Example review round 2: YAML-side items (2026-10-13)
A second fresh review confirmed round 1's fixes: the salt leak is closed, recording is realistic, null-session refusals are handled, windows use version_history, and INC-0002 is flagged. It found no redaction leak and confirmed that U_n truth and the cluster bootstrap are correct. A final code and README round is in progress in mcp-mayhem.
- Item 2 FIXED: the YAML now says "When any of the pattern's occurrence times is unknown … leave it out of the median, which therefore errs optimistic: long lags gather more incidents and are more often left out." The synthetic run shows about −9 h against a median injected lag of about 126 h.
- Item 4 "agent versions" FIXED:
  - The definition keeps "agent (model)", because a model change can alter what agents attempt.
  - Known failure mode 5 now says the reference implementation logs the guard layer's commit, the client's name and version and each guard's version history, but NO model version, so a model change silently pools windows.
- Synthetic summary: the primary figure for item 4 is BIAS with a 95% CI, plus RMSE against U_n. Coverage is demoted, because for a skewed discrete Q1 an unbiased estimate need not cover near 0.5.
  - All synthetic figures are CONDITIONAL on n ≥ 100, an outcome-selected subset of about 19% of windows. The Example line must say so.
- Window restarts: mcp-mayhem chose an optional per-guard `version_history`, tested, so no caveat is needed.
- Schema OK; 906 words.
- The Example TODO is filled from the tagged run.

## Worked example VERIFIED from a clean export (2026-10-13)
- mcp-mayhem f7da1ed78f86d0b13978c474e1e3ae5a3c35023d is equal to origin/main. It follows f813216 (versions), 8851b35 (correct_guard and guard_history) and b77a76f (release-zip test fix). Tim confirmed the push in mcp-mayhem-48's session. NO TAG yet.
- Metrology checked a `git archive f7da1ed` export:
  - fixture CHECKSUMS.sha256: all 5 OK;
  - guardCoverage tests: **62/62**;
  - `measure --json` is byte-for-byte equal to expected_report.json, and the text report matches the README and the message;
  - `synthetic --seed 7 --replicates 1000` output equals the reported figures.
- mcp-mayhem-48 reports sjv 222, verdictLedger 652, gitRobot 568 and guardCoverage mutation 16/16. Metrology did not re-run these here; gitRobot was 568 at f813216 plus b77a76f.
- REAL: |G|/|K| = 2/3. git.reset.work-destroying is unguarded, age ≥ 51.75 d: the agent-shell guard has no replaying test, and 77c6d09 sits at the wrong entry point.
  - Time to guard: refspec-force ≥ 0.00 d (detected at fix time); dotnet-file-write ≥ 8.67 d; median withheld.
  - Discovery trend: 3 before the first logged session, then 0 and 0.
  - Item 4: n = 0 (no window yet), withheld.
- SYNTHETIC (seed 7, 1000 replicates, r = 0.30, 70% of guards logging; 30 Zipf patterns, 2000 sessions):
  - Item 4: 28,908 windows; 80.8% withheld at n < 100, so 5,540 are reported (19.2% of windows, 63.6% of sessions).
  - Against U_n: bias +0.0004 (95% CI −0.0000 to +0.0009), RMSE 0.0180 (mean Û 0.0262), coverage 0.501.
  - Against the never-observed target: bias +0.0185, coverage 0.903.
  - Item 2: exact-only median minus the injected median is −9.2 h (injected median 126 h); 12,031 values are lower bounds, with a mean shortfall of 36.5 h.
  - End to end, replicate 0 agrees.
- REDACTION (metrology's own scan):
  - Register keeps only ids, pattern, times, guard commit, has_regression_test, entry point and hashed session. No harm text and no notes.
  - Audit keys: ts, op, decision, refusal_class, surface, hashed session, versions.
  - No C:\, C:/, Users, timbr, @, .mcp-local, Temp, token, password or raw session id.
  - DEVIATION from Tim's "no args": 72 refused rows keep a reduced `args`: read → a git verb name (ls-tree, grep, tag, reset, …); push → `{"branch":"b"}` (the shape of the refspec). It is documented in metadata.json as the rule-1 pattern feature. Benign, but Tim was told.
  - The salt is published, which is fine: it hashes only random MCP connection ids.
- DECIDED (Tim, 2026-10-13):
  - **Wait for the INC-0001 fix before tagging.** The sequence is: ZeroParadox reset control → metrology verifies it → correct_guard → the fixture and expected report are regenerated → metrology re-verifies from a clean export → tag.
  - The fixture's reduced args are **accepted**.
  - Tag name: no preference, so metrology picked **`nist-metrology-2026-10b`**, a sibling of the existing tag.

## INC-0001 regression control LANDED and VERIFIED (2026-10-13)
- ZeroParadox 5bf7106 (2026-10-13T17:41:53Z) was merged into `illustrated` as **283157b90077450f651907054b12ca2a45089949 at 2026-10-13T17:47:17Z**. Pushed at 18:00:12Z; it is on origin/illustrated. The merge changes only test_block_git_gh.ps1 (+50/−3). Tim approved it in the zeroparadox session.
- Metrology verified from a clean `git archive 283157b` export: **"ALL 27 CONTROLS BEHAVED", exit 0**. The suite includes:
  - GIT-INC0001: `git reset --hard` sent verbatim through Invoke-Hook, the same path as bare git, DENY;
  - GIT-MUT1: the deny branch is removed, the SHA changes, and the result goes to ALLOW;
  - GIT-MUT0: the unmutated copy still denies.
- block_git_gh.ps1 is registered for both the Bash and PowerShell matchers at 283157b, and the hook has existed since 872811c. The test sends tool_name PowerShell only; INC-0001's shell was not recorded. Accepted: the hook does not branch on the tool.
- Values sent to mcp-mayhem-48 for correct_guard: guard_commit 283157b, guarded_at 2026-10-13T17:47:17+00:00, regression_test `tools/verify/claude_hooks/test_block_git_gh.ps1::GIT-INC0001`, entry point agent-shell. Provenance: the hook has denied all direct git since 872811c, 2026-08-23T14:22:18Z.
- Expected real item 1: 3/3. Expected time to guard for git.reset.work-destroying: ≥ 51.89 d (from detected_at 2026-08-22T20:27:40Z), a lower bound.

## INC-0001 corrected; example regenerated and RE-VERIFIED (2026-10-13)
- mcp-mayhem 08ec670ff46a88e3f3dc92e15d099f7a6fc89629 is equal to origin/main. Tim confirmed the push in mcp-mayhem-48's session.
  - Register: correct_guard on INC-0001 is set to 283157b / 17:47:17Z / GIT-INC0001; 77c6d09 is moved to guard_history ("gitrobot-mcp/cli (gitRobot read)").
  - The manifest's test label is the plain "ZeroParadox block_git_gh hook suite, control GIT-INC0001", because make_fixture's redaction scan refused the consumer path.
- Metrology checked a clean `git archive 08ec670` export:
  - checksums 5/5; guardCoverage 62/62;
  - `--json` equal to expected_report.json;
  - synthetic output byte-identical to the f7da1ed run;
  - leak scan clean: no paths, user names, raw session ids, .ps1 or claude-local.
  - The new rows add client names claude-code 2.1.286 and zp-hooks-attest 1. Both are fine to publish.
- REAL NOW:
  - item 1 = 3/3;
  - time to guard: reset ≥ 51.89 d, refspec ≥ 0.00 d (detected at fix time), dotnet ≥ 8.67 d; median withheld;
  - 17 sessions, with no new patterns after the first batch;
  - item 4: W1 n=1, W2 n=2, Û withheld.
- ⚠ PRE-TAG FINDING (metrology → mcp-mayhem-48): W2 (17:41:54–17:47:17Z, n=2) matches ZeroParadox's commit and merge, and its sessions are almost certainly client `zp-hooks-attest`, which is hook automation, not an agent. The YAML's unit is the AGENT session, but the tool counts every client in n.
  - No reported number changes, since Û is withheld either way. It is still a mismatch between the definition and the implementation, and cheap to fix.
  - Asked for: the manifest declares the non-agent clients (or the agent clients); the tool excludes those sessions from n and from item 3's batches and reports how many it excluded; the README states it; the fixture and expected output are regenerated.

## Agent-client rule; example RE-VERIFIED at 75b8862 (2026-10-13)
- mcp-mayhem 75b8862d4b1c340dcba55aca50e3edd4524da520 is equal to origin/main, and only guardCoverage/ changed. Tim confirmed the push.
  - W1 = claude-code (the agent).
  - W2 = zp-hooks-attest (ZeroParadox's pre-commit hook calling attest), which is automation.
  - The 4 null-client rows were gitRobot's reaper (surface internal), already excluded.
- Rule: the manifest's `agent_clients: ["claude-code"]` is an ALLOW-list.
  - Undeclared clients, and sessions with no recorded client, are not counted; they are listed with count and reason.
  - If agent_clients is absent, no session counts; it is never treated as "everyone".
  - Refusals outside an agent session are not observations.
- Metrology checked a clean `git archive 75b8862` export:
  - checksums 5/5; guardCoverage **65/65**;
  - `--json` equal to expected_report.json;
  - synthetic byte-identical to f7da1ed.
- REAL:
  - 1 agent session; 14 with unknown client and 2 zp-hooks-attest are not counted;
  - item 1 3/3; item 2 unchanged, median withheld;
  - item 3: 3 patterns before the first logged session, then 0 new in 1 session;
  - item 4: W1 n=1, Û withheld.
- YAML unit sentence updated to say "from a client declared as an agent; sessions of other clients, such as a commit hook, are not counted". Validators OK; 925 words.
- READY TO TAG: `nist-metrology-2026-10b` at 75b8862. Tags are cut ONLY on Tim's own instruction in mcp-mayhem-48's session; mcp-mayhem-48 must not ask him about it. That session is holding. Metrology then verifies the tag with ls-remote and fills in the YAML Example line and implementation link.

## TAGGED and RELEASED: `nist-nov-2026` (2026-10-13)
- Tim tagged and released it himself (release published 18:31:13Z). It is a lightweight tag at **75b8862d4b1c340dcba55aca50e3edd4524da520**, verified with ls-remote. **The old tag `nist-metrology-2026-10` is REMOVED** from the remote (Tim's decision).
- Consequence: ALL THREE submissions now cite `nist-nov-2026`.
  - verdictLedger/ and inventoryFidelity/ are unchanged between 97d2988 and 75b8862 (empty diff).
  - Re-verified from a clean export of the tag: inventoryFidelity 86/86; verdictLedger 651/652 (the known CRLF artifact of a Windows export); the evidence-currency example reproduces the YAML's stages (4/4 → 3+1 stale → 3+1+1 never examined → 5/5).
- Guard-coverage YAML: implementation links filled; Example line filled (60 words, from the 75b8862 report and the seed-7 synthetic run); 953 words.
- Validators: schema and inspect OK for all three YAMLs. Links: every repo link returns 200; the ACM DOIs return 302 to dl.acm.org, which returns 403 to scripts (bot blocking); the IEEE DOIs return 202.
- PR.md written. Positioned against Detector Gap (#6), which measures variants within one pattern.
- NEXT: a fresh adversarial review of the YAML and PR.md, then Tim's OK, then PR branches (Tim's call), one per YAML off upstream main.

## RETAGGED: `nist2026` (2026-10-13). nist-nov-2026 is gone.
- Tim deleted nist-nov-2026 (it had the month wrong) and, instructing mcp-mayhem-48, created an **annotated** `nist2026` (tag object 78e6a04, on commit **75b8862**). Its annotation names all three implementations. The GitHub release was not recreated, so there is currently no release. All three YAMLs and PR.md files now cite nist2026, and all 6 repo links return 200. The commit is unchanged, so nothing needs re-verifying.
- ⚠ Metrology's own slip: a `git fetch --prune-tags` run in mcp-mayhem's clone deleted the stale LOCAL nist-nov-2026 tag. It matched Tim's intent, but it changed another session's refs. Disclosed to Tim. From now on, fetch read-only without pruning.

## Adversarial review 1 of the final YAML + PR.md: REVISE → fixed (2026-10-13)
- B1: "less than 1/n" was unattributed and did not justify n ≥ 100. Now: "n ≥ 100 is a convention: Robbins' bound for abundance data (MSE "less than 1/n", cited in Böhme, 2018) gives an RMSE below 0.1 there, loose against typical values (about 0.03 in the replay)."
- B2: "bounds the probability that the next session shows" overstated it. U_n now counts patterns RECORDED (refused by a logging guard or entered in the register), and failure mode 1 says U_n scales with the recording rate and does not bound unrecorded attempts.
- B3: the real headline looked staged, since two tested guards were added on the measurement day. The Example now says "Real data … informs only item 1: 3 of 3 patterns guarded, two by tests added on the day measured; other values are lower bounds or withheld." PR.md says the same.
- Non-blocking items, all done:
  - The definition matches the code: G needs a guard and test at EVERY entry point where the pattern was observed; a pattern guarded before first observation has no value; refused evidence records are listed among non-observations; batches are "declared".
  - Explanations moved out of the definition into failure modes 5-7. Definition 451 → 392 words.
  - The CI is written "about 0 to 0.0009". "19% of windows" is explicit. The replay is said to "check the implementation, not the method".
  - "(model)" parenthetical removed.
- Kept: the metadata (Safe, Secure & Resilient; Privacy & Security Evaluation, the only fitting TEVV value). STADS stays "27(2), 1-52": Crossref gives pages 1-52 and no article number.
- Validators OK. Total 1001 words; Example 62.

## Adversarial review 2: REVISE → fixed (2026-10-13)
- B1: "An incident with no known session counts toward K and G only" was FALSE, because such incidents feed items 2 and 3 in the code. Now: "counts in items 1-3 but not in item 4."
- B2: the Example looked gamed. Now: "1 of 3 patterns was guarded until the day measured, and 3 of 3 after two tests were added that day; one was blocked within about 18 hours but took at least 52 days to a tested guard."
- B3: the synthetic figures were selective. Now: "close to unbiased but imprecise (RMSE about 70% of its mean) and is withheld in 81% of windows."
- B4: length. 1,001 → 924 words; the definition is 378.
  - The gitRobot-specific list of refusal reasons became "refusals not about the action's safety".
  - The Robbins rationale became "n ≥ 100, a convention". Both reviewers agreed it justified nothing.
  - The reset-estimator sentence was dropped.
- Also:
  - "U_n is an upper bound on the probability".
  - G "declared in a manifest".
  - Failure mode 3 adds the sessionless-incident bias in Q1.
  - Failure mode 5 adds unversioned agent instructions.
  - Failure mode 7 reworded.
  - Lifecycle stage is now Operate & Monitor only.
  - "misbehaving agent that does not adapt to evade them".
  - PR.md: "the worked example is the reference implementation"; item 4 phrased as a count.
- Not changed: STADS pages. The reviewers disagree on the article number (7 vs 4) and Crossref has none, so "27(2), 1-52" stays.

## Adversarial review 3: REVISE → fixed (2026-10-13)
- B1: "two tests were added that day" was wrong. The DC-71 guard itself was new that day (6312942 → b6bae57). Now "two tested guards were completed that day".
- B2: "at least 52 days" was false; the bound is 51.89. Now "at least 51.9 days".
- B3: the "18 hours" did not say what it was measured from. Now "blocked about 18 hours after detection" (hook commit 872811c, 17 h 55 m after detected_at).
- B4: candour. The Example now says "the median and item 4 are withheld".
- Also:
  - synthetic figures marked "conditional on n ≥ 100";
  - failure mode 6 adds that a zero time to guard (detected at fix time) says nothing;
  - failure mode 7 ties restarted windows to the FSE'21 reset estimators;
  - the catalogue-comparison paragraph is cut from usage_details (PR.md keeps it);
  - PR.md: "the worked example runs the reference implementation on a public fixture".
- Not changed:
  - STADS article number: reviewers said 7, then 4, then 7, and Crossref has none, so "27(2), 1-52" stays.
  - Attest exclusion: covered by "refusals not about the action's safety".
- Now 940 words (siblings 802/907); Example 78; validators OK.
- The article "Building NIST Submissions with AI Agents" is a private Claude Docs doc, revised after its own adversarial review. It needs one more fresh review before Tim shares it publicly.

## Final review round (YAML review 4 + article review 2), 2026-10-13
- YAML review 4: REVISE, 1 blocking. "blocked about 18 hours after detection" was unsupported.
  - ZeroParadox 872811c's own message says the hooks were already wired through the ignored settings.local.json. That commit TRACKED them; it did not switch them on. Blocking may predate the incident. Metrology confirmed this read-only from the commit message.
  - INC-0001's detected_at is also the earliest record (ba30b87), not a detection moment.
  - Fixed. The Example now says "one, blocked by a hook committed the day after its first record, waited at least 51.9 days for a replaying test". Item 2 now measures "from the incident's first record".
  - The 51.9-day lower bound still holds: an earlier detection only makes the true value larger.
- Also: "estimates, slightly high, U_n" (Q1/n is unbiased for U_{n-1}); "1 of 3 patterns had a tested guard before the day measured"; synthetic "(19% of windows, 64% of sessions)", "near-zero absolute bias". 945 words; Example 78; validators OK.
- ⚠ The TAGGED example README (nist2026, line 98) says the hook "has blocked every direct git call since 2026-08-23T14:22:18Z, about 18 hours after detection". "Since" is literally true, but "about 18 hours" implies a start time. Fixing it needs a new commit and re-tag (Tim's call). Reported to Tim and mcp-mayhem-48; not fixed.
- Article review 2: REVISE, 3 blocking, all fixed:
  - the table row now says "two of those guards and their tests were completed";
  - "Ten of the errors caught and logged are below";
  - "caught mostly by structure".
  - Also applied: the same hook correction, the regex row now caught by "Self-check of the first pass", the tag rule reworded, and the diagram caption and title no longer claim "nothing crosses without a receipt".

## 2026-10-13: README line-98 fix (mcp-mayhem 875646f, untagged)
Verified read-only: README-only diff (7+/6-) from 75b8862. The 18-hour claim is removed; wording now matches the YAML Example (hook committed day after first record, 872811c, may have blocked earlier; >=51.9 days to replaying test 5bf7106, merged as 283157b). mcp-mayhem-48 reports 65 tests pass, fixture and expected_report unchanged. Goes into the single re-tag after Tim's data refresh. Refresh plan from mcp-mayhem-48: rerun make_fixture with the same salt, regenerate the README real-output block from a real run, recheck README prose numbers (session counts, n).

## 2026-10-14: UNIT CHANGED to agent instance (subagent), Tim's decision
**Why (Tim):** ZeroParadox sessions are intentionally long-lived and run many independent subagents; "the longer running sessions you're way more likely to run into weird s***", which is why the work is split into subagents. Counting sessions pools them; 100 sessions in a fixed version window would take months.
**Evidence (read-only, 2026-10-13/14):**
- git_ops.jsonl: all declared-agent-client rows (claude-code) are ONE gitRobot session, 9e7c8522..., across the whole day. A /clear in ZeroParadox started a new conversation (ad237cd6...) but gitRobot kept the same MCP session id: /clear is invisible to the guard layer.
- gitRobot http_calls.jsonl requests carry _meta."claudecode/toolUseId". Each id appears in exactly one transcript (main or subagents/agent-*.jsonl), so call -> agent instance is a join. Spot-checked: toolu_011nSgu5... -> one subagent; the 4 calls after /clear -> ad237cd6 main.
- Session 16e1d86f: 574 gitRobot tools/call (15:02-01:55 UTC); 514 mapped; 60 ids not yet in any transcript; 161 units (160 subagents + main); calls per unit median 2-3, max 19; 471 reads; 0 refusals; one version window. Q1 = 0, so U-hat would be 0 over ~160 instances.
- un_id is a gate-run attestation id, NOT an agent id.
- Script: scratchpad/subagent_units.py (one conversation dir; must be widened to all transcripts of the project). Snapshot of the rotating http_calls logs (28 MB, private) at scratchpad/snapshot-2026-10-14/.
**Options considered:** calls (Tim's first idea; retries make Q1 optimistic, needs a collapse rule) vs subagent (fresh context, absorbs retries, matches deployment). Subagent chosen.
**Done here (drafts only):** YAML Unit / items 3-4 / failure modes 3-4 rewritten for agent instances; DRAFT banner in YAML and PR.md.
**Still PENDING before the YAML can be submitted:**
1. Change request to mcp-mayhem-48 (NOT yet sent; needs Tim's approval there): log toolUseId into the append-only git_ops (http_calls rotates ~1 day), the call->instance join over all project transcripts, estimator unit switch, fixture regen (anonymised instance ids), synthetic replay, tests, README.
2. Tim cuts one tag (also picks up README fix 875646f). Verify from clean export; repin all three.
3. Rewrite the Example (synthetic figures are session-based) and PR.md maturity; the long-lived-session sentence; 'release tag' -> 'tag'.
4. Fresh adversarial review; Tim's OK.

## 2026-10-14 evening: first real policy-refusal observation; reference implementation run on live logs
**Run:** clean `git archive` of mcp-mayhem 875646f (guardCoverage/), `python -m guard_coverage measure` on the LIVE `.mcp-local/gitRobot/git_ops.jsonl` + `.mcp-local/incidents/incidents.json` + the fixture manifest. As of 2026-10-14T22:46:58Z:
- inputs: 7896 audit rows; 1 policy-refusal observation, 5 incident observations; 1 agent session (session unit).
- item 1: |G|/|K| = 3/4. NEW pattern `gitrobot.worktree-target.any` (gitrobot-mcp/cli), unguarded: "no regression test declared for it at gitrobot-mcp/cli", age 0.01 days.
- item 2: unchanged (>=51.89, >=0.00, >=8.67 days; median withheld).
- item 3: batch 1 (1 session, partial): 1 new.
- item 4 (sessions): W1 2026-10-13T15:02:32Z .. 22:46:58Z, n=1, Q1=1, Q2=0, withheld.
- skipped non-policy refusals: allowlist 3, gate 2, operational 4 (these are NOT observations, by the implementation's own rule `refusal_class != "policy"`).
**The refusal:** 2026-10-14T22:31:23Z, op worktree.target, class policy: an agent passed `worktree=C:\Workspace\ZeroParadox\.claude-local`, which git does not list as a worktree. gitRobot: it "will not accept a path git has not vouched for, because that is the general-proxy hole the repo modes exist to close." Made by the MAIN agent of conversation ad237cd6 (join), not a subagent. Its occurrence time is KNOWN (logged refusal): if a regression test is declared later, it gives the first EXACT time-to-guard value. If gitRobot already has such a test, guarded_at precedes the first observation and the pattern has no value (definition). Which one is for mcp-mayhem-48 to establish; NOT asked yet.
**Subagent unit (scratch join, scratchpad/subagent_units.py, merged http_calls snapshot):** same span 15:02:31 .. 22:46:58; 1307 agent-client calls, all with toolUseId, all mapped; 286 instances = 3 conversations (16e1d86f 185 incl. 184 subagents; ad237cd6 96 incl. 95; 598417dc 5 incl. 4) = 283 subagents + 3 mains; one gitRobot session; one version window (gitRobot f813216, Claude Code 2.1.286). Q1 = 1, Q2 = 0 -> U-hat = 1/286 = 0.0035. The script's own refusal detection from http_calls is NOT reliable (substring heuristic over-counts); refusals were taken from git_ops (authoritative).
**Docs updated (drafts):** YAML Example rewritten with these numbers + banner saying where each number comes from; guard-coverage PR.md maturity bullets (unit rationale; thin data); all three PR.md "release tag" -> "tag"; EC PR.md primary-spec wording and reference naming (Gligoric et al./Ekstazi, Torres-Arias et al./in-toto). These text changes need the fresh adversarial pass before posting.

## 2026-10-15: change request sent to mcp-mayhem-48 (awaiting Tim's approval there)
- Request: per-call client id logged durably (reads included); unit = agent instance via toolUseId -> transcript; backfill or forward-only (their call); anonymised fixture ids; synthetic replay relabelled; tests/README; NO tag (Tim cuts one covering this + 875646f).
- Item 7 answered by mcp-mayhem-48, VERIFIED here read-only: gitRobot/tests/test_worktree_target.py::test_a_path_git_does_not_list_is_refused exists at 75b8862, introduced c46a0c5 (2026-09-03T11:54:35-05:00). Declared in the manifest, gitrobot.worktree-target.any becomes guarded BEFORE first observation (no time-to-guard value) -> 4/4.
- OPEN replay question sent: the observed action was a READ with worktree = `.claude-local` (a nested git repo); the test STAGES into a plain temp dir. Consistency with the INC-0001 ruling needs a stated judgement on whether the test replays the pattern.
- Consequence for drafts: the YAML Example's "the fourth ... has no regression test yet" is WRONG in substance (the test existed, undeclared). Regenerate at the refresh. The article was corrected (rev 38) and gained a row (14 errors).
- 2026-10-15 replay question RESOLVED: mcp-mayhem-48 judged that the test replays the pattern; verified here (`_target` at 875646f, engine.py:282+, refuses only on `resolved not in _worktree_paths()`, independent of the tool and of repo vs plain dir; the same guard and entry point, unlike INC-0001). Its "reason 4" (a policy refusal means the guard held, so dating G from a later test would be fabricated) REJECTED: it contradicts the definition (time to guard runs to guard AND test; INC-0001 precedent), and I asked for it to be left out of the commit message. Optional literal test (read with worktree = a nested repo): Tim's call; it does not change guarded_at, because the existing test predates the observation.

## Implementation of the unit change VERIFIED (2026-10-15): mcp-mayhem 627b69b (untagged)

mcp-mayhem-48 pushed 34713d5 (gitRobot tool_calls.jsonl, client_call_id on every audit row; live since the restart at 2026-10-15T18:02:10Z) and 627b69b (guardCoverage, unit = agent instance; item 7 declared). Verified from a clean `git archive 627b69b` in the scratchpad (`v627/`):
- guardCoverage: 114 passed. The real `measure` output reproduces their quoted block exactly: 4/4; worktree-target "guarded before first observation (41.23 days earlier)"; median withheld; item 3 has 404 instances; item 4 W1 n=301, Q1=1, Q2=0, U_hat 0.0033; 103 instances in no window; 5 incidents excluded from item 4.
- Fixture CHECKSUMS OK. Instance, call and session ids are salted hashes, with no toolu_ ids, paths or conversation ids (grep). The manifest declares `test_a_path_git_does_not_list_is_refused` at c46a0c5, guarded_at 2026-09-03T16:54:35Z, with the note giving reasons 1-3 only.
- gitRobot: 548 passed, 13 skipped. Two tests could not run in my venv because anyio, the MCP server dependency, is missing (an environment gap, not a failure). So their count of 586 is NOT independently confirmed.
- **My earlier figures were wrong in three places, and their corrections were confirmed:**
  - The merged snapshot holds 127 duplicate agent calls (same ts, session, rpc_id and toolUseId on adjacent lines; e.g. toolu_01RUG31jx3tGuWWWfoyKhzcV at lines 15162-3).
  - 3 toolUseIds sit in 7, 7 and 4 subagent transcripts of ad237cd6 (forked history), so they are ambiguous.
  - My script's `owner.setdefault` assigned them arbitrarily. The true count is 285 instances (282 subagents) in my window, not 286.
- The gap from 2026-10-14T22:46:58Z to 10-15T10:32:14Z rotated out of http_calls before anyone copied it. Those 76 claude-code audit rows have no instance.
- The 301 window figure is W1 from 2026-10-13T15:02:31Z to 10-15T14:19:44Z, from the public fixture. The YAML Example and PR.md now use it, along with 4/4 and "guarded before first observation". The synthetic share now says "64% of instances" (63.6%). The RMSE of 0.0180 against a mean of 0.0262 is 69%, so "about 70%" stands.
- NEXT: Tim cuts the tag (it covers 875646f, 34713d5 and 627b69b). Then re-verify at the tag, repin all three YAMLs and PR.mds, remove the banners, run the adversarial review and get Tim's read.

## Repinned to nist2026.1 (2026-10-15)

Tim had mcp-mayhem-48 cut annotated tag `nist2026.1`: object 650f4148, commit 627b69bba094cb41e7e7bd67d20ffdc5079cfcd0. `nist2026` is unchanged (75b8862).
- Checked with ls-remote and a local fetch (without --prune-tags).
- A `git archive nist2026.1` export is identical to the verified 627b69b export, ignoring caches.
- Tests from that export:
  - guardCoverage 114/114;
  - inventoryFidelity 86/86;
  - gitRobot 586/586 (their count, now confirmed);
  - verdictLedger 651/652, the known CRLF-on-Windows-export control.
- verdictLedger and inventoryFidelity have no diff from 75b8862 to 627b69b.
- Test environment: the server tests need the `mcp` extra. Its declared `mcp>=1.2` resolves today to mcp 2.x, which lacks `mcp.server.fastmcp`, so a fresh install fails collection. The tests pass with `mcp<2`. Reported to mcp-mayhem-48. It does not affect the metric implementations, which use only the standard library.
- All three YAMLs and PR.md files are repinned (links /tree/nist2026.1/…; tag and commit in PR.md); the six links return 200. The DRAFT banners are removed, and schema and inspect validation pass for all three.
- NEXT: a fresh adversarial review of the GC YAML and PR.md and the EC and IF PR.md changes, then Tim's read and OK.
