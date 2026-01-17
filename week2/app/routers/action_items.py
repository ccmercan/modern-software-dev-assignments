"""
Action items router.
Handles endpoints for extracting and managing action items.
"""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Query

from .. import db
from ..exceptions import ActionItemNotFoundError, DatabaseError
from ..schemas import (
    ActionItemResponse,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(request: ExtractRequest) -> ExtractResponse:
    """
    Extract action items from text using heuristic-based extraction.
    
    Args:
        request: ExtractRequest containing the text and optional save_note flag
        
    Returns:
        ExtractResponse with extracted action items and optional note_id
        
    Raises:
        DatabaseError: If database operations fail
    """
    try:
        note_id: Optional[int] = None
        if request.save_note:
            note_id = db.insert_note(request.text)
            logger.info(f"Saved note with id {note_id}")

        items = extract_action_items(request.text)
        logger.info(f"Extracted {len(items)} action items from text")
        
        ids = db.insert_action_items(items, note_id=note_id)
        
        action_items = [
            ActionItemResponse(
                id=item_id,
                note_id=note_id,
                text=item_text,
                done=False,
                created_at="",  # Will be set from DB if needed
            )
            for item_id, item_text in zip(ids, items)
        ]
        
        return ExtractResponse(note_id=note_id, items=action_items)
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in extract endpoint: {e}", exc_info=True)
        raise DatabaseError(f"Failed to extract action items: {str(e)}", original_error=e) from e


@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(request: ExtractRequest) -> ExtractResponse:
    """
    Extract action items from text using LLM-powered extraction via Ollama.
    
    Args:
        request: ExtractRequest containing the text and optional save_note flag
        
    Returns:
        ExtractResponse with extracted action items and optional note_id
        
    Raises:
        DatabaseError: If database operations fail
    """
    try:
        note_id: Optional[int] = None
        if request.save_note:
            note_id = db.insert_note(request.text)
            logger.info(f"Saved note with id {note_id}")

        items = extract_action_items_llm(request.text)
        logger.info(f"Extracted {len(items)} action items using LLM")
        
        ids = db.insert_action_items(items, note_id=note_id)
        
        action_items = [
            ActionItemResponse(
                id=item_id,
                note_id=note_id,
                text=item_text,
                done=False,
                created_at="",  # Will be set from DB if needed
            )
            for item_id, item_text in zip(ids, items)
        ]
        
        return ExtractResponse(note_id=note_id, items=action_items)
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in extract_llm endpoint: {e}", exc_info=True)
        raise DatabaseError(f"Failed to extract action items with LLM: {str(e)}", original_error=e) from e


@router.get("", response_model=list[ActionItemResponse])
def list_all(note_id: Optional[int] = Query(None, description="Filter by note ID")) -> list[ActionItemResponse]:
    """
    List all action items, optionally filtered by note_id.
    
    Args:
        note_id: Optional note ID to filter action items
        
    Returns:
        List of ActionItemResponse objects
        
    Raises:
        DatabaseError: If database operations fail
    """
    try:
        rows = db.list_action_items(note_id=note_id)
        return [
            ActionItemResponse(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=bool(r["done"]),
                created_at=r["created_at"],
            )
            for r in rows
        ]
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in list_all endpoint: {e}", exc_info=True)
        raise DatabaseError(f"Failed to list action items: {str(e)}", original_error=e) from e


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, request: MarkDoneRequest) -> MarkDoneResponse:
    """
    Mark an action item as done or not done.
    
    Args:
        action_item_id: The ID of the action item to update
        request: MarkDoneRequest with the done status
        
    Returns:
        MarkDoneResponse with the updated status
        
    Raises:
        ActionItemNotFoundError: If the action item doesn't exist
        DatabaseError: If database operations fail
    """
    try:
        # Check if action item exists by trying to get it
        items = db.list_action_items()
        if not any(item["id"] == action_item_id for item in items):
            raise ActionItemNotFoundError(action_item_id)
        
        db.mark_action_item_done(action_item_id, request.done)
        logger.info(f"Marked action item {action_item_id} as {'done' if request.done else 'not done'}")
        
        return MarkDoneResponse(id=action_item_id, done=request.done)
    except (ActionItemNotFoundError, DatabaseError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error in mark_done endpoint: {e}", exc_info=True)
        raise DatabaseError(f"Failed to mark action item as done: {str(e)}", original_error=e) from e


