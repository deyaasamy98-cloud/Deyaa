# Usage: transcribe_queue.py QUEUE_FILE OUT_DIR AUDIO_DIR [KEYS] [MAX_JOBS]
# QUEUE_FILE lines: key<TAB>url ; produces OUT_DIR/key.txt (timestamped).
# KEYS: optional comma list restricting which keys to process ("all" = every key).
# MAX_JOBS: optional; stop after transcribing this many lectures (keeps each run short).
# Resumable: audio is processed in 10-minute chunks saved under OUT_DIR/key.chunks/.
import sys, os, subprocess, time, numpy as np
from faster_whisper import WhisperModel
q, out, adir = sys.argv[1:4]
keys = None if len(sys.argv) < 5 or sys.argv[4] == "all" else set(sys.argv[4].split(","))
max_jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
done_jobs = 0
CH = 600
os.makedirs(out, exist_ok=True); os.makedirs(adir, exist_ok=True)
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
while True:
    jobs = [l.rstrip("\n").split("\t") for l in open(q, encoding="utf8") if l.strip()]
    todo = [(k, u) for k, u in jobs if not os.path.exists(f"{out}/{k}.txt") and (keys is None or k in keys)]
    if not todo or done_jobs >= max_jobs: break
    k, u = todo[0]
    mp3 = f"{adir}/{k}.mp3"
    if not os.path.exists(mp3):
        subprocess.run(["curl", "-sSL", "--retry", "5", "-C", "-", "-o", mp3 + ".part", u], check=True)
        os.rename(mp3 + ".part", mp3)
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    cdir = f"{out}/{k}.chunks"; os.makedirs(cdir, exist_ok=True)
    n = int(np.ceil(len(a) / (CH * 16000)))
    t = time.time()
    for i in range(n):
        cf = f"{cdir}/{i:03d}.txt"
        if os.path.exists(cf): continue
        seg = a[i * CH * 16000:(i + 1) * CH * 16000]
        segs, _ = model.transcribe(seg, language="ar", beam_size=1, vad_filter=True, condition_on_previous_text=False)
        lines = []
        for s in segs:
            st = s.start + i * CH
            lines.append(f"[{int(st//60):03d}:{int(st%60):02d}] {s.text.strip()}")
        open(cf + ".tmp", "w", encoding="utf8").write("\n".join(lines) + "\n")
        os.rename(cf + ".tmp", cf)
        print(k, "chunk", i + 1, "/", n, flush=True)
    with open(f"{out}/{k}.txt.tmp", "w", encoding="utf8") as f:
        for i in range(n): f.write(open(f"{cdir}/{i:03d}.txt", encoding="utf8").read())
    os.rename(f"{out}/{k}.txt.tmp", f"{out}/{k}.txt")
    os.remove(mp3)
    print(k, "done", round(time.time() - t), "s", flush=True)
    done_jobs += 1
