import asyncio
import json
from collections import deque

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/api")

event_queues = {}


def publish_event(session_id: str, event: dict) -> None:
    queue = event_queues.setdefault(session_id, deque())
    queue.append(event)


@router.get("/events")
async def events(request: Request, session_id: str) -> StreamingResponse:
    return StreamingResponse(
        event_stream(request, session_id),
        media_type="text/event-stream",
    )


async def event_stream(request: Request, session_id: str):
    queue = event_queues.setdefault(session_id, deque())

    while True:
        if await request.is_disconnected():
            break

        if queue:
            event = queue.popleft()
            yield f"data: {json.dumps(event)}\n\n"
        else:
            yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"

        await asyncio.sleep(1)
