import requests
import json
from app.core.config import DEFAULT_OPTIONS


def local_model_stream(prompt: str, model="phi3"):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": DEFAULT_OPTIONS
    }

    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))

                token = data.get("response", "")
                done = data.get("done", False)

                if token:
                    yield token

                if done:
                    break