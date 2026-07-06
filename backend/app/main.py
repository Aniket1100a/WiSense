import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as FastAPIHTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.router import router as api_v1_router
from app.config.settings import Settings
from app.core.logging import configure_logging
from app.database.base import Base
from app.database.session import engine
from app.models import activity_log, capability, room, sensor, signalsample

settings = Settings()
configure_logging(settings.debug)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting WiSense backend application")
    if settings.debug or settings.environment == "development":
        logger.info("Creating missing database tables for development")
        Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down WiSense backend application")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan,
)


@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    """Custom CORS middleware for development mode."""

    if settings.debug or settings.environment == "development":
        if request.method == "OPTIONS":
            return JSONResponse(
                content={},
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD",
                    "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, ngrok-skip-browser-warning",
                    "Access-Control-Max-Age": "3600",
                },
            )

    response = await call_next(request)

    if settings.debug or settings.environment == "development":
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept, ngrok-skip-browser-warning"

    return response


@app.options("/{full_path:path}")
async def options_handler(full_path: str) -> JSONResponse:
    """Catch-all OPTIONS handler for preflight requests."""

    return JSONResponse(
        content={},
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, ngrok-skip-browser-warning",
            "Access-Control-Max-Age": "3600",
        },
    )


@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException) -> JSONResponse:
    """Handle known HTTP exceptions with JSON responses."""

    detail = exc.detail
    message = detail if isinstance(detail, str) else "Request failed"
    errors = detail if not isinstance(detail, str) else None
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": message,
            "data": None,
            "pagination": None,
            "errors": errors,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors and return structured JSON."""

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation failed",
            "data": None,
            "pagination": None,
            "errors": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions and preserve internal details from leaking."""

    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "data": None,
            "pagination": None,
            "errors": None,
        },
    )


app.include_router(health_router)
app.include_router(api_v1_router)
