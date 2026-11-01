---
name: course-summary
description: Summarize a media buying / performance marketing / creative course (YouTube video, playlist, or uploaded transcript/files) into a study page that ADDS to the course — every idea marked still valid / changed / outdated, a "2026 updates" section from official sources, a campaign map, and ready-to-use checklists — in the Cairo font, exported to PDF and saved to ملخصات. Also feeds a separate living file that links creative-evaluation and data-analysis ideas to the user's Reel Analytics project. Use when the user sends a media buying / ads / creative course lesson to summarize.
---

# Course summary (media buying)

The user is a **creative strategist / content maker** for Egyptian e-commerce brands (Brand Gallery, SEZLUXE). They shoot Reels, analyse them monthly in their own Excel tool **Reel Analytics**, and report to a manager and a media buyer. Market: **Egypt, EGP, Meta (Facebook/Instagram) Reels**. Read `references/reel-analytics.md` before the first lesson of a session.

Talk to the user in Egyptian Arabic. Write the page in clear Modern Standard Arabic; keep English platform terms as they appear in Ads Manager (Campaign, Ad set, CTR, ROAS…), and quote the instructor's phrases inside «».

## Fixed preferences (do not ask)

Same as the video-summary skill: Cairo font, PDF always, everything in `ملخصات/` with `NN - العنوان` numbering, README row, commit + push, send the PDF in chat. Reuse its files:
- head (CSS): `.claude/skills/video-summary/assets/head.html`
- transcript: `.claude/skills/video-summary/scripts/get_subs.sh`, `vtt2txt.py`
- PDF: `.claude/skills/video-summary/scripts/to_pdf.js` with fonts `.claude/skills/video-summary/assets/fonts`
- README row: `.claude/skills/video-summary/scripts/add_row.py`

One page per lesson (or per short module if lessons are under ~10 min). Title format: `NN - العنوان - اسم الكورس س`.

## The page: five sections (template `assets/body-template.html`)

1. **الملخص** — 6–10 topics in the instructor's order, timestamp chip on each (if the source is a file without timestamps, cite the slide/page instead). Every topic gets a status pill:
   - `ok` 🟢 لسه شغال · `mix` 🟡 اتغيّر · `no` 🔴 قديم / مبقاش بيتعمل كده
2. **تحديثات 2026** — one card per 🟡/🔴 item and per important 🟢 item that has a new nuance: «الكورس قال» vs «الوضع دلوقتي», and the source. **Search the web every time** (WebSearch); prefer official sources (Meta Business Help Center, Meta for Business blog, Meta Blueprint, Google Ads Help, TikTok Business). Give the date of the change when known. Never write platform changes from memory; if you can't confirm, say «مش متأكد، اتأكد من …» or leave it out. Also flag wrong numbers and myths here (pill `no`).
3. **خريطة الحملة** — the tree, but shaped to the lesson: campaign structure (Campaign ← Ad set ← Ad), funnel (TOF/MOF/BOF), or a decision tree («لو الـ CPM عالي ← …»). One root, 4–7 branches.
4. **المطلوب: اعمل إيه** — tools, not advice:
   - a step order (4–6 steps),
   - checklists (pre-launch, testing, scaling) with `☐` items,
   - click-paths inside Ads Manager when the lesson is practical,
   - formulas with a worked example in EGP,
   - old→new belief table (with timestamps) only if the lesson has mindset content.
5. **زيادة على الكورس** (short, 3–6 cards) — what the course didn't say but adds real value: tools (Meta Ad Library, AI creative tools), test ideas, Egypt-specific notes (COD, confirmation/delivery rate, real profit after returns), better free resources (Blueprint, Skillshop…). Each must be concrete and sourced.

Nothing else (no quizzes, no Q&A) unless asked.

## The separate project file: «من الكورس إلى Reel Analytics»

A living file that grows with every lesson. **Not numbered**; fixed names:
- HTML: `ملخصات/html/ربط الكورس بـ Reel Analytics.html`
- PDF: `ملخصات/ربط الكورس بـ Reel Analytics.pdf`
- Template: `assets/project-log-template.html`. Keep one artifact URL and republish it each time.

After writing each lesson page, go through the lesson again and pull out **anything about creatives, how to evaluate them, metrics, testing, or data analysis**. For each idea add a card:
- **الفكرة** + source (summary NN + timestamp chip),
- **تتربط بإيه في الملف** — exact tab/column (e.g. `Ads › Diagnosis`, `Report › Lessons`, `What To Shoot › Priority`),
- **النوع**: عمود جديد · تعديل قاعدة · حد/عتبة · تجربة (test) · سطر في التقرير · سكريبت/تصوير,
- **إزاي تطبقها** — steps, and an Excel formula in the file's own style (`IF(OR(x="",x=0),"",…)`, COUNTIFS on `Group`) when it applies; test the formula logic against the September numbers in `references/reel-analytics.md`,
- **الأولوية**: عالية / متوسطة / بعدين, and **تحديث 2026** if relevant.

Then update the backlog table at the top of the file (one row per card: idea, tab, type, priority, status `جديد`). If an idea repeats an earlier card, add the new source to the old card instead of duplicating. If a lesson has nothing relevant, don't touch the file and say so in the reply.

Commit both files with the lesson. Send the project PDF in chat only when it changed.

## Steps

1. Get the source. YouTube → transcript as in the video-summary skill (step 1). Paid platform → ask the user for the transcript or files; PDFs/slides → read them fully.
2. Read the whole lesson before writing.
3. Research updates (WebSearch, several queries in one turn) for the lesson's claims.
4. Write the lesson page, assemble with head.html, export PDF, publish Artifact (icon `chart`), copy HTML, add README row (source label: course name + lesson number).
5. Update the project file (above), export its PDF, republish its artifact.
6. Commit, push, send PDFs.
7. Reply briefly in Egyptian Arabic: link(s), the 2–3 most important updates (what changed since the course), and what was added to the Reel Analytics file.
