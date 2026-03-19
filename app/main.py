from fastapi import FastAPI

from app.api.v1.routers.events import router as events_router
from app.api.v1.routers.ws import router as ws_router
from app.core.config import settings
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title="Notification Service", version="1.0.0", debug=settings.debug)

    app.include_router(events_router)
    app.include_router(ws_router)

    return app


app = create_app()
