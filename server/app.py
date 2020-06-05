"""
Main App
"""
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, Depends, Response
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.docs import get_redoc_html

from server.config import app_logger
from server import __description__, __title__, __version__
from server.core import on_app_start, on_app_shutdown
from server.middleware import LogRequests, Auth
from server.database.models.user import User
from server.core.dependencies import get_current_user
from server.consts import HTTP_OK, FAVICON
from server.api import router as endpoints_router

logger = app_logger(__name__)


def create_app() -> FastAPI:

    app = FastAPI(
        title=__title__,
        description=__description__,
        version=__version__,
        redoc_url=None,
        docs_url=None,
        openapi_url=None
    )

    app.add_middleware(LogRequests)
    app.add_middleware(Auth)

    app.include_router(endpoints_router, prefix='/api/{api_key}')

    app.add_event_handler("startup", on_app_start(app, logger))
    app.add_event_handler("shutdown", on_app_shutdown(app, logger))

    @app.get("/")
    async def home():
        return HTTP_OK

    @app.get('/favicon.ico')
    def favicon():
        return FAVICON

    @app.get("/api/{api_key}/openapi.json")
    async def get_open_api_endpoint(
            api_key: str,
            user: User = Depends(get_current_user)
    ):
        return JSONResponse(get_openapi(title=__title__, version=__version__, routes=app.routes))

    @app.get("/api/{api_key}/docs")
    async def get_docs(
            api_key: str,
            user: User = Depends(get_current_user)
    ):
        if api_key:
            return get_swagger_ui_html(openapi_url=f"/api/{api_key}/openapi.json", title="fastAPI Docs")
        else:
            return get_swagger_ui_html(openapi_url=f"/api/openapi.json", title="fastAPI Docs")

    @app.get("/api/{api_key}/redoc")
    async def get_redoc(
            api_key: str,
            user: User = Depends(get_current_user)
    ):
        if api_key:
            return get_redoc_html(openapi_url=f"/api/{api_key}/openapi.json", title="fastAPI Docs")
        else:
            return get_redoc_html(openapi_url=f"/api/openapi.json", title="fastAPI Docs")

    return app
