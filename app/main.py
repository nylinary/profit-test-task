from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title="Notification Service", version="1.0.0", debug=settings.debug)

    return app


app = create_app()
