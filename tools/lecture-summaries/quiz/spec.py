import sys, json, re
d = json.load(open(f"../specs/{sys.argv[1]}.json"))
cl = lambda s: re.sub(r"\*\*", "", s)
print(d["book"], "|", d["lesson_label"], "|", d["url"]); print(cl(d["title"]))
for s in d["sections"]:
    print("##", s["title"])
    for b in s["blocks"]:
        if b["type"] == "table": print("  T:", " / ".join(cl(" — ".join(r)) for r in b["rows"]))
        else: print("  " + b.get("kind", b["type"]) + ":", cl(b.get("title", "")), "::", cl(b.get("text") or " • ".join(b.get("items", []))))
for q in d["questions"]: print("Q:", cl(q["q"]), "=>", cl(q["a"]))
