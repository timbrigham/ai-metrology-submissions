## Metric submission

AI Inventory Fidelity measures whether an organisation's inventory of an AI system's components (prompts, tool definitions, guardrail configurations, model and dataset digests) describes what is actually deployed. It reconciles the inventory against a scan of the deployment by name and content hash, and reports inventory precision and recall.

## Checklist

- [x] This PR adds **one** YAML file under `submissions/`, following
  [SUBMISSION_FORMAT.md](https://github.com/usnistgov/ai-metrology-submissions/blob/main/SUBMISSION_FORMAT.md).
- [x] All required fields are filled in (`schema_version`, name, applied
  definition, submitter organization(s), contact email, references,
  implementation resources).
- [x] The submission contains **no proprietary or confidential information** ---
  I understand everything posted here is public and non-confidential.
- [x] I will follow this pull request for review comments (GitHub email
  notifications enabled on my account).
- [x] I have self-checked my submission against
  [CONTENT_STANDARDS.md](https://github.com/usnistgov/ai-metrology-submissions/blob/main/CONTENT_STANDARDS.md)
  --- the substantive criteria reviewers apply.

## Additional context

- **Maturity:**
  - This is a newly proposed method, not adopted elsewhere, and not independently validated.
  - The reference implementation is a single-author proof of concept used in one dedicated environment, pinned at release tag `TAG_TBD`.
  - It uses only the Python standard library, and its worked example reproduces the YAML's numbers exactly under test.
- **Primary specification:** the YAML's `applied_definition`.
- **Peer-reviewed support:** for the underlying measurement only.
  - Balliu et al. (IEEE S&P 2023) and Yu et al. (DSN 2024) measure SBOM precision and recall against ground truth.
  - This method moves that measurement from SBOM tool output to an organisation's own AI inventory. It adds content hashes for unversioned AI artifacts and reports the outcome classes separately.
- **Relation to the catalogue and open submissions:**
  - I found no AI Metrology Center entry on inventory or bill-of-materials accuracy.
  - The nearest open submission is adverse-action traceability (#14), a qualitative, single-domain reconciliation of outputs to their declared sources.
- **Context:** in security operations the system of record is not trusted on its own; practitioners establish what is deployed by continuous reconciliation against several independent sources (cf. CIS Controls v8, Controls 1-2). Governance guidance asks for an AI inventory (AI RMF GOVERN 1.6), but not how to check it. This applies that practice to AI-specific components: verification, in the TEVV sense, that the deployed configuration is the one registered.

