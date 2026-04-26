import requests
import time
import logging


def local_model_generate(prompt: str, system_prompt: str = None, timeout: int = 100):
    url = "http://localhost:11434/api/generate"

    final_prompt = prompt
    if system_prompt:
        final_prompt = f"{system_prompt}\n\nUser: {prompt}"

    payload = {
        "model": "phi3",
        "prompt": final_prompt,
        "stream": False,
        "options": {
            "num_predict": 120,       
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
            "model": payload["model"],
            "response": generated_text,

            "metadata": {
                "latency_seconds": latency,
                "eval_count": data.get("eval_count"),
                "prompt_eval_count": data.get("prompt_eval_count"),
                "total_duration_ns": data.get("total_duration"),
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
            "model": "phi3",
            "response": None,
            "error": "Request timed out",
            "metadata": {
                "latency_seconds": None
            }
        }

    except requests.exceptions.RequestException as e:
        logging.error("REQUEST FAILED: %s | Prompt: %s", str(e), prompt)

        return {
            "success": False,
            "model": "phi3",
            "response": None,
            "error": str(e),
            "metadata": {
                "latency_seconds": None
            }
        }
    
    