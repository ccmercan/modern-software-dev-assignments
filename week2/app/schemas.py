"""
Pydantic schemas for API request and response models.
Provides type safety and automatic validation for API contracts.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# Request Schemas
class ExtractRequest(BaseModel):
    """Request schema for extracting action items from text."""
    
    text: str = Field(..., min_length=1, description="The text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the text as a note")
    
    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v: str) -> str:
        """Ensure text is not just whitespace."""
        if not v.strip():
            raise ValueError("text cannot be empty or only whitespace")
        return v.strip()


class CreateNoteRequest(BaseModel):
    """Request schema for creating a new note."""
    
    content: str = Field(..., min_length=1, description="The content of the note")
    
    @field_validator("content")
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        """Ensure content is not just whitespace."""
        if not v.strip():
            raise ValueError("content cannot be empty or only whitespace")
        return v.strip()


class MarkDoneRequest(BaseModel):
    """Request schema for marking an action item as done/not done."""
    
    done: bool = Field(default=True, description="Whether the action item is done")


# Response Schemas
class ActionItemResponse(BaseModel):
    """Response schema for an action item."""
    
    id: int = Field(..., description="Unique identifier for the action item")
    note_id: Optional[int] = Field(None, description="ID of the associated note, if any")
    text: str = Field(..., description="The action item text")
    done: bool = Field(..., description="Whether the action item is completed")
    created_at: str = Field(..., description="ISO timestamp of when the item was created")
    
    class Config:
        from_attributes = True


class NoteResponse(BaseModel):
    """Response schema for a note."""
    
    id: int = Field(..., description="Unique identifier for the note")
    content: str = Field(..., description="The content of the note")
    created_at: str = Field(..., description="ISO timestamp of when the note was created")
    
    class Config:
        from_attributes = True


class ExtractResponse(BaseModel):
    """Response schema for action item extraction."""
    
    note_id: Optional[int] = Field(None, description="ID of the created note, if save_note was True")
    items: List[ActionItemResponse] = Field(..., description="List of extracted action items")


class MarkDoneResponse(BaseModel):
    """Response schema for marking an action item as done."""
    
    id: int = Field(..., description="ID of the action item")
    done: bool = Field(..., description="Whether the action item is done")
