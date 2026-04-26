import requests
import time
import logging


def local_model_generate(
    prompt: str,
    system_prompt: str = None,
    model: str = "phi3",
    max_tokens: int = 120,
    timeout: int = 120,
    mode: str = "fast"
):
    url = "http://localhost:11434/api/generate"

    final_prompt = prompt

    if system_prompt:
        final_prompt = f"{system_prompt}\n\nUser: {prompt}"

    if mode == "fast":
        max_tokens = min(max_tokens, 120)
        final_prompt = f"Give a complete answer in 3–4 short sentences. Do not cut off mid-sentence.\n\n{final_prompt}"

    elif mode == "balanced":
        max_tokens = min(max_tokens, 120)

    elif mode == "detailed":
        max_tokens = min(max_tokens, 250)

    payload = {
        "model": model,
        "prompt": final_prompt,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.7
        }
    }

    start_time = time.time()

    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()

        data = response.json()
        generated_text = data.get("response", "")

        latency = time.time() - start_time

        input_tokens = data.get("prompt_eval_count")
        output_tokens = data.get("eval_count")

        return {
            "success": True,
            "model": model,
            "response": generated_text,

            "metadata": {
                "latency_seconds": latency,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": (
                    (input_tokens or 0) + (output_tokens or 0)
                    if input_tokens is not None and output_tokens is not None
                    else None
                ),
                "provider": "local",
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
                "provider": "local",
                "mode": mode
            }
        }
    
