def route_score(prompt: str):
    words = len(prompt.split())
    prompt_lower = prompt.lower()

    simple_boost = 0
    if any(k in prompt_lower for k in ["what is", "define", "who is", "when is","short", "brief", "explain briefly", "Explain"]):
        simple_boost = -3

    cost = 1 if words < 10 else 3
    complexity = 1 if words < 15 else 5
    latency = 1 if words < 20 else 4

    return cost + complexity + latency + simple_boost