"""App entrypoint: FastAPI (REST API) + Gradio UI mounted at /ui, served by one uvicorn process."""

import logging

import gradio as gr
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app import __version__
from app.api.routes import router
from app.config import get_settings
from app.core.exceptions import FinanceError
from app.logging_setup import configure_logging
from app.ui.gradio_ui import build_ui

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    api = FastAPI(title="yapp - Personal Finance Toolkit", version=__version__)
    api.include_router(router)

    @api.exception_handler(FinanceError)
    async def finance_error_handler(request: Request, exc: FinanceError) -> JSONResponse:
        logger.warning("Rejected %s %s: %s", request.method, request.url.path, exc)
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @api.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        return RedirectResponse(url="/ui")

    logger.info("Starting yapp v%s (env=%s)", __version__, settings.app_env)
    return gr.mount_gradio_app(api, build_ui(settings), path="/ui", max_file_size="1mb")


app = create_app()
