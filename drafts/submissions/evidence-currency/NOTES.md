# Candidate: evidence currency (working name)

**Status:** feasibility checked on 2026-10-09. No YAML yet.

## The metric (draft wording)
- A decision (merge, push, ship) relies on gate verdicts.
- Each verdict is bound to the content it judged: (step, path, git blob id).
- At decision time, report how many in-scope subjects each step has **current** evidence for.
- Report three things separately, never merged:
  - **stale**: examined, but the content has changed since;
  - **never examined**;
  - **not applicable**.
- The failure it targets: a pass recorded on old bytes still counts after the content changes.

## Implementation: verdictLedger (mcp-mayhem, public, MIT)
- Repo: https://github.com/timbrigham/mcp-mayhem, folder `verdictLedger/`.
  - The logic is public. The ledger data (`.mcp-local/`) is not tracked.
- Packaging: `pyproject.toml`
  - zero declared dependencies, and `mcp` is optional;
  - CLI `zpledger`, MCP server `zpledger-mcp`.
- Statuses (`core/inventory.py:17-18`): SATISFIED, STALE, MISSING (never examined), NOT_APPLICABLE, FAIL/UNDECIDED.
- Per-step counts in `inventory.build`: `subjects_covered`, `subjects_stale`, `subjects_unexamined`, `scope`.
  - The rate is a sum over rows. **Nothing outputs it as one number today.**
- Test run on a clean `git archive` export, 2026-10-09: **634 passed, 4 failed**.
  - The failures look environmental or cross-server, not core logic:
    - CRLF on disk after export;
    - two MCP-conformance tests that expect all three servers;
    - one test bound to gitRobot's vocabulary.
- **Gaps a NIST reviewer would hit:**
  1. **Undeclared dependency.** `core/errors.py:22` imports `mcpcommon` (a sibling folder), but `pyproject` declares `dependencies = []`. A bare install fails at import.
  2. **No single-number output.** The reviewer will want "actually computes the metric". Fix: add a CLI subcommand or a documented recipe.
  3. **No worked example on a non-ZeroParadox repo.** The config (`required.v2`) is shaped around ZeroParadox's gates.
     - A minimal sample config plus a toy repo would show it is usable today.
  4. The README style (⚠⚠, "Tim's call", internal IDs) is the same crank-signal risk as the ZeroParadox repo.
     - A NIST reviewer will click through, so the YAML should link the code, not the README.

## Overlap check (subagent, 2026-10-09): ADJACENT, not a duplicate
- **Catalogue:** about 146 entries read, none on staleness, freshness, provenance, attestation, audit trail or evaluator/gate validity.
  - Caveat: items behind "Show N more" toggles may have been missed.
- **Open PRs to distinguish explicitly:**
  - **#16 audit-trail tamper detection.** Its target is malicious edits to the log. Ours is honest content change silently invalidating a verdict that is still valid.
  - **#20 tool-descriptor mutation.** It measures a pin's field coverage. Ours measures how current the evidence behind a decision is.
  - **#23 cross-carrier non-measurement fidelity.** It shares "never examined is not a pass", but has no content binding and no staleness.
  - **#19 paired control** and **#22 judge health** are about evaluator validity, not evidence currency.
  - #21 is unrelated: it is a premise audit, and its hash is only a certificate.
- I have not read #23 in full myself.

## Still to do before drafting the YAML
- [ ] References: 1–2 sources on the METHOD.
  - Candidates to search: build systems that key results on content hashes (Bazel, Nix, "build systems à la carte"), and in-toto/SLSA attestation binding to a digest.
  - Every one must be verified at the source.
- [ ] Decide the exact number(s) the YAML defines.
- [ ] Fix gaps 1–3 in mcp-mayhem (Tim's repo, so his call).
