import json
import time
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.core.api_key_dep import get_api_key
from app.services.rate_limiter import check_rate_limit
from app.services.router_stream import route_stream
from app.services.cost_calculator import calculate_cost
from app.services.usage_logger import log_usage

router = APIRouter()


class GenerateRequest(BaseModel):
    prompt: str
    task_type: str = "auto"


@router.post("/v1/generate")
def generate(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    api_key=Depends(get_api_key),  
):
    check_rate_limit(api_key.api_key)

    start_time = time.time()

    route = route_stream(request.prompt)

    provider = route["provider"]
    model = route["model"]
    stream_source = route["stream"]

    def event_generator():
        collected_tokens = []

        input_tokens = len(request.prompt.split())

        try:

            for token in stream_source:
                collected_tokens.append(token)

                yield f"data: {json.dumps({'token': token})}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

        finally:

            output_tokens = len(collected_tokens)
            latency = time.time() - start_time

            cost = calculate_cost(
                input_tokens,
                output_tokens,
                provider
            )

            log_data = {
                "user_id": api_key.user_id,
                "api_key_id": api_key.id,
                "model": model,
                "provider": provider,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "cost": cost,
                "latency": latency,
                "cache_hit": False
            }


            background_tasks.add_task(log_usage, log_data)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


