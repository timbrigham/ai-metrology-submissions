# drafts

Working folder for contributions to NIST's AI Metrology Center intake: https://github.com/usnistgov/ai-metrology-submissions. Everything here is a draft. Nothing is posted until Tim approves it, and Tim posts it himself.

This folder lives on the `drafts` branch of Tim's fork.
- It is pushed to Tim's own fork, which is public but is not a submission. Nobody at NIST is notified unless a PR is opened.
- **Never open a PR from this branch.** A submission PR must add exactly one YAML file under `submissions/`.
- To submit, cut a fresh branch from `main` (for example `git switch -c submit/<name> main`), copy the one YAML into `submissions/`, and push only that branch.

## ▶ RESUME HERE: current state (updated 2026-10-10, end of session)
| item | folder | state | next action |
|---|---|---|---|
| **Evidence Currency** | `submissions/evidence-currency/` | **SUBMISSION-COMPLETE.** YAML + PR.md final, pinned to tag `nist-metrology-2026-10` (= 97d2988), verified, both validators pass | Wait for NIST's clarification, then Tim opens the PR (procedure below) |
| **AI Inventory Fidelity** | `submissions/inventory-fidelity/` | **SUBMISSION-COMPLETE.** Revised for multi-source, continuous reconciliation and independence of sources (Tim, 2026-10-10); pinned to the same tag; validators pass | Same. Optional: one more review round on the last one-line independence addition |
| Incident-Driven Guard Coverage | `submissions/guard-coverage/` | PARKED. Design v1 + refs verified (STADS TOSEM'18, FSE'21), data audit done; no YAML | Wait for instrumentation data (items 1, 2, 4 in progress in mcp-mayhem-48). Then a YAML, an example (read-only tool over the gitRobot log + incident register), and reviews |
| Recurrence response | `submissions/recurrence-response/` | PARKED. Design v2 (implementation-declared shape taxonomy + effectiveness arm) + refs verified (Bouzenia & Pradel ASE'25, SWE-agent NeurIPS'24; MIRAGE-Bench as prior art); data audit done | Needs a SPECIFIC failure signature (not "Exit code N") and data: Claude Code transcripts now kept 365 days. Then an example script, a YAML, reviews. Strongest TEVV fit of the four |
| #19 comment | `comments/pr19/` | SHELVED (#19 was rejected by NIST pending clarification) | Tim to revisit |
| Ideas only | (none) | claim coverage; NL-to-formal faithfulness | Not started |

**Open external dependencies:**
- NIST's promised clarification (hbooth on #19, 2026-10-09). None as of 2026-10-10. Tim declined a scheduled check, so look only when asked.
- Instrumentation (after the tag; item 3 dropped):
  - **Item 1 DONE and VERIFIED** at mcp-mayhem abdb679 (2026-10-10): `surface` (mcp | cli | internal) + `session` on every git_ops row, always present and null when unknown. Logging-only (tiers.py untouched; thread targets wrapped with a context copy); 545/545 gitRobot tests at a clean export; live log confirmed (first row: reaper, surface=internal). ⚠ Rows before abdb679 lack both keys: absent means "before the field existed", NOT unknown.
  - Items 2 (refusal_class) and 4 (SJV incident register): pending in mcp-mayhem-48. Verify each is logging-only when its SHA arrives.

**Submission procedure (Tim posts):** for each metric, cut a fresh branch from upstream `main`, copy that ONE YAML into `submissions/`, push it to the fork, and open the PR to usnistgov with that folder's `PR.md` as the body. Tim confirms the two checklist commitments (self-check, will follow the PR).

**Scope caveat recorded 2026-10-10:** NIST's scope is AI TEVV. Evidence Currency fits as a check on TEVV evidence. Inventory Fidelity fits as configuration verification. The parked two are the most central (they evaluate agent behaviour or safety controls).

## Rules for anything leaving this folder
- Run a separate adversarial review in a fresh instance, then get Tim's explicit OK.
- Lead with the checkable artifact. No branded or ontology vocabulary. Disclose when code is Tim's own.
- Call it "independent review" or "replication evidence", not "peer review".
- Verify every citation and link at the source.

## Layout
- `comments/prNN/`: a comment on an existing PR. Holds `comment.md` (the text to paste), `NOTES.md` (status, evidence and review findings), and any harness.
- `submissions/`: candidate new YAML files, plus a notes file for each.

## Index

| item | target | status |
|---|---|---|
| `comments/pr19/` | #19 paired-control non-measurement | SHELVED (Tim, 2026-10-09). #19 was rejected by NIST pending clarifications; Tim will revisit |
| (none) | #20 tool-descriptor mutation | decided not to comment: the gap is the submitter's own implementation |
| `submissions/evidence-currency/` | new: evidence currency (verdictLedger) | SUBMISSION-COMPLETE (see RESUME HERE) |
| (none) | new: NL-to-formal claim faithfulness | idea only |
| `guard-coverage/` | was: verified agent containment (claimed-restriction verification). SUPERSEDED on 2026-10-10 by Incident-Driven Guard Coverage, see the status table | superseded / parked |
| `submissions/inventory-fidelity/` | new: AI inventory fidelity | SUBMISSION-COMPLETE (see RESUME HERE) |
| `submissions/recurrence-response/` | new: recurrence response | PARKED (see RESUME HERE) |
| (none) | new: claim coverage (Tim, 2026-10-09). Of the claims a project publishes (model card, system card, assurance case), the fraction bound to a gate that checks them. It is the link upstream of evidence currency | idea only. Needs a prior-art check (requirements traceability, assurance cases / GSN) and code that computes it |

## Framing (Tim, 2026-10-09)
CI gates are the proof that what we claim is what we do. The chain:
0. an inventory of the exact objects, reconciled against reality (SSOT via SJV; inventory fidelity, idea). It supplies the denominator for everything below;
1. claims, bound to gates (claim coverage, idea);
2. gates that are shown to work (seen to fail on a control: the #19 comment), shown to have run (audit log including clean passes) and that cannot be routed around by an agent (gitRobot capability removal: Incident-Driven Guard Coverage, parked);
3. evidence that is still current for the bytes shipped (evidence currency).

Lead with the AI-accountability version: "are your published claims (model and system cards, assurance cases) still backed by evidence about what you are releasing?"

## Decisions (Tim, 2026-10-09)
- Submitter: `Tim Brigham (independent researcher)`. 6 of 13 open PRs are by independents, so there is precedent.
- Contact: `timbrigham@gmail.com` (changed 2026-10-09: the zeroparadox.org homepage reads 'A machine-verified mathematical ontology', a triage trigger for NIST reviewers).
- (HISTORY) Tagging: ONE mcp-mayhem tag, created only once all three candidate examples (evidence currency, inventory fidelity / SJV, agent containment / gitRobot) are done and verified. Then every YAML is re-pinned to that tag.
  - DECIDED (Tim, 2026-10-10, in mcp-mayhem-48's session): "Drop containment". The tag covers evidence currency + inventory fidelity ONLY, created on metrology's request after final verification. Guard coverage and recurrence response stay parked.
- Still one PR per metric. NIST's check requires exactly one file under `submissions/` per PR. The three PRs can be opened together.

## NIST change on 2026-10-09: conciseness is now a criterion
- hbooth on #19 (2026-10-09 18:32 UTC): "Rejected and Please Resubmit after we have provided additional clarifications regarding what we are looking for … clear and concise descriptions of the submitted metric such that it can be understood, with minimal effort on the part of a human reader." The PR is still open.
- Consequences:
  - Our #19 comment is ON HOLD. The PR is effectively rejected, so evidence there now has little value.
  - All three YAMLs need a conciseness pass. #19 was about 540 words when rejected.
  - WAIT for NIST's promised clarification before submitting anything. This fits the one-tag plan.

## (HISTORY) Status at 2026-10-09: superseded by RESUME HERE
| submission | YAML | example | verified by metrology |
|---|---|---|---|
| evidence currency | trimmed, final fact-check passed | verdictLedger @ 6a8d029 | yes (clean export) |
| AI inventory fidelity | rev 3, aligned to code | inventoryFidelity @ 77c6d09 | yes (clean export: exact numbers, 86 tests, stdlib only) |
| Incident-Driven Guard Coverage (`guard-coverage/`, formerly agent containment) | PARKED: design v1 + refs verified; no YAML | not built | no |
| Recurrence response / repeated-failure adaptation (`recurrence-response/`) | PARKED: design v2 + refs verified; no YAML | not built | no |

Before the tag: Tim's decision on the open tagging question above, a joint final adversarial review, NIST's clarification, and a maturity note in each PR description. Then re-pin the links to the tag.

## Framing rules from Tim (2026-10-10), apply to every submission
- **Proportionate threat model:** best effort against an agent that misbehaves but is not ill-intentioned. Covering the top few common patterns is enough. Never imply completeness; state the scope, e.g. the attempts listed.
- **Proof of concept:** the reference implementations are single-author proofs of concept built for one dedicated environment, not production or complete tools. The metrics can be general, but the implementations' scope must be stated plainly. All three YAMLs carry the same sentence.

## 2026-10-10 update
- mcp-mayhem 78dd222: scope statement added to the root README and both example READMEs. Verified here from a clean export, and both examples' numbers are unchanged.
- Tim approved the source-comment tone pass in verdictLedger/core. It is mcp-mayhem-48's work.
- Containment (Part B) is NOT being built. It was reframed, renamed Incident-Driven Guard Coverage, and PARKED.
- gitRobot `-n` false refusal: confirmed by mcp-mayhem-48 (also 8). Tim approved the narrow fix: `-n` for log/grep, `--git-dir` for rev-parse, and grep added to the read allow-list. It does not touch either submission's code.
- Classification-rule sensitivity, demonstrated: the same log gave 62 keys / 43 singletons under metrology's normalisation and 44 / 26 under mcp-mayhem-48's.

## Framing: security operations applied to AI agents (Tim, 2026-10-10)
Tim: "This is honestly turning into a cyber security concept... Effectively this is auditing and responding to an audit log."
| security practice | our piece |
|---|---|
| audit logging | gitRobot git_ops, MCP http_calls, session transcripts |
| log integrity / retention | verdictLedger tamper detection; retention audit (Claude Code `cleanupPeriodDays` raised from 30 to 365 on 2026-10-10) |
| detection | guards and hooks that refuse risky actions |
| incident response / post-mortem | incident becomes guard plus regression test (the `+branch` force-push) |
| detection coverage, time to remediate | Incident-Driven Guard Coverage (parked) |
| false-positive rate | the `-n` and `grep` false refusals |
| control validation | "a gate never seen to fail is a hypothesis"; the #19 paired-control comment |
| asset inventory | AI Inventory Fidelity |
| audit-evidence freshness | Evidence Currency |
The log-hygiene findings from the 2026-10-10 audit are classic audit-log issues: rotation erasing history, no session id, incidents only as prose. ("Test traffic in production" was a misreading: those records are real lane-worktree operations.)
Possible use: one line in the PR descriptions, and the organising idea if the parked candidates are revived. It also fits the best-effort stance: security operations measures detection and response, never "stops everything".
- Tag name APPROVED by Tim (2026-10-10): `nist-metrology-2026-10`, created only on metrology's request after verification. It goes on the commit carrying the verdictLedger comment-tone pass plus the new `inventoryFidelity/README.md` (one SHA, pending). Then add package-level links (`verdictLedger/`, `inventoryFidelity/`) beside the example links, and re-pin both YAMLs and PR.md (`TAG_TBD`).
- Instrumentation APPROVED by Tim (2026-10-10, Q&A): (1) `session` + `surface` on every git_ops record; (2) `refusal_class` (policy / gate / operational / allowlist) set at the refusal site; (3) a fixture guard so tests can never write the production log (PREMISE CORRECTED: the suspected test records are real lane-worktree work, and tests already don't write there; Tim DROPPED item 3 on the corrected premise, 2026-10-10); (4) incident register as an SJV collection, seeded with the known incidents. Spec sent to mcp-mayhem-48. It lands AFTER the tag, never bundled with the tagged commit. Purpose: data for the parked guard-coverage and recurrence-response metrics.

## SUBMISSION-COMPLETE (2026-10-10)
- mcp-mayhem tag `nist-metrology-2026-10` → commit 97d298887973566381768b61a8b748f84970c44f. Verified by metrology from a clean export: both examples exact, tests pass (inventoryFidelity 86; verdictLedger 651/652, the 1 being CRLF from the Windows export), and the tone pass is AST-identical. Remote tag checked with ls-remote, and all four links return 200.
- Both YAMLs link example + package at the tag; both PR.md files state tag + commit. Both pass check-jsonschema and inspect.
- Remaining: (1) NIST's promised clarification (none as of 2026-10-10); (2) Tim's go. Then, per submission: a fresh branch from upstream main, copy the ONE YAML into `submissions/`, push to the fork, open the PR to usnistgov with PR.md as the body. Tim posts.
