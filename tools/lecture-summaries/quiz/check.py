import sys, importlib.util
from txsrc import lines
for lec in sys.argv[1:]:
    sp = importlib.util.spec_from_file_location(lec, f"qs/{lec}.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    L = lines(lec)
    for k, q in enumerate(m.Q):
        rs = q["s"] if isinstance(q["s"], list) else [q["s"]]
        txt = " … ".join(" ".join(s for _, s in L[i:i+n]) for i, n in rs)
        print(f"{k+1}. {q['q']}\n   ✔ {q['o'][0] if 'o' in q else q['tf']}\n   « " + txt + " »")
    print(lec, len(m.Q))
