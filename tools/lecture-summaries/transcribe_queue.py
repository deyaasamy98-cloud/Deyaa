# Usage: transcribe_queue.py QUEUE_FILE OUT_DIR AUDIO_DIR
# QUEUE_FILE lines: key<TAB>url ; produces OUT_DIR/key.txt (timestamped)
import sys, os, subprocess, time, numpy as np
from faster_whisper import WhisperModel
q, out, adir = sys.argv[1:4]
os.makedirs(out, exist_ok=True); os.makedirs(adir, exist_ok=True)
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
while True:
    jobs = [l.rstrip("\n").split("\t") for l in open(q, encoding="utf8") if l.strip()]
    todo = [(k, u) for k, u in jobs if not os.path.exists(f"{out}/{k}.txt")]
    if not todo: break
    k, u = todo[0]
    mp3 = f"{adir}/{k}.mp3"
    if not os.path.exists(mp3):
        subprocess.run(["curl", "-sSL", "--retry", "4", "-o", mp3 + ".part", u], check=True)
        os.rename(mp3 + ".part", mp3)
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    t = time.time()
    segs, _ = model.transcribe(a, language="ar", beam_size=1, vad_filter=True, condition_on_previous_text=False)
    with open(f"{out}/{k}.part", "w", encoding="utf8") as f:
        for s in segs:
            f.write(f"[{int(s.start//60):03d}:{int(s.start%60):02d}] {s.text.strip()}\n"); f.flush()
    os.rename(f"{out}/{k}.part", f"{out}/{k}.txt")
    os.remove(mp3)
    print(k, "done", round(time.time() - t), "s", flush=True)
