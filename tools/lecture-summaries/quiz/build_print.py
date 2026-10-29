"""نسخة PDF للطباعة: الأسئلة ثم مفتاح الإجابات بالأدلة. python3 build_print.py out.html"""
import sys, html
import build_quiz as bq
L = ["أ", "ب", "ج", "د"]
e = html.escape
d = bq.build()
css = open(bq.os.path.join(bq.HERE, "print.css"), encoding="utf-8").read()
css = css.replace("__FONT_AR__", bq.font("cairo-arabic.woff2")).replace("__FONT_LA__", bq.font("cairo-latin.woff2"))
out = [f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>اختبار تراث ابن تيمية</title><style>{css}</style></head><body>',
       '<h1>اختبار الكتب الخمسة الأولى من «جمع الكتب المشروحة من تراث ابن تيمية»</h1>',
       '<p class="sub">شرح الشيخ حسين عبد الرازق · الفيديوهات 9 إلى 27 · 60 سؤالًا · النجاح من 70٪ · مفتاح الإجابات والأدلة في آخر الملف</p>']
for bi, b in enumerate(d["books"]):
    out.append(f'<h2>{bi+1}. {e(b["name"])}</h2>')
    for q in [q for q in d["qs"] if q["b"] == bi]:
        kind = "صح أو خطأ" if q["type"] == "tf" else "اختيار من متعدد"
        opts = "".join(f'<li><b>{L[i]}</b> {e(o)}</li>' for i, o in enumerate(q["opts"]))
        out.append(f'<div class="q"><div class="h">سؤال {q["id"]} · الدرس {q["lesson"]} · {e(q["level"])} · {kind}</div>'
                   f'<p class="t">{e(q["q"])}</p><ol class="o">{opts}</ol></div>')
out.append('<h2 class="key">مفتاح الإجابات والأدلة</h2>')
for q in d["qs"]:
    b = d["books"][q["b"]]["name"]
    out.append(f'<div class="a"><p><b>سؤال {q["id"]}: ({L[q["a"]]}) {e(q["opts"][q["a"]])}</b></p><p>{e(q["why"])}</p>'
               f'<blockquote>«{e(q["quote"])}»</blockquote><p class="r">{e(b)} — الدرس {q["lesson"]} (الفيديو {q["video"]}) · '
               f'<a href="{q["url"]}">{q["url"]}</a> ({q["time"]})</p></div>')
out.append('</body></html>')
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out))
