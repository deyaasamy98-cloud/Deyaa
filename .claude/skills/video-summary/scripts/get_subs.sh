#!/usr/bin/env bash
# usage: get_subs.sh <outdir> <youtube-url-or-playlist>
# Downloads Arabic subtitles (ar-orig preferred) for a video or every video in a playlist,
# retrying across player clients because YouTube rate-limits cloud IPs.
set -u
OUT="$1"; URL="$2"; mkdir -p "$OUT/subs"; cd "$OUT"
yt-dlp --flat-playlist --print "%(playlist_index|1)s|%(id)s|%(duration_string)s|%(title)s" "$URL" > list.txt 2>/dev/null
cut -d'|' -f1,2 list.txt | while IFS='|' read idx id; do printf '%02d|%s\n' "$idx" "$id"; done > ids.txt
for round in 1 2 3; do
  while IFS='|' read idx id; do
    ls subs/${idx}_*.vtt >/dev/null 2>&1 && continue
    for c in web_embedded ios default; do
      timeout 150 yt-dlp --extractor-args "youtube:player_client=$c" --ignore-no-formats-error --skip-download \
        --write-auto-subs --write-subs --sub-langs "ar-orig,ar" --sub-format vtt -o "subs/${idx}_${id}" \
        "https://www.youtube.com/watch?v=$id" > last.log 2>&1
      ls subs/${idx}_*.vtt >/dev/null 2>&1 && break
      grep -q "no subtitles for the requested" last.log && { echo "NOCAP $idx"; break; }
      sleep 12
    done
    ls subs/${idx}_*.vtt >/dev/null 2>&1 && echo "OK $idx" || echo "miss $idx r$round"
    sleep 8
  done < ids.txt
done
echo FINISHED
