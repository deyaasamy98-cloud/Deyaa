---
name: video-summary
description: Summarize a YouTube video or playlist (Arabic lectures, podcasts, psychology/recovery content) into a study page with four sections only — summary by topic with timestamp links, a tree (تشجير), supporting and opposing research, and "المطلوب: اعمل إيه" (actions, behaviors, beliefs) — in the Cairo font, exported to PDF and saved to the ملخصات folder. Use when the user sends a YouTube link and asks to summarize it (لخص، ملخص، كمل على دي، البلاي ليست).
---

# Video summary

The user sends a YouTube link (video or playlist) and wants a summary. Talk to them in Egyptian Arabic. Write the page itself in clear Modern Standard Arabic, quoting the speaker's Egyptian phrases inside «».

## Fixed preferences (do not ask)

- Font: **Cairo** everywhere (already in `assets/head.html`).
- Always export **PDF** and send it in the chat.
- Save everything in the summaries folder (`ملخصات/` at the repo root; override with env `SUMMARIES_DIR`): PDF at `ملخصات/NN - العنوان.pdf`, HTML at `ملخصات/html/NN - العنوان.html`, numbered after the last existing number, and add a row to `ملخصات/README.md`. Commit and push.
- Content: the four sections in `assets/body-template.html` and **nothing else** unless asked (no quizzes, no Q&A).
- Playlist: deliver **one video at a time**, then continue to the next without waiting. Check upload dates: playlists are often newest-first; work in the series' real order and label episode numbers correctly.

## Steps

1. **Get the transcript.** `pip install -U "yt-dlp[default]" deno` if missing, then run `scripts/get_subs.sh <workdir> <url>` in the background (it retries; YouTube rate-limits cloud IPs). Convert each VTT: `python3 -I scripts/vtt2txt.py <file.vtt> <out.txt>` (prefers `ar-orig`; output has a `[m:ss]` marker every ~90 s). Get the upload date with `yt-dlp --print "%(upload_date)s"`.
   - If a video has no captions and audio can't be downloaded from the server, tell the user plainly and offer: TurboScribe (paste the YouTube link), or a Cowork prompt that runs yt-dlp + faster-whisper on their machine and uploads the text.
2. **Read the whole transcript** (in parts if long). Do not summarize from a partial read.
3. **Write the body** from `assets/body-template.html`:
   - Summary: 6–10 topics in the speaker's order, each with a timestamp chip `https://youtu.be/<id>?t=<seconds>` (compute seconds carefully from the `[m:ss]` markers), a key idea, and bullet points with short quotes.
   - Tree: one root, 4–7 branches.
   - Research: 5–8 cards on the main claims. For each: what supports it, what opposes or limits it (real studies: author, year, journal), and a one-line verdict. Flag claims research contradicts (pill `no`), wrong numbers, and misattributed quotes. Never invent citations; if unsure, describe the finding without a citation or leave it out.
   - Do: a 4–6 step start order, an old→new belief table with timestamps, then 4–7 action cards (exercises, daily practices). Everything concrete.
4. **Assemble and export:**
   ```
   { echo "<title>العنوان</title>"; cat assets/head.html; cat body.html; } > page.html
   NODE_PATH=$(npm root -g) node scripts/to_pdf.js assets/fonts page.html "ملخصات/NN - العنوان.pdf"
   ```
   Check the log says `fonts loaded: Cairo`. Optionally render a page with `pdftoppm -r 50 -png -f 1 -l 1` and look at it.
5. **Publish** the page as an Artifact (icon `book`), copy the HTML to `ملخصات/html/`, run `python3 -I scripts/add_row.py NN "title" "pdf name without .pdf" "source label" "source url" "artifact url"`, commit, push, and send the PDF with SendUserFile.
6. **Reply** briefly in Egyptian Arabic: the link, what is in it, the 2–3 most important research corrections, and what comes next.

## Notes

- `scripts/to_pdf.js` embeds the Cairo woff2 files from `assets/fonts/` as data URIs, prints A4 in light mode with page numbers, and opens `<details>`.
- The page cannot be written to the user's laptop from a cloud session. If they want files on their computer, send a zip, or give a Cowork prompt that downloads the `ملخصات` folder from GitHub into their chosen path.
