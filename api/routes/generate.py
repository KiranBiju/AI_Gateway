import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.services.local_model_stream import local_model_stream
from app.services.router import route_request
from app.core.dependencies import get_api_key_user
from app.services.router_stream import route_stream

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    task_type: str = "auto"

@router.post("/v1/generate")
def generate(request: GenerateRequest):

    def stream():
        for token in route_stream(request.prompt):
            chunk = {
                "token": token
            }
            yield f"data: {json.dumps({'token': token})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")