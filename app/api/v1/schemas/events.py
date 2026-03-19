from datetime import datetime

from pydantic import BaseModel, HttpUrl

from app.domain.enums.event_type import EventType


class EventPayload(BaseModel):
    class StartedPayload(BaseModel):
        status: str

    class ProgressPayload(BaseModel):
        progress: int
        status: str

    class FinishedPayload(BaseModel):
        status: str
        download_url: HttpUrl

    type: EventType
    product: str
    job_id: str
    timestamp: datetime
    payload: StartedPayload | ProgressPayload | FinishedPayload
