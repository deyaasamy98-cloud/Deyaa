import sys, json, re
cl = lambda s: re.sub(r"\*\*", "", s)
for lec in sys.argv[1:]:
    d = json.load(open(f"../specs/{lec}.json"))
    print("=====", lec, d["book"], "|", d["lesson_label"], "|", cl(d["title"]))
    for q in d["questions"]: print("Q:", cl(q["q"]), "=>", cl(q["a"]))
    print("NOTES:", " / ".join(cl(n) for n in d["notes"]))
