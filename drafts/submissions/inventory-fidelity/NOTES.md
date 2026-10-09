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

## Overlap (research agent, 2026-10-09)
**Verdict:** CLEAR in the catalogue and ADJACENT to open PRs. Not a duplicate.
- Catalogue: 147 entries read, and nothing matches inventory, registry, SBOM/AIBOM, provenance, lineage, configuration or reconciliation. The keyword scan was done by the small model, and the collapsed reference sections were not read.
- **#14** (adverse-action traceability) is closest in spirit. It is a qualitative, record-level reconciliation in a single domain (credit), tracing outputs to their declared sources.
- **#20**: detector sensitivity for a single pinned object.
- **#16**: log integrity, so different.

## References (I checked the starred quotes in the extracted text myself)
1. ★ **Balliu et al., "Challenges of Producing Software Bill of Materials for Java," IEEE Security & Privacy, 2023.**
   - DOI 10.1109/MSEC.2023.3302956 (Crossref, per the agent).
   - "The precision is the share of dependencies in the SBOM that are correct with respect to the ground truth."
   - Dependencies are "identical if their name and version match precisely".
   - Checked in arXiv 2303.11102v2. The two-column extraction interleaves the lines, but the words are present. Re-check against the published version before citing.
2. ★ **Yu, Song, Hu, Yin, "On the Correctness of Metadata-Based SBOM Generation: A Differential Analysis Approach," DSN 2024.**
   - DOI 10.1109/DSN58291.2024.00018.
   - "...the differences between the reported libraries and the ones actually installed." The phrase "the ones actually installed" is confirmed in the extract.
3. **DeHoratius & Raman, "Inventory Record Inaccuracy: An Empirical Analysis," Management Science 54(4), 2008.**
   - DOI 10.1287/mnsc.1070.0789.
   - Only the abstract has been seen, and the paper is about retail. It is the classic study of recorded versus physical inventory.

**Relevance (governance, so it cannot be cited as grounding):**
- ★ AI RMF GOVERN 1.6, verified verbatim: "Mechanisms are in place to inventory AI systems and are resourced according to organizational risk priorities."
- SP 800-218A N1 says "AI models and their components may need to be added ... to an organization's asset inventories". This quote is from the agent and not yet checked by me.
- NIST asks organisations to keep an inventory, but never says how to measure whether it is true. That gap is the pitch.

**Draft candour sentence:** "No peer-reviewed work we found defines this metric for AI-system inventories. The references establish the underlying measurement, identity-keyed precision and recall of a claimed component list against observed ground truth, in software supply-chain and retail-inventory settings. The AI-object scope and the separate outcome classes are our extension."

## Reviewer's blunt view (adopted)
- As drafted, this is SBOM precision and recall under new names. Name the mechanism honestly: matched / registered = **inventory precision**, matched / present = **inventory recall**. Claim only the AI-object scope and the class breakdown as new.
- ⚠ **Name-only identity is a validity hole.** A prompt or model file swapped under the same name counts as "matched", and that is exactly the AI supply-chain failure that matters.
  - Fix: key identity on name AND content hash, and add a class **matched-by-name, content changed**.
  - This ties directly to evidence currency's (path, blob) binding. The same idea at the inventory level: verdictLedger's binding could supply it.
- Lead with "make GOVERN 1.6 measurable: does the AI inventory describe what is actually deployed?" The thing measured is the inventory process, not the model.
- A worked example on a real AI artifact (an agent repo's prompts, tools and model references) is mandatory. Without one, it reads as Lean bookkeeping relabelled.
