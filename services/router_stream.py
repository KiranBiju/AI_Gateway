from app.services.local_model_stream import local_model_stream
from app.services.cloud_model_stream import cloud_model_stream
from app.utils.scoring import route_score


def route_stream(prompt: str, system_prompt="You are helpful"):

    score = route_score(prompt)
    print("ROUTING SCORE:", score)

    use_local = score < 8

    if use_local:
        return local_model_stream(prompt)
    else:
        return cloud_model_stream(prompt, system_prompt)