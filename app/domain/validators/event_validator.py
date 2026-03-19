import logging

from app.domain.entities.event import BaseEvent
from app.domain.entities.job_finished_event import JobFinishedEvent
from app.domain.entities.job_progress_event import JobProgressEvent
from app.domain.entities.job_started_event import JobStartedEvent
from app.domain.enums.event_type import EventType
from app.domain.exceptions.validation import EventValidationError
from app.domain.value_objects.event_request import EventRequest

logger = logging.getLogger(__name__)


class EventValidator:
    @staticmethod
    def validate(req: EventRequest) -> BaseEvent:
        logger.info(f"[{EventValidator.__name__}.{EventValidator.validate.__name__}] Validating event")
        try:
            return EventValidator._validate(req=req)
        except TypeError as exc:
            raise EventValidationError(f"Invalid data: {exc}") from exc

    @staticmethod
    def _validate(req: EventRequest) -> BaseEvent:
        if req.type == EventType.JOB_STARTED:
            return JobStartedEvent(
                type=req.type,
                product=req.product,
                job_id=req.job_id,
                timestamp=req.timestamp,
                payload=JobStartedEvent.Payload(**req.payload),
            )

        elif req.type == EventType.JOB_PROGRESS:
            return JobProgressEvent(
                type=req.type,
                product=req.product,
                job_id=req.job_id,
                timestamp=req.timestamp,
                payload=JobProgressEvent.Payload(**req.payload),
            )

        elif req.type == EventType.JOB_FINISHED:
            return JobFinishedEvent(
                type=req.type,
                product=req.product,
                job_id=req.job_id,
                timestamp=req.timestamp,
                payload=JobFinishedEvent.Payload(**req.payload),
            )

        raise EventValidationError(f"Unsupported type: {req.type}")
