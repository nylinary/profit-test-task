from dataclasses import dataclass

from app.domain.enums.event_type import EventType


@dataclass
class EventRequest:
    type: EventType
    product: str
    job_id: str
    timestamp: str
    payload: dict
