import logging
from dataclasses import asdict

from fastapi import HTTPException

from app.application.managers.connection_manager import ConnectionManager
from app.application.storage.job_storage import JobState, JobStorage
from app.domain.entities.job_finished_event import JobFinishedEvent
from app.domain.entities.job_progress_event import JobProgressEvent
from app.domain.entities.job_started_event import JobStartedEvent
from app.domain.exceptions.validation import EventValidationError
from app.domain.validators.event_validator import EventValidator
from app.domain.value_objects.event_request import EventRequest

logger = logging.getLogger(__name__)


class EventService:
    def __init__(self, manager: ConnectionManager, storage: JobStorage) -> None:
        self.manager = manager
        self.storage = storage

    async def process(self, req: EventRequest) -> None:
        logger.info(f"[{self.__class__.__name__}.{self.process.__name__}] Processing")
        try:
            event = EventValidator.validate(req=req)
        except EventValidationError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        await self._dispatch(event)

    async def _dispatch(self, event) -> None:
        if isinstance(event, JobStartedEvent):
            await self._process_job_started(event)
        elif isinstance(event, JobProgressEvent):
            await self._process_job_progress(event)
        elif isinstance(event, JobFinishedEvent):
            await self._process_job_finished(event)

    async def _process_job_started(self, event: JobStartedEvent) -> None:
        state = JobState(
            job_id=event.job_id,
            product=event.product,
            status=event.payload.status,
            progress=None,
            updated_at=event.timestamp,
        )
        self.storage.save(state)
        await self.manager.broadcast(job_id=event.job_id, message=asdict(state))

    async def _process_job_progress(self, event: JobProgressEvent) -> None:
        state = JobState(
            job_id=event.job_id,
            product=event.product,
            status=event.payload.status,
            progress=event.payload.progress,
            updated_at=event.timestamp,
        )
        self.storage.save(state)
        await self.manager.broadcast(job_id=event.job_id, message=asdict(state))

    async def _process_job_finished(self, event: JobFinishedEvent) -> None:
        state = JobState(
            job_id=event.job_id,
            product=event.product,
            status=event.payload.status,
            progress=None,
            updated_at=event.timestamp,
        )
        self.storage.save(state)
        await self.manager.broadcast(job_id=event.job_id, message=asdict(state))
