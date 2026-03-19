from dataclasses import dataclass

from app.domain.entities.event import BaseEvent


@dataclass
class JobFinishedEvent(BaseEvent):
    @dataclass
    class Payload:
        status: str
        download_url: str

    payload: Payload
