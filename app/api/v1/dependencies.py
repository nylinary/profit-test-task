from app.application.managers.connection_manager import ConnectionManager
from app.application.services.event_service import EventService
from app.application.storage.job_storage import JobStorage

connection_manager = ConnectionManager()
job_storage = JobStorage()


def get_event_service() -> EventService:
    return EventService(manager=connection_manager, storage=job_storage)
