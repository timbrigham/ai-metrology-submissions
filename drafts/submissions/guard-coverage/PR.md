## Metric submission

Incident-Driven Guard Coverage measures how well regression-tested guards on an AI agent's tool use keep up with the risky actions agents are observed to attempt. It reports the share of observed patterns that have a guard and a test replaying the observed action, the time from first occurrence to that tested guard, the discovery trend, and an estimate of how likely the next session is to show a pattern not yet seen.

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
  - This is a newly proposed method, not independently validated.
  - The reference implementation is a single-author proof of concept used in one dedicated environment, pinned at release tag `nist2026` (commit `75b8862d4b1c340dcba55aca50e3edd4524da520`). It uses only the Python standard library.
  - The worked example runs on a public, redacted extract of that environment's real logs and incident register, with checksums, and reproduces the report exactly under test.
  - The real data is thin: three observed patterns, two of whose tested guards were added on the day measured, and one agent session with version data so far. No occurrence time is known, so time to guard is only a lower bound.
  - Time to guard and the unseen-pattern estimate are therefore also shown on a seeded synthetic replay, which the example labels as synthetic. The replay uses one setting under the estimator's own assumptions, so it checks the implementation, not the method.
- **Primary specification:** the YAML's `applied_definition`, with the worked example's README as the reference implementation.
- **Peer-reviewed support:** for the unseen-pattern estimate only. Items 1-3 are plain counts and durations.
  - Böhme (TOSEM 2018) treats software testing as species discovery and uses the Good-Turing discovery probability as a residual-risk measure.
  - Böhme, Liyanage and Wüstholz (ESEC/FSE 2021, Eq. 22) give the estimator on incidence data, together with its reset variants.
- **Relation to the catalogue and open submissions:**
  - The AI Metrology Center's "Agent / Tool Abuse Testing" generates attempts, and "Post-deployment Feedback" collects incidents. Neither measures how fast observed patterns are absorbed into tested guards.
  - Detector Gap (#6) measures whether a detector still catches obfuscated variants of a known hazard. It could test a guard's robustness within one pattern; this metric counts patterns and the time to guard them.
- **Context:** this applies the security operations loop (log, detect, respond, add a regression test) to AI agents' tool use, against a misbehaving but not adversarial agent. It reports how complete and how fast that loop is, and makes no claim that unobserved actions are covered.
