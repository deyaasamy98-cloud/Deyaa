import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
TX = os.path.join(HERE, "..", "transcripts")
# video 11 and 12 were transcribed as one 138-minute file (L011.txt); split at 68:13
SPLIT = 68*60+13
def lines(lec):
    n = int(lec[1:])
    path = os.path.join(TX, "L011.txt" if n in (11, 12) else f"L{n:03d}.txt")
    out = []
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"\[(\d+):(\d+)\]\s*(.*)", ln.strip())
        if not m: continue
        t = int(m.group(1))*60 + int(m.group(2))
        if n == 11 and t >= SPLIT: continue
        if n == 12:
            if t < SPLIT: continue
            t -= SPLIT
        out.append((t, m.group(3)))
    return out
