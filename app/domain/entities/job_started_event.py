from dataclasses import dataclass

from app.domain.entities.event import BaseEvent


@dataclass
class JobStartedEvent(BaseEvent):
    @dataclass
    class Payload:
        status: str

    payload: Payload
