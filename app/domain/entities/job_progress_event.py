from dataclasses import dataclass

from app.domain.entities.event import BaseEvent


@dataclass
class JobProgressEvent(BaseEvent):
    @dataclass
    class Payload:
        status: str
        progress: int

    payload: Payload
