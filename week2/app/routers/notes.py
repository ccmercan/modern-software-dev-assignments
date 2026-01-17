"""
Notes router.
Handles endpoints for creating and retrieving notes.
"""

from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter

from .. import db
from ..exceptions import DatabaseError, NoteNotFoundError
from ..schemas import CreateNoteRequest, NoteResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse)
def create_note(request: CreateNoteRequest) -> NoteResponse:
    """
    Create a new note.
    
    Args:
        request: CreateNoteRequest containing the note content
        
    Returns:
        NoteResponse with the created note details
        
    Raises:
        DatabaseError: If database operations fail
    """
    try:
        note_id = db.insert_note(request.content)
        logger.info(f"Created note with id {note_id}")
        note = db.get_note(note_id)
        if note is None:
            raise DatabaseError(f"Failed to retrieve created note {note_id}")
        return NoteResponse(
            id=note["id"],
            content=note["content"],
            created_at=note["created_at"],
        )
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_note endpoint: {e}", exc_info=True)
        raise DatabaseError(f"Failed to create note: {str(e)}", original_error=e) from e


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """
    Get a single note by ID.
    
    Args:
        note_id: The ID of the note to retrieve
        
    Returns:
        NoteResponse with the note details
        
    Raises:
        NoteNotFoundError: If the note doesn't exist
        DatabaseError: If database operations fail
    """
    try:
        row = db.get_note(note_id)
        if row is None:
            raise NoteNotFoundError(note_id)
        return NoteResponse(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"],
        )
    except (NoteNotFoundError, DatabaseError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_single_note endpoint: {e}", exc_info=True)
        raise DatabaseError(f"Failed to get note: {str(e)}", original_error=e) from e


@router.get("", response_model=List[NoteResponse])
def list_notes() -> List[NoteResponse]:
    """
    List all notes.
    
    Returns:
        List of NoteResponse objects
        
    Raises:
        DatabaseError: If database operations fail
    """
    try:
        rows = db.list_notes()
        return [
            NoteResponse(
                id=row["id"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in list_notes endpoint: {e}", exc_info=True)
        raise DatabaseError(f"Failed to list notes: {str(e)}", original_error=e) from e


