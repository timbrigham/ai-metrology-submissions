# Candidate: verified agent containment (working name)

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

## Overlap and references
Pending the research agent.
