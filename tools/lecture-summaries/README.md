# Lecture summary pipeline

Used for «ملخصات تراث ابن تيمية - الشيخ حسين عبد الرازق».

- **Audio source**: YouTube blocks cloud IPs, so audio comes from archive.org uploads of the same lectures
  (matched to the playlist by duration). `queue.tsv` maps lesson key (`L<playlist#>`) to the audio URL; `meta.json`
  has the playlist entries.
- **Transcription**: `transcribe_queue.py queue.tsv tx/ audio/` (faster-whisper `large-v3-turbo`, int8, CPU; ~0.3x realtime on 4 cores).
- **Build**: `build.py specs/LXXX.json OUT_DIR` renders the PDF and the mind/tree map PNGs with headless Chromium.
  Fonts (Google Fonts, installed to ~/.fonts): Noto Naskh Arabic (body), Noto Kufi Arabic (headings), Aref Ruqaa (cover title), Amiri / Amiri Quran (quotes, ayat).
- Spec fields: see `specs/L009.json` (sections → blocks of type p/h/quote/matn/list/box/table; mind; tree; notes; questions by type; expand).

Style decisions requested by the user: large font, green/gold/cream palette suited to a sharia lesson, one PDF per lecture
with a descriptive name, high-resolution maps (readable after Telegram compression), academic-style review questions grouped by type
with model answers, expansion topics, and never the words «حقيبة/حزمة مذاكرة».

## Parallel transcription workers
Each worker session runs, one lecture per invocation (each run stays well under the 2-hour background limit):

```
pip install faster-whisper
python3 -I tools/lecture-summaries/transcribe_queue.py tools/lecture-summaries/queue.tsv /tmp/tx /tmp/audio <COMMA_KEYS> 1
```
then copies `/tmp/tx/<KEY>.txt` to `tools/lecture-summaries/transcripts/`, commits, `git pull --rebase`, and pushes.
`L011.txt` covers playlist videos 11+12 (split at [068:14]); `L074.txt` + `L074b.txt` together are video 74.
