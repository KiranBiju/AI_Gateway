from app.services.cloud_model import cloud_model_generate


def cloud_model_stream(prompt: str, system_prompt: str):
    result = cloud_model_generate(prompt, system_prompt)

    if not result.get("success"):
        yield "[ERROR]"
        return

    text = result["response"]

    # fake streaming (chunked)
    for word in text.split():
        yield word + " "