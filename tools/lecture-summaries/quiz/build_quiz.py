"""يبني صفحة الاختبار من quiz60.py وتفريغات الدروس.
python3 build_quiz.py <مسار الصفحة المستقلة> [<مسار نسخة Artifact>]"""
import base64, json, random, sys, os
from txsrc import lines
import quiz60

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = {9: "vDQ-O6iCgbM", 10: "_TfI3Ef92BI", 11: "xC4pYNfSN8Y", 12: "hf8DBrlYGnI", 13: "RG9o6H6CAXo",
         14: "EGwWyTSCFKA", 15: "VxrJMuSQ__Y", 16: "av6eM5XamWs", 17: "nSV0DtppiC4", 18: "UPfMbvbWdJU",
         19: "GlRhWa5vSOE", 20: "l-3-TBaJYHk", 21: "zHPqX0xzSSQ", 22: "eGhRPiqFWvw", 23: "C7n0-iqnLNE",
         24: "cOhhkoYRyZQ", 25: "a0M8tIvyuFM", 26: "5BUYW50Ea1Y", 27: "DL3-8ZIcrrA"}
FONTS = os.path.join(HERE, "fonts")

def hms(t):
    h, m, s = t // 3600, t % 3600 // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def build():
    rnd = random.Random(1446)
    mcq = [q for q in quiz60.Q if "o" in q]
    slots = [i % 4 for i in range(len(mcq))]; rnd.shuffle(slots)
    books, where = [], {}
    for bi, (name, lecs) in enumerate(quiz60.BOOKS):
        vids = [int(l[1:]) for l in lecs]
        books.append({"name": name, "lessons": len(lecs), "videos": f"{min(vids)}–{max(vids)}"})
        for li, l in enumerate(lecs): where[l] = (bi, li + 1)
    cache, out, k = {}, [], 0
    for n, q in enumerate(quiz60.Q, 1):
        L = cache.setdefault(q["l"], lines(q["l"]))
        rs = q["s"] if isinstance(q["s"], list) else [q["s"]]
        quote = " … ".join(" ".join(s for _, s in L[i:i + c]) for i, c in rs)
        for a, b in q.get("fix", {}).items():
            assert a in quote, (n, a); quote = quote.replace(a, b)
        t = L[rs[0][0]][0]; v = int(q["l"][1:]); bi, lesson = where[q["l"]]
        if "o" in q:
            right, wrong = q["o"][0], q["o"][1:]; rnd.shuffle(wrong)
            pos = slots[k]; k += 1
            opts = wrong[:pos] + [right] + wrong[pos:]; typ, ans = "mcq", pos
        else:
            opts, typ, ans = ["صح", "خطأ"], "tf", 0 if q["tf"] else 1
        out.append({"id": n, "b": bi, "lesson": f"{lesson:02d}", "video": v, "type": typ, "level": q["lv"],
                    "q": q["q"], "opts": opts, "a": ans, "why": q["why"], "quote": quote,
                    "time": hms(t), "url": f"https://youtu.be/{VIDEO[v]}?t={t}"})
    return {"books": books, "qs": out}

def font(name):
    return base64.b64encode(open(os.path.join(FONTS, name), "rb").read()).decode()

if __name__ == "__main__":
    data = build()
    body = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    body = (body.replace("__FONT_AR__", font("cairo-arabic.woff2"))
                .replace("__FONT_LA__", font("cairo-latin.woff2"))
                .replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    full = ('<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + body.replace("<style>", "<style>\n:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}", 1)
                  .replace("\n<header", "\n</head>\n<body>\n<header", 1)
            + "\n</body>\n</html>\n")
    open(sys.argv[1], "w", encoding="utf-8").write(full)
    if len(sys.argv) > 2: open(sys.argv[2], "w", encoding="utf-8").write(body)
    from collections import Counter
    print(len(data["qs"]), Counter(q["a"] for q in data["qs"] if q["type"] == "mcq"),
          Counter(q["a"] for q in data["qs"] if q["type"] == "tf"), Counter(q["b"] for q in data["qs"]),
          Counter(q["level"] for q in data["qs"]))
