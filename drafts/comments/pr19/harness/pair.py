import sys, importlib
src, fixtures = sys.argv[1], sys.argv[2]
sys.path.insert(0, src)
b = importlib.import_module("batch")
decls = ["ZeroParadox/T.lean::t_alpha"]
for side in ("control", "uncovered", "degenerate"):
    b.REPO = f"{fixtures}/{side}"
    ok, msg = b.check_ssot(decls)
    print(f"{side:10s} -> {ok!s:5s} | {msg[:70]}")
