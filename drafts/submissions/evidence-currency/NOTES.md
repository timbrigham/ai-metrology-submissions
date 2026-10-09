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

## References (researched 2026-10-09; quotes read in the full-text PDFs)
No peer-reviewed source defines this exact measurement. The two below establish the principle: a recorded result is valid only while the hashes of its exact inputs are unchanged.

1. **Gligoric, Eloussi & Marinov, "Practical Regression Test Selection with Dynamic File Dependencies," ISSTA 2015, ACM.** https://doi.org/10.1145/2771783.2771784
   - DOI checked in Crossref.
   - "For each test entity, Ekstazi checks if the checksums of all used files are still the same. If so, the test entity is not selected." (§3)
   - "Our insight is to view RTS as memoization: if none of the dependent files for some test changed, then the test need not be run." (§7)
   - "Ekstazi tracks even files that were attempted to be accessed but did not exist" (§7). This bears on never-examined content.
2. **Mokhov, Mitchell & Peyton Jones, "Build Systems à la Carte," Proc. ACM Program. Lang. 2(ICFP), Art. 79, 2018.** https://doi.org/10.1145/3236774
   - DOI resolves.
   - "4.2.2 Verifying Traces. An alternative way to determine if a key is dirty is to record the values/hashes of dependencies used last time, and if something has changed, the key is dirty and must be rebuilt — in essence a trace which we can use to verify existing values."
   - Verified in the extracted text.
   - The JFP 2020 extended version's DOI is NOT verified. Cite the ICFP one.

**AI-specific alternate:** Schnabl, Hugenroth, Marino & Beresford, "Attestable Audits," arXiv:2506.23706.
- An ICML 2025 workshop paper (TAIG), not main track.
- It binds benchmark results to model, code and data hashes, but has no staleness counts.

**Rejected:**
- in-toto (USENIX Sec 2019): tamper detection, a single pass/fail.
- RTSLinux (FSE 2017): redundant with Ekstazi.
- Nix/Dolstra: not fetched.
- SLSA: not peer-reviewed.
- Several arXiv preprints: verified at snippet level only.

**Candour sentence (draft):** "No peer-reviewed source we know of defines this exact measurement. Regression test selection (Gligoric et al., ISSTA 2015) and build-system verifying traces (Mokhov et al., ICFP 2018) establish the underlying principle: a recorded result is valid only while the checksums of the exact content it was computed on are unchanged. Evidence currency applies that per-result validity predicate at decision time and reports the counts (current, stale, never examined, not applicable) separately rather than as one pass rate."

## Still to do before drafting the YAML
- [x] References.
- [ ] Decide the exact number(s) the YAML defines.
- [x] Gaps 1–3 fixed by mcp-mayhem-48 in `8207aa5f08b66632b07f2d52130664a49daee05c` (on origin/main).
  - Verified here on 2026-10-09 from a clean `git archive 8207aa5`:
    - `python -I examples/evidence-currency/run_example.py` exits 0, with 4 scenarios: 100% → stale 75% → never-examined 60% → re-checked 80%;
    - the JSON includes a `definition` string;
    - tests: 645 passed, 1 failed. The failure is CRLF from the Windows export, which is environmental.
  - YAML links:
    - https://github.com/timbrigham/mcp-mayhem/tree/8207aa5f08b66632b07f2d52130664a49daee05c/verdictLedger/examples/evidence-currency
    - https://github.com/timbrigham/mcp-mayhem/tree/8207aa5f08b66632b07f2d52130664a49daee05c/verdictLedger
  - Command, run from verdictLedger/: `python -m core.cli --repo <repo> --data <records.jsonl> evidence-currency --ref HEAD [--json]`
  - Caveats the YAML must state:
    - it needs a full checkout of mcp-mayhem, not a pip package;
    - it counts RECORDED verdicts and does not re-run them;
    - a current FAIL counts as current, so this is not a pass rate;
    - editing a checker does not make its verdicts stale;
    - per-step `status` can read SATISFIED while currency < 100% (never-examined is reported, not blocking), so the YAML must not use `status` as the metric.
- [ ] Draft the YAML. Then a separate adversarial review, then Tim's OK.
