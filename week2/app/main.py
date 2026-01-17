"""
Main FastAPI application.
Handles application setup, lifecycle, and exception handling.
"""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import get_frontend_dir, get_settings
from .db import init_db
from .exceptions import (
    ActionItemNotFoundError,
    AppException,
    DatabaseError,
    NoteNotFoundError,
    ValidationError,
)
from .routers import action_items, notes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_title,
    debug=settings.debug,
    description="A FastAPI application for extracting and managing action items from notes",
)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize the application on startup."""
    logger.info("Starting up application...")
    try:
        init_db()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Cleanup on application shutdown."""
    logger.info("Shutting down application...")


# Exception handlers
@app.exception_handler(NoteNotFoundError)
async def note_not_found_handler(request: Request, exc: NoteNotFoundError) -> JSONResponse:
    """Handle note not found errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "detail": f"Note with id {exc.note_id} not found"},
    )


@app.exception_handler(ActionItemNotFoundError)
async def action_item_not_found_handler(
    request: Request, exc: ActionItemNotFoundError
) -> JSONResponse:
    """Handle action item not found errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "detail": f"Action item with id {exc.action_item_id} not found",
        },
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Validation error", "detail": exc.message},
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """Handle database errors."""
    logger.error(f"Database error: {exc.message}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Database error", "detail": exc.message},
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle general application exceptions."""
    logger.error(f"Application error: {exc.message}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Application error", "detail": exc.message},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred" if not settings.debug else str(exc),
        },
    )


# Routes
@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the frontend HTML page."""
    html_path = get_frontend_dir() / "index.html"
    if not html_path.exists():
        logger.error(f"Frontend file not found: {html_path}")
        raise FileNotFoundError(f"Frontend file not found: {html_path}")
    return html_path.read_text(encoding="utf-8")


# Include routers
app.include_router(notes.router)
app.include_router(action_items.router)

# Mount static files
static_dir = get_frontend_dir()
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")