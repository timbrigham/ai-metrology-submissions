# Candidate: inventory fidelity (working name)

**Status:** idea. Implementation read on 2026-10-09. Overlap and reference check running.

## The metric (draft wording)
- Keep a registry of the exact objects an AI system consists of or depends on: models, datasets, prompt templates, tool definitions, guardrail configs.
- Reconcile it against a scan of the actual artifact, by identity, and report each count separately, never merged:
  - **matched**: registered and present;
  - **phantom**: present, not registered;
  - **vanished**: registered, not present;
  - **resurrected**: retired, now present again.
- Mismatches are flagged, never silently resolved. A rename with no recorded rename shows as one vanished plus one phantom.
- Fidelity: matched / registered and matched / present.
- This supplies the trusted denominator for evidence currency. See evidence currency's failure mode 2.

## Implementation: SJV / structuredJsonValidator (mcp-mayhem, public, MIT)
- `reconcile` (`structuredJsonValidator/consumers/lean/operations.py:264`) already returns a drift summary with:
  - `matched` (count);
  - `vanished`, `phantom` and `resurrection` (lists).
- Identity is the fully qualified name, and file/line are location only, so a moved object is an update, not a drop-and-add.
- An unrecorded rename is deliberately left unguessed: it is flagged as vanished plus phantom.
- The registry itself is a schema-enforced flat JSON file with operation-mediated writes and an append-only SHA-256 hash log, so drift from an out-of-band edit is detectable.

**Gaps for a NIST example:**
1. **Lean-specific.** `reconcile` lives in the Lean consumer, and its scan input is Lean declarations. An AI version needs a general object type, or an AI-asset consumer.
2. **It writes.** `reconcile` mutates the registry: phantoms are added as `pending`. Measuring needs a read-only variant that returns the summary without writing. No dry-run exists for reconcile; one exists only for `annotate_by_filter`.
3. **No AI scanner.** Something has to enumerate the AI objects in an artifact (prompt files, tool definitions, model references in config, dataset pointers).
4. **No single-number output.** The ratios are not printed today.

## Overlap and references
Pending the research agent.
