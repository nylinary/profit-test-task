from collections import defaultdict
from dataclasses import asdict

from fastapi import WebSocket

from app.application.storage.job_storage import JobStorage


class ConnectionManager:
    def __init__(self):
        self._subscriptions: dict[str, list[WebSocket]] = defaultdict(list)

    def subscribe(self, job_id: str, websocket: WebSocket) -> None:
        self._subscriptions[job_id].append(websocket)

    def unsubscribe(self, job_id: str, websocket: WebSocket) -> None:
        self._subscriptions[job_id].remove(websocket)

    async def broadcast(self, job_id: str, message: dict) -> None:
        for websocket in self._subscriptions.get(job_id, []):
            await websocket.send_json(message)

    async def subscribe_and_send(self, job_id: str, websocket: WebSocket, storage: JobStorage) -> None:
        self.subscribe(job_id=job_id, websocket=websocket)
        state = storage.get(job_id)
        if state:
            await websocket.send_json(asdict(state))
