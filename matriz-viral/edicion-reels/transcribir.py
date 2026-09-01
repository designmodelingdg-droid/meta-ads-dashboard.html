import json
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")

out = {}
for name in ["valor6-hook", "valor6-desarrollo", "valor6-cta"]:
    segments, info = model.transcribe(
        f"{name}.wav", language="es", word_timestamps=True, beam_size=5
    )
    words = []
    for seg in segments:
        for w in seg.words:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
    out[name] = words
    print(f"=== {name} ===")
    print(" ".join(x["w"] for x in words))

with open("palabras.json", "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("guardado palabras.json")
