from app.services.local_model import local_model_generate
from app.services.cloud_model import cloud_model_generate

from app.utils.safety import safe_call
from app.utils.scoring import route_score


def is_simple_query(prompt: str) -> bool:
    prompt_lower = prompt.lower()

    simple_keywords = [
        "what is", "define", "who is", "when is",
        "short", "brief", "explain briefly", "explain"
    ]

    complex_keywords = [
        "compare", "analyze", "why", "how",
        "advantages", "disadvantages",
        "architecture", "design", "step by step",
        "implementation", "generate"
    ]

    if any(k in prompt_lower for k in complex_keywords):
        return False

    if any(k in prompt_lower for k in simple_keywords):
        return True

    return len(prompt.split()) < 12


def is_truncated(text: str, output_tokens: int, max_tokens: int) -> bool:
    if not text:
        return False

    if output_tokens is not None and max_tokens is not None:
        return output_tokens >= max_tokens

    return False


# MAIN ROUTER
def route_request(
    prompt: str,
    task_type: str = "auto",   # auto | simple | complex
    system_prompt: str = "You are a helpful assistant",
    budget_mode: str = "balanced"  # low | balanced | high
):
    """
    Production-ready routing engine:
    - scoring-based routing
    - safe execution
    - fallback handling
    """

    #ROUTING DECISION (SCORING)

    score = route_score(prompt)
    print("ROUTING SCORE:", score)

    use_local = score < 8


    if task_type == "simple":
       use_local = True
    elif task_type == "complex":
       use_local = False

    if budget_mode == "low":
       use_local = True
    elif budget_mode == "high":
       use_local = False


    
    #MODEL EXECUTION

    result = None
    provider_used = None

   
    if use_local:
        result = safe_call(
            local_model_generate,
            prompt,
            system_prompt,
            mode="fast"
        )

        provider_used = "local"

        if not result.get("success"):
            result = safe_call(
                cloud_model_generate,
                prompt,
                system_prompt,
                mode="balanced"
            )
            provider_used = "cloud"
            result.setdefault("metadata", {})["fallback"] = True

    else:
        result = safe_call(
            cloud_model_generate,
            prompt,
            system_prompt,
            mode="balanced"
        )
        
        provider_used = "cloud"
   

    if result and result.get("success"):
        result.setdefault("metadata", {})
        result["metadata"]["routed_via"] = provider_used

        if "fallback" not in result["metadata"]:
            result["metadata"]["fallback"] = False

    return result



#CLI TEST
if __name__ == "__main__":
    import json

    print("\n MaaS Router (Advanced)\n")

    prompt = input("Enter your prompt: ")

    result = route_request(prompt)

    print("\n RESPONSE:\n")
    print(result["response"])

    print("\n METADATA:\n")
    print(json.dumps(result["metadata"], indent=2))

    