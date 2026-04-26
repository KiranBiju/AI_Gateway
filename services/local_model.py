import requests
import time
import logging


def local_model_generate(
    prompt: str,
    system_prompt: str = None,
    model: str = "phi3",
    max_tokens: int = 60,
    timeout: int = 120,
    mode: str = "fast"   # fast | balanced | detailed
):
    url = "http://localhost:11434/api/generate"

    final_prompt = prompt
    if system_prompt:
        final_prompt = f"{system_prompt}\n\nUser: {prompt}"

    if mode == "fast":
        max_tokens = min(max_tokens, 60)
        final_prompt = f"Answer briefly in 3-4 lines.\n\n{final_prompt}"

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

        result = {
            "success": True,
            "model": model,

            "response": generated_text,

            "metadata": {
                "mode": mode,
                "latency_seconds": latency,

                "prompt_tokens": data.get("prompt_eval_count"),
                "output_tokens": data.get("eval_count"),

                "total_time_sec": (
                    data.get("total_duration", 0) / 1e9
                    if data.get("total_duration") else None
                ),

                "eval_time_sec": (
                    data.get("eval_duration", 0) / 1e9
                    if data.get("eval_duration") else None
                ),

                "max_tokens_used": max_tokens
            }
        }

        logging.info("PROMPT: %s", prompt)
        logging.info("RESPONSE: %s", generated_text)
        logging.info("METADATA: %s", result["metadata"])

        return result

    except requests.exceptions.Timeout:
        logging.error("TIMEOUT for prompt: %s", prompt)

        return {
            "success": False,
            "model": model,
            "response": None,
            "error": "timeout",
            "metadata": {
                "latency_seconds": None
            }
        }

    except requests.exceptions.RequestException as e:
        logging.error("REQUEST FAILED: %s | Prompt: %s", str(e), prompt)

        return {
            "success": False,
            "model": model,
            "response": None,
            "error": str(e),
            "metadata": {
                "latency_seconds": None
            }
        }