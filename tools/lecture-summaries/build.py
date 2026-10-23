# Build a lecture summary: PDF + mind map PNG + tree map PNG from a JSON spec.
# Usage: python3 build.py spec.json OUT_DIR
import json, sys, os, re, html, asyncio
from playwright.async_api import async_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PALETTE = ["#1F5C45", "#9A6B1F", "#21606F", "#7A2E3A", "#3E4F86", "#5D6B21", "#6A3D7A", "#8A4B22", "#2F6E62", "#4B5563"]

def esc(s): return html.escape(str(s), quote=False)

def md(s):
    """Inline markup: **bold**, ==highlight==, ﴿ayah﴾ and «quote» styling."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"==(.+?)==", r"<mark>\1</mark>", s)
    s = re.sub(r"﴿(.+?)﴾", r'<span class="ayah">﴿\1﴾</span>', s)
    s = s.replace("\n", "<br>")
    return s

CSS = r"""
:root{--ink:#24201b;--muted:#6b6257;--paper:#FBF7EE;--card:#FFFDF8;--green:#1F5C45;--green2:#2E7A5C;
--gold:#B8893B;--gold2:#E9D6A8;--wine:#7A2E3A;--line:#E4D9C3}
@page{size:A4;margin:0}
@page land{size:A4 landscape;margin:0}
@page port{size:A4;margin:0}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;background:var(--paper);padding:15mm 15mm 17mm;-webkit-box-decoration-break:clone;box-decoration-break:clone;color:var(--ink);font-family:"Noto Naskh Arabic","Amiri",serif;
font-size:15.5pt;line-height:1.95;direction:rtl;text-align:justify}
b{color:var(--green);font-weight:700}
mark{background:linear-gradient(transparent 55%,#F1DFA9 55%);color:inherit;padding:0 2px}
.ayah{font-family:"Amiri Quran","Amiri",serif;color:#14523b;font-size:1.04em}
h1,h2,h3,h4{font-family:"Noto Kufi Arabic","Cairo",sans-serif;line-height:1.5;text-align:right;margin:0}
.cover{page-break-after:always;height:263mm;display:flex;flex-direction:column;justify-content:space-between;
border:2.5px solid var(--gold);outline:7px solid var(--green);outline-offset:-14px;padding:16mm 14mm;gap:5mm;overflow:hidden;background:
radial-gradient(circle at 50% 0%,#FFF9EA 0,#FBF7EE 60%)}
.cover .series{font-family:"Noto Kufi Arabic";color:var(--gold);font-size:17pt;text-align:center;letter-spacing:.5px}
.cover .book{font-family:"Aref Ruqaa","Amiri";color:var(--green);font-size:36pt;text-align:center;line-height:1.5;margin:8mm 0 2mm}
.cover .lesson{display:block;margin:0 auto;width:max-content;background:var(--green);color:#fff;font-family:"Noto Kufi Arabic";
font-size:19pt;padding:2mm 10mm;border-radius:40px}
.cover .title{font-family:"Noto Kufi Arabic";font-weight:600;font-size:18pt;color:var(--wine);text-align:center;margin-top:6mm;line-height:1.7}
.cover .orn{text-align:center;color:var(--gold);font-size:22pt;letter-spacing:8px;margin:4mm 0}
.cover .overview{font-size:13.5pt;text-align:center;color:#3b342c;line-height:1.9}
.chips{display:flex;flex-wrap:wrap;gap:2.5mm;justify-content:center;margin-top:4mm}
.chip{border:1.5px solid var(--gold);color:var(--green);border-radius:30px;padding:0 4mm;font-family:"Noto Kufi Arabic";font-size:11pt;background:#fff;line-height:1.9}
.meta{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.meta div{background:#fff;border:1px solid var(--line);border-right:5px solid var(--gold);border-radius:6px;padding:2mm 4mm;font-size:12.5pt;line-height:1.7}
.meta small{display:block;color:var(--muted);font-family:"Noto Kufi Arabic";font-size:10.5pt}
.toc{page-break-after:always}
.toc h2,.sec>h2{font-size:22pt;color:var(--green);border-bottom:3px solid var(--gold);padding-bottom:1.5mm;margin:0 0 5mm;
display:flex;align-items:center;gap:3mm}
.num{display:inline-flex;align-items:center;justify-content:center;min-width:11mm;height:11mm;border-radius:50%;
background:var(--green);color:#fff;font-size:15pt;font-family:"Noto Kufi Arabic"}
.toc ol{list-style:none;padding:0;margin:0;columns:1}
.toc li{display:flex;gap:3mm;align-items:center;border-bottom:1px dashed var(--line);padding:1.3mm 0;font-family:"Noto Kufi Arabic";font-size:14.5pt}
.toc li span.n{color:var(--gold);min-width:9mm;font-weight:700}
.sec{margin-bottom:8mm}
.sec h3{font-size:17pt;color:var(--wine);margin:5mm 0 2mm}
.sec p{margin:0 0 3mm}
.quote{background:#fff;border:1px solid var(--line);border-right:6px solid var(--green);border-radius:8px;padding:3mm 5mm;margin:3mm 0 4mm;
font-family:"Amiri";font-size:17pt;line-height:2;color:#1d3d30;page-break-inside:avoid}
.quote .src{display:block;font-family:"Noto Kufi Arabic";font-size:11pt;color:var(--muted);margin-top:1mm}
.matn{border-right-color:var(--gold);background:#FFFBF0}
.box{border-radius:10px;padding:3mm 5mm;margin:3mm 0 4mm;page-break-inside:avoid;border:1.5px solid}
.box h4{font-size:14.5pt;margin-bottom:1mm}
.box.fawaid{background:#EEF6F0;border-color:#9CC7AE}.box.fawaid h4{color:var(--green)}
.box.tanbih{background:#FBEEEE;border-color:#DDAAAA}.box.tanbih h4{color:var(--wine)}
.box.def{background:#FFF7E3;border-color:#E3C87F}.box.def h4{color:#8A6418}
.box.key{background:var(--green);border-color:var(--green);color:#fff}.box.key h4{color:var(--gold2)}.box.key b{color:#FFE7A8}
ul.l,ol.l{margin:1mm 0 3mm;padding-right:7mm}
ul.l li,ol.l li{margin-bottom:1mm}
ul.l li::marker{color:var(--gold)}
ol.l li::marker{color:var(--green);font-family:"Noto Kufi Arabic";font-weight:700}
table{width:100%;border-collapse:collapse;margin:3mm 0 5mm;font-size:13.5pt;line-height:1.7;page-break-inside:avoid;background:#fff}
th{background:var(--green);color:#fff;font-family:"Noto Kufi Arabic";font-weight:500;padding:2mm 3mm}
td{border:1px solid var(--line);padding:2mm 3mm;vertical-align:top}
tr:nth-child(even) td{background:#FBF6EA}
.mappage{page-break-before:always;page-break-after:always;display:flex;flex-direction:column;background:var(--paper)}
.mappage.land{page:land;height:178mm}.mappage.port{page:port;height:262mm}
.mappage h2{font-size:18pt;color:var(--green);text-align:center;margin-bottom:2mm}
.mapimg{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.mapimg img{width:100%;height:100%;object-fit:contain}
.notes li{margin-bottom:2mm}
.notes{list-style:none;padding:0}
.notes li{display:flex;gap:3mm;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:8px;padding:2mm 4mm;page-break-inside:avoid}
.notes li:before{content:"✓";color:#fff;background:var(--green);border-radius:4px;min-width:6.5mm;height:6.5mm;line-height:6.5mm;text-align:center;font-size:11pt;margin-top:2.5mm}
.q{background:#fff;border:1px solid var(--line);border-radius:10px;padding:3mm 5mm;margin-bottom:4mm;page-break-inside:avoid}
.q .qh{display:flex;gap:3mm;align-items:flex-start;font-weight:700}
.q .qn{background:var(--wine);color:#fff;border-radius:6px;min-width:9mm;text-align:center;font-family:"Noto Kufi Arabic";font-size:13pt;line-height:9mm;height:9mm;margin-top:1mm}
.q .qt{font-size:10.5pt;font-family:"Noto Kufi Arabic";color:var(--gold);border:1px solid var(--gold);border-radius:20px;padding:0 3mm;white-space:nowrap;margin-top:2mm;font-weight:400}
.q .opts{margin:1mm 12mm 0 0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:0 6mm;font-size:14pt}
.q .ans{margin-top:2mm;border-top:1.5px dashed var(--gold2);padding-top:2mm;color:#21402f}
.q .ans:before{content:"الإجابة النموذجية: ";font-family:"Noto Kufi Arabic";color:var(--green);font-weight:700}
.qgroup{font-size:16pt;color:var(--wine);margin:6mm 0 3mm;font-family:"Noto Kufi Arabic"}
.exp{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.exp div{background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:8px;padding:2mm 4mm;page-break-inside:avoid;font-size:13.5pt;line-height:1.8}
.exp b{display:block;font-family:"Noto Kufi Arabic";font-size:14pt}
.foot{margin-top:8mm;text-align:center;color:var(--muted);font-size:11pt}
"""

MAP_CSS = r"""
*{box-sizing:border-box}body{margin:0;background:#FBF7EE;font-family:"Noto Naskh Arabic";direction:ltr;width:max-content}
#wrap{position:relative;display:inline-block;padding:50px 60px 40px;direction:rtl}
svg.links{position:absolute;inset:0;overflow:visible;pointer-events:none}
.hdr{text-align:center;font-family:"Noto Kufi Arabic";color:#1F5C45;font-size:44px;margin-bottom:8px}
.sub{text-align:center;font-family:"Noto Kufi Arabic";color:#B8893B;font-size:26px;margin-bottom:36px}
.mm{display:grid;grid-template-columns:auto auto auto;align-items:center;column-gap:120px}
.col{display:flex;flex-direction:column;gap:34px}
.center{width:380px;min-height:380px;border-radius:50%;background:radial-gradient(circle at 50% 35%,#2E7A5C,#163F30);
border:10px solid #B8893B;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
font-family:"Noto Kufi Arabic";font-size:40px;line-height:1.45;padding:40px;box-shadow:0 0 0 6px #FBF7EE,0 0 0 9px #1F5C45}
.center small{font-size:24px;color:#F3E2B3;margin-top:8px}
.br{width:640px;background:#FFFDF8;border:3px solid var(--c);border-radius:22px;overflow:hidden}
.br h3{margin:0;background:var(--c);color:#fff;font-family:"Noto Kufi Arabic";font-weight:600;font-size:31px;padding:10px 22px;line-height:1.45}
.br ul{margin:0;padding:12px 22px 14px 18px;list-style:none}
.br li{font-size:25px;line-height:1.6;padding:5px 0;border-bottom:1px dashed #E4D9C3;display:flex;gap:10px}
.br li:last-child{border:0}
.br li:before{content:"◆";color:var(--c);font-size:16px;margin-top:9px}
.tree{display:flex;align-items:center}
.node{display:flex;align-items:center;flex-direction:row}
.kids{display:flex;flex-direction:column;gap:14px;margin-right:110px}
.box{font-family:"Noto Kufi Arabic";border-radius:16px;padding:10px 22px;line-height:1.45;max-width:560px}
.l0{background:#163F30;color:#fff;font-size:40px;border:6px solid #B8893B;padding:24px 34px;text-align:center;max-width:420px}
.l1{background:var(--c);color:#fff;font-size:30px;font-weight:600;min-width:300px}
.l2{background:#FFFDF8;border:3px solid var(--c);color:#24201b;font-size:25px;font-weight:500}
.l3{background:transparent;border-right:5px solid var(--c);border-radius:4px;color:#3b342c;font-size:22.5px;font-family:"Noto Naskh Arabic";padding:4px 14px;max-width:720px}
.kids.k1{gap:30px}.kids.k2{gap:12px}.kids.k3{gap:6px;margin-right:80px}
.foot{text-align:center;color:#6b6257;font-size:20px;margin-top:30px;font-family:"Noto Kufi Arabic"}
"""

LINK_JS = r"""
() => {
  const wrap = document.getElementById('wrap'); const W = wrap.getBoundingClientRect();
  const svg = document.querySelector('svg.links'); svg.setAttribute('width', W.width); svg.setAttribute('height', W.height);
  let out = '';
  document.querySelectorAll('[data-from]').forEach(el => {
    const a = document.getElementById(el.dataset.from).getBoundingClientRect(), b = el.getBoundingClientRect();
    const c = el.dataset.c || '#1F5C45', w = el.dataset.w || 4;
    let x1, x2; const y1 = a.top + a.height/2 - W.top, y2 = b.top + b.height/2 - W.top;
    if (b.left > a.right) { x1 = a.right - W.left; x2 = b.left - W.left; } else { x1 = a.left - W.left; x2 = b.right - W.left; }
    const mx = (x1 + x2) / 2;
    out += `<path d="M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}" stroke="${c}" stroke-width="${w}" fill="none" stroke-linecap="round"/>`;
    out += `<circle cx="${x2}" cy="${y2}" r="${w*1.6}" fill="${c}"/>`;
  });
  svg.innerHTML = out;
}
"""

def mind_html(spec):
    m = spec["mind"]; brs = m["branches"]
    half = (len(brs) + 1) // 2
    right, left = brs[:half], brs[half:]
    def br(b, i):
        c = PALETTE[i % len(PALETTE)]
        items = "".join(f"<li><span>{md(x)}</span></li>" for x in b["items"])
        return f'<div class="br" id="b{i}" style="--c:{c}" data-from="ctr" data-c="{c}" data-w="7"><h3>{esc(b["title"])}</h3><ul>{items}</ul></div>'
    rc = "".join(br(b, i) for i, b in enumerate(right))
    lc = "".join(br(b, i + half) for i, b in enumerate(left))
    center = f'<div class="center" id="ctr">{esc(m["center"])}<small>{esc(m.get("sub",""))}</small></div>'
    return f"""<div id="wrap"><svg class="links"></svg><div class="hdr">الخريطة الذهنية — {esc(spec['short'])}</div>
<div class="sub">{esc(spec['book'])} · {esc(spec['lesson_label'])}</div>
<div class="mm"><div class="col">{rc}</div>{center}<div class="col">{lc}</div></div>
<div class="foot">{esc(spec['speaker'])} · {esc(spec['series'])}</div></div>"""

def tree_html(spec):
    t = spec["tree"]; cnt = [0]
    def node(n, lvl, parent, color):
        cnt[0] += 1; nid = f"n{cnt[0]}"
        attrs = f'data-from="{parent}" data-c="{color}" data-w="{[0,6,4,3][min(lvl,3)]}"' if parent else ""
        kids = n.get("children", [])
        label = md(n["title"]) if lvl >= 2 else esc(n["title"])
        box = f'<div class="box l{min(lvl,3)}" id="{nid}" style="--c:{color}" {attrs}>{label}</div>'
        if not kids: return f'<div class="node">{box}</div>'
        inner = "".join(node(k, lvl + 1, nid, PALETTE[i % len(PALETTE)] if lvl == 0 else color) for i, k in enumerate(kids))
        return f'<div class="node">{box}<div class="kids k{min(lvl+1,3)}">{inner}</div></div>'
    body = node({"title": t["root"], "children": t["children"]}, 0, None, "#1F5C45")
    return f"""<div id="wrap"><svg class="links"></svg><div class="hdr">الخريطة الشجرية — {esc(spec['short'])}</div>
<div class="sub">{esc(spec['book'])} · {esc(spec['lesson_label'])}</div><div class="tree">{body}</div>
<div class="foot">{esc(spec['speaker'])} · {esc(spec['series'])}</div></div>"""

def block(b):
    t = b["type"]
    if t == "p": return f"<p>{md(b['text'])}</p>"
    if t == "h": return f"<h3>{esc(b['text'])}</h3>"
    if t in ("quote", "matn"):
        src = f'<span class="src">— {esc(b["src"])}</span>' if b.get("src") else ""
        return f'<div class="quote {"matn" if t=="matn" else ""}">{md(b["text"])}{src}</div>'
    if t == "list":
        tag = "ol" if b.get("ordered") else "ul"
        return f'<{tag} class="l">' + "".join(f"<li>{md(x)}</li>" for x in b["items"]) + f"</{tag}>"
    if t == "box":
        body = md(b["text"]) if "text" in b else '<ul class="l">' + "".join(f"<li>{md(x)}</li>" for x in b["items"]) + "</ul>"
        return f'<div class="box {b.get("kind","fawaid")}"><h4>{esc(b["title"])}</h4>{body}</div>'
    if t == "table":
        th = "".join(f"<th>{esc(h)}</th>" for h in b["head"])
        rows = "".join("<tr>" + "".join(f"<td>{md(c)}</td>" for c in r) + "</tr>" for r in b["rows"])
        return f"<table><tr>{th}</tr>{rows}</table>"
    raise ValueError(t)

QTYPE = {"essay": "سؤال مقالي", "define": "عرّف", "compare": "قارن", "mcq": "اختيار من متعدد", "tf": "صح أم خطأ",
         "why": "علّل", "apply": "تطبيق", "list": "عدّد", "explain": "اشرح"}
GROUPS = [("define", "أولًا: المصطلحات والتعريفات"), ("list", "ثانيًا: التعداد والتقسيم"), ("why", "ثالثًا: التعليل"),
          ("compare", "رابعًا: المقارنة"), ("explain", "خامسًا: الشرح والاستدلال"), ("essay", "سادسًا: أسئلة مقالية"),
          ("apply", "سابعًا: التطبيق والتنزيل"), ("mcq", "ثامنًا: اختيار من متعدد"), ("tf", "تاسعًا: صح أم خطأ مع التصحيح")]

def pdf_html(spec, mind_png, tree_png):
    secs = spec["sections"]
    toc_items = [s["title"] for s in secs] + ["الخريطة الذهنية", "الخريطة الشجرية", "ملاحظات المذاكرة — لا تنسَ",
                                               "أسئلة المراجعة وإجاباتها", "عناوين للتوسع والبحث"]
    toc = "".join(f'<li><span class="n">{i+1:02d}</span>{esc(t)}</li>' for i, t in enumerate(toc_items))
    chips = "".join(f'<span class="chip">{esc(k)}</span>' for k in spec.get("keywords", []))
    body = ""
    for i, s in enumerate(secs):
        body += f'<div class="sec"><h2><span class="num">{i+1}</span>{esc(s["title"])}</h2>' + "".join(block(b) for b in s["blocks"]) + "</div>"
    n = len(secs)
    from PIL import Image
    def mp(k, t, f):
        w, h = Image.open(f).size
        return f'<div class="mappage {"land" if w > h else "port"}"><h2>{k} · {t}</h2><div class="mapimg"><img src="file://{f}"></div></div>'
    maps = mp(n + 1, "الخريطة الذهنية", mind_png) + mp(n + 2, "الخريطة الشجرية", tree_png)
    notes = "".join(f"<li><span>{md(x)}</span></li>" for x in spec["notes"])
    qs = ""; k = 0
    for g, gt in GROUPS:
        items = [q for q in spec["questions"] if q["type"] == g]
        if not items: continue
        qs += f'<div class="qgroup">{gt}</div>'
        for q in items:
            k += 1
            opts = ""
            if q.get("options"):
                opts = '<ul class="opts">' + "".join(f"<li>({'أبجد'[j] if j<4 else j+1}) {md(o)}</li>" for j, o in enumerate(q["options"])) + "</ul>"
            qs += (f'<div class="q"><div class="qh"><span class="qn">{k}</span><span style="flex:1">{md(q["q"])}</span>'
                   f'<span class="qt">{QTYPE[g]}</span></div>{opts}<div class="ans">{md(q["a"])}</div></div>')
    exp = "".join(f"<div><b>{esc(e['title'])}</b>{md(e['desc'])}</div>" for e in spec["expand"])
    return f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="cover"><div><div class="series">{esc(spec['series'])}</div><div class="orn">۞ ❁ ۞</div>
<div class="book">{esc(spec['book'])}</div><span class="lesson">{esc(spec['lesson_label'])}</span>
<div class="title">{esc(spec['title'])}</div></div>
<div><div class="overview">{md(spec['overview'])}</div><div class="chips">{chips}</div></div>
<div class="meta"><div><small>الشارح</small>{esc(spec['speaker'])}</div><div><small>المدة</small>{esc(spec['duration'])}</div>
<div><small>المتن</small>{esc(spec['matn_author'])}</div><div><small>رابط الدرس</small>{esc(spec['url'])}</div></div></div>
<div class="toc"><h2><span class="num">≡</span>فهرس المحتويات</h2><ol>{toc}</ol></div>
{body}{maps}
<div class="sec" style="page-break-before:always"><h2><span class="num">{n+3}</span>ملاحظات المذاكرة — لا تنسَ</h2><ul class="notes">{notes}</ul></div>
<div class="sec" style="page-break-before:always"><h2><span class="num">{n+4}</span>أسئلة المراجعة وإجاباتها</h2>
<p>أجب عن كل سؤال بنفسك أولًا، ثم قارن إجابتك بالإجابة النموذجية تحته.</p>{qs}</div>
<div class="sec" style="page-break-before:always"><h2><span class="num">{n+5}</span>عناوين للتوسع والبحث</h2><div class="exp">{exp}</div>
<div class="foot">ملخص تعليمي مُعد من تفريغ صوت الدرس، والمرجع الأصلي هو الدرس نفسه والكتاب المشروح.</div></div>
</body></html>"""

async def render_map(page, inner, out_png):
    await page.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{MAP_CSS}</style></head><body>{inner}</body></html>')
    await page.evaluate("document.fonts.ready")
    box = await page.evaluate("(() => {const r = document.getElementById('wrap').getBoundingClientRect(); return [Math.ceil(r.width), Math.ceil(r.height)]})()")
    await page.set_viewport_size({"width": box[0], "height": box[1]})
    await page.evaluate(LINK_JS)
    el = await page.query_selector("#wrap")
    await el.screenshot(path=out_png)

async def main(spec_path, out_dir):
    spec = json.load(open(spec_path, encoding="utf8"))
    os.makedirs(out_dir, exist_ok=True)
    base = spec["file_base"]
    mind_png = os.path.abspath(f"{out_dir}/{spec['map_base']} - الخريطة الذهنية.png")
    tree_png = os.path.abspath(f"{out_dir}/{spec['map_base']} - الخريطة الشجرية.png")
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME)
        pg = await b.new_page(viewport={"width": 1200, "height": 800}, device_scale_factor=2.5)
        await render_map(pg, mind_html(spec), mind_png)
        await render_map(pg, tree_html(spec), tree_png)
        pg2 = await b.new_page()
        tmp = os.path.abspath(f"{out_dir}/.tmp.html")
        open(tmp, "w", encoding="utf8").write(pdf_html(spec, mind_png, tree_png))
        await pg2.goto(f"file://{tmp}"); await pg2.evaluate("document.fonts.ready")
        await pg2.pdf(path=f"{out_dir}/{base}.pdf", print_background=True, prefer_css_page_size=True,
                      display_header_footer=True, header_template="<span></span>",
                      footer_template=f'<div style="width:100%;font-size:9pt;color:#8a7f70;text-align:center;font-family:Noto Kufi Arabic;direction:rtl">{esc(spec["short"])} · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
        os.remove(tmp)
        await b.close()
    print("built", base)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
