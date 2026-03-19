import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.v1.dependencies import connection_manager, job_storage

logger = logging.getLogger(__name__)
router = APIRouter(tags=["ws"])


@router.websocket("/ws")
async def websocket_handler(websocket: WebSocket) -> None:
    await websocket.accept()

    job_id = None

    try:
        while True:
            data = await websocket.receive_json()
            if data.get("action") == "subscribe":
                job_id = data.get("job_id")
                await connection_manager.subscribe_and_send(
                    job_id=job_id,
                    websocket=websocket,
                    storage=job_storage,
                )
    except WebSocketDisconnect:
        if job_id:
            connection_manager.unsubscribe(job_id=job_id, websocket=websocket)
