On the request for independent support: here is one reproducible data point, on an evaluator from a codebase unrelated to the submitter's. It is a field instance of the "missing baselines, unreadable sources" class named in the YAML's `usage_details`.

**The evaluator.** `check_ssot` is a CI gate in a public repository I maintain, a Lean proof project. It passes when every new declaration is listed in a registry file, `ssot.json`. From when this code entered the tracked tree (2026-08-15) until the fix (2026-09-06), it returned a pass when that file was absent ([code at the defect](https://github.com/timbrigham/ZeroParadox/blob/09129065f280a0a8765d5cfb1a28663feb911fe2/tools/verify/batch.py#L1015-L1020)):

```python
if not os.path.exists(p):
    return True, "no ssot.json in tree"
```

The fixed version returns `False` on that branch ([fixed lines](https://github.com/timbrigham/ZeroParadox/blob/28f78173bfe68419d3265753b4b323c35c0b2ca9/tools/verify/batch.py#L1122-L1134)).

**The pair, run on both revisions.** I built it by hand from the YAML's `applied_definition`, without the submitter's conformance suite. I used one declaration and matched configuration. Besides the YAML's control/degenerate pair, I added a third input showing that the gate does fail when coverage is genuinely missing.

| input | before fix (`0912906`) | after fix (`28f7817`) |
|---|---|---|
| control: registry lists the declaration | `True` | `True` |
| extra: registry omits it | `False` | `False` |
| degenerate: no registry file | **`True`** | `False` |

Before the fix, the case fails under the submitted procedure, because the degenerate variant inherits the control's pass. After the fix the gate no longer passes the degenerate input, but its output is still binary: it returns the same `False` as the genuine-miss row, and only the message says the registry could not be read. Read literally, that is a measured negative, not the "required non-measurement status", so the case still fails. It would pass only if the message were mapped to a non-measurement status, which is the adaptation step in known failure mode 2. The pair catches the vacuous pass. It does not certify the fix.

**Scope.** I found and fixed this defect before this submission existed. I built the pair afterwards, knowing the answer. So this shows that the procedure correctly classifies a real defect that occurred in practice. It is not evidence that the procedure finds defects prospectively. It is one case of one degenerate class, on a CI gate rather than an AI model evaluator, though `usage_details` includes "gates". It is not peer review, I have no connection to the submitter, and I'm offering it as one external known-answer instance that the submitter may reference or ignore.

<details><summary>Reproduction (stdlib Python, under a minute)</summary>

From a clone of `timbrigham/ZeroParadox` (`git clone --filter=blob:none` keeps it light), export the gate at each commit with `mkdir <dir> && git archive <sha> tools/verify | tar -x -C <dir>`, then run `python -I pair.py <dir>/tools/verify <fixtures>`:

```python
import sys, importlib
src, fixtures = sys.argv[1], sys.argv[2]   # tools/verify dir, fixtures dir
sys.path.insert(0, src)
b = importlib.import_module("batch")
decls = ["ZeroParadox/T.lean::t_alpha"]
for side in ("control", "uncovered", "degenerate"):
    b.REPO = f"{fixtures}/{side}"
    ok, msg = b.check_ssot(decls)
    print(f"{side:10s} -> {ok!s:5s} | {msg[:70]}")
```

Fixtures: `control/ssot.json` is `{"rows":[{"qualified":"ZP.t_alpha","short":"t_alpha"}]}`. `uncovered/ssot.json` is the same with `t_beta`. `degenerate/` need not exist; the point is only that it has no `ssot.json` under it.
</details>
