import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def cloud_model_generate(
    prompt: str,
    system_prompt: str = None,
    model: str = "llama-3.1-8b-instant",
    max_tokens: int = 200,
    timeout: int = 120,
    mode: str = "fast"
):

    if not GROQ_API_KEY:
        return {
            "success": False,
            "model": model,
            "response": None,
            "error": "Missing GROQ_API_KEY",
            "metadata": {}
        }

    url = "https://api.groq.com/openai/v1/chat/completions"

    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    if mode == "fast":
        max_tokens = min(max_tokens, 80)
        messages.append({
            "role": "system",
            "content": "Keep answers short (3–4 lines max)."
        })

    elif mode == "balanced":
        max_tokens = min(max_tokens, 150)

    elif mode == "detailed":
        max_tokens = min(max_tokens, 300)

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": max_tokens
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    start_time = time.time()

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()

        data = response.json()
        generated_text = data["choices"][0]["message"]["content"]

        latency = time.time() - start_time

        usage = data.get("usage", {})

        input_tokens = usage.get("prompt_tokens")
        output_tokens = usage.get("completion_tokens")

        return {
            "success": True,
            "model": model,
            "response": generated_text,

            "metadata": {
                "latency_seconds": latency,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": usage.get("total_tokens"),

                "provider": "cloud",
                "mode": mode
            }
        }

    except Exception as e:
        return {
            "success": False,
            "model": model,
            "response": None,
            "error": str(e),
            "metadata": {
                "latency_seconds": None,
                "input_tokens": None,
                "output_tokens": None,
                "total_tokens": None,
                "provider": "cloud",
                "mode": mode
            }
        }
    

