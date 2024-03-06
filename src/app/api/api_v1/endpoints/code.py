# Copyright (C) 2024, Quack AI.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0> for full license details.


from fastapi import APIRouter, Security, status
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_token_payload
from app.models import UserScope
from app.schemas.code import ChatHistory
from app.schemas.login import TokenPayload
from app.services.ollama import ollama_client
from app.services.telemetry import telemetry_client

router = APIRouter()


@router.post("/chat", status_code=status.HTTP_200_OK, summary="Chat with our code model")
async def chat(
    payload: ChatHistory,
    token_payload: TokenPayload = Security(get_token_payload, scopes=[UserScope.ADMIN, UserScope.USER]),
) -> StreamingResponse:
    telemetry_client.capture(token_payload.user_id, event="compute-chat")
    # Run analysis
    return StreamingResponse(
        ollama_client.chat(payload.model_dump()["messages"]).iter_content(chunk_size=8192),
        media_type="text/event-stream",
    )
