import urllib.request
import json
from pathlib import Path

API_KEY = "sk-fish-4GPT3tSw1c0YN-rxK0jZiHDbpcAHIAAZlndZSbPyEB4"
VOICE_ID = "db0639bd49fd407e9845829ee044cfa4"

text = "众神最狠的刑罚，从来不是巨石，是永恒的无意义。"
payload = {
    "text": text,
    "reference_id": VOICE_ID,
    "format": "mp3",
    "temperature": 0.6,
    "top_p": 0.72,
    "repetition_penalty": 1.2
}

req = urllib.request.Request(
    "https://api.fish.audio/v1/tts",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "model": "s2.1-pro-free"
    }
)

with urllib.request.urlopen(req) as resp:
    data = resp.read()
    with open("test_voice_user.mp3", "wb") as f:
        f.write(data)
    print("Synthesized user voice successfully:", len(data), "bytes")
