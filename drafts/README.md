# drafts

Working folder for contributions to NIST's AI Metrology Center intake: https://github.com/usnistgov/ai-metrology-submissions. Everything here is a draft. Nothing is posted until Tim approves it, and Tim posts it himself.

This folder lives on the `drafts` branch of Tim's fork.
- It is pushed to Tim's own fork, which is public but is not a submission. Nobody at NIST is notified unless a PR is opened.
- **Never open a PR from this branch.** A submission PR must add exactly one YAML file under `submissions/`.
- To submit, cut a fresh branch from `main` (for example `git switch -c submit/<name> main`), copy the one YAML into `submissions/`, and push only that branch.

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
| `comments/pr19/` | #19 paired-control non-measurement | drafted, 2 review rounds, awaiting Tim's OK |
| (none) | #20 tool-descriptor mutation | decided not to comment: the gap is the submitter's own implementation |
| `submissions/evidence-currency/` | new: evidence currency (verdictLedger) | feasibility checked: public and MIT, overlap is ADJACENT; references verified; implementation pushed at mcp-mayhem 8207aa5 and verified; YAML next |
| (none) | new: NL-to-formal claim faithfulness | idea only |
