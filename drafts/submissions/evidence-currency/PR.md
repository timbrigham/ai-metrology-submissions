## Metric submission

Evidence Currency measures, at a release or deployment decision, how much of the recorded evaluation evidence behind that decision was produced against the exact files being released. It reports current, stale and never-examined evidence separately, so a release claim such as "safety-evaluated" can be checked against the bytes actually shipped.

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
  - This is a newly proposed method, primarily submitter-grounded, and not independently validated.
  - The reference implementation is a single-author proof of concept used in one dedicated environment, pinned at release tag `TAG_TBD`.
  - Its worked example runs the YAML's scenario exactly and is pinned by tests.
- **Primary specification:** the YAML's `applied_definition`, with the worked example's README as the reference implementation.
- **Peer-reviewed support:** for the underlying principle only, not the metric itself.
  - Ekstazi (ISSTA 2015): a recorded result is valid only while its inputs' hashes are unchanged.
  - in-toto (USENIX Security 2019): decision-time checking of recorded evidence against artifact hashes.
- **Relation to the catalogue and open submissions:**
  - I found no AI Metrology Center entry on evidence staleness or provenance.
  - Audit-trail tamper detection (#16) measures malicious edits to a log.
  - Tool-descriptor mutation detection (#20) measures how much of a definition a pin covers.
  - Cross-carrier non-measurement fidelity (#23) shares the rule that "not examined is not a pass", but does not bind evidence to content.
- **Context:** this comes from applying security audit practice to AI agents, i.e. checking whether audit evidence is still valid for the system being shipped.
