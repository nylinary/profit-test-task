import logging

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_event_service
from app.api.v1.schemas.events import EventPayload
from app.application.services.event_service import EventService
from app.domain.value_objects.event_request import EventRequest

router = APIRouter(tags=["events"])
logger = logging.getLogger(__name__)


@router.post("/events")
async def events(payload: EventPayload, service: EventService = Depends(get_event_service)) -> dict:
    logger.info(f"[{events.__name__}] Accepted POST request")
    req = EventRequest(
        type=payload.type,
        product=payload.product,
        job_id=payload.job_id,
        timestamp=payload.timestamp.isoformat(),
        payload=payload.payload.model_dump(),
    )
    await service.process(req=req)

    return {"status": "accepted"}
