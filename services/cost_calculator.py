def calculate_cost(input_tokens, output_tokens, provider):
    if not input_tokens or not output_tokens:
        return 0

    if provider == "local":
        return 0

    # simple pricing (update later)
    return (input_tokens * 0.000001) + (output_tokens * 0.000002)