from dataclasses import dataclass
from typing import Any

from app.domain.enums.event_type import EventType


@dataclass
class BaseEvent:
    type: EventType
    product: str
    job_id: str
    timestamp: str
    payload: Any
