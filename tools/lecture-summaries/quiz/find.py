import signal; signal.signal(signal.SIGPIPE, signal.SIG_DFL)
import sys, re
from txsrc import lines
lec, pat = sys.argv[1], sys.argv[2]
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 2
L = lines(lec); r = re.compile(pat); k = 0
for i, (t, s) in enumerate(L):
    if r.search(s):
        k += 1
        if k > 10: print("..."); break
        prev = L[i-1][1] if i else ""
        print(f"({prev}) >>#{i} [{t//60}:{t%60:02d}] " + " | ".join(x[1] for x in L[i:i+ctx+1]))
