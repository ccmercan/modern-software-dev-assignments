"""
Database layer for the application.
Handles all database operations with proper error handling and transaction management.
"""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from typing import Optional

from .config import get_data_dir, get_db_path
from .exceptions import DatabaseError

logger = logging.getLogger(__name__)


def ensure_data_directory_exists() -> None:
    """Ensure the data directory exists."""
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection():
    """
    Context manager for database connections.
    Ensures proper cleanup and error handling.
    """
    ensure_data_directory_exists()
    db_path = get_db_path()
    connection = None
    try:
        connection = sqlite3.connect(str(db_path))
        connection.row_factory = sqlite3.Row
        yield connection
        connection.commit()
    except sqlite3.Error as e:
        if connection:
            connection.rollback()
        logger.error(f"Database error: {e}", exc_info=True)
        raise DatabaseError(str(e), original_error=e) from e
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Unexpected database error: {e}", exc_info=True)
        raise DatabaseError(f"Unexpected error: {str(e)}", original_error=e) from e
    finally:
        if connection:
            connection.close()


def init_db() -> None:
    """
    Initialize the database by creating tables if they don't exist.
    Should be called during application startup.
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER,
                    text TEXT NOT NULL,
                    done INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (note_id) REFERENCES notes(id)
                );
                """
            )
            logger.info("Database initialized successfully")
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        raise DatabaseError(f"Failed to initialize database: {str(e)}", original_error=e) from e


def insert_note(content: str) -> int:
    """
    Insert a new note into the database.
    
    Args:
        content: The content of the note
        
    Returns:
        The ID of the newly created note
        
    Raises:
        DatabaseError: If the database operation fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            note_id = int(cursor.lastrowid)
            logger.debug(f"Inserted note with id {note_id}")
            return note_id
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Failed to insert note: {e}", exc_info=True)
        raise DatabaseError(f"Failed to insert note: {str(e)}", original_error=e) from e


def list_notes() -> list[sqlite3.Row]:
    """
    List all notes from the database.
    
    Returns:
        List of note rows ordered by ID descending
        
    Raises:
        DatabaseError: If the database operation fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
            notes = list(cursor.fetchall())
            logger.debug(f"Retrieved {len(notes)} notes")
            return notes
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Failed to list notes: {e}", exc_info=True)
        raise DatabaseError(f"Failed to list notes: {str(e)}", original_error=e) from e


def get_note(note_id: int) -> Optional[sqlite3.Row]:
    """
    Get a note by its ID.
    
    Args:
        note_id: The ID of the note to retrieve
        
    Returns:
        The note row if found, None otherwise
        
    Raises:
        DatabaseError: If the database operation fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            if row:
                logger.debug(f"Retrieved note with id {note_id}")
            else:
                logger.debug(f"Note with id {note_id} not found")
            return row
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Failed to get note {note_id}: {e}", exc_info=True)
        raise DatabaseError(f"Failed to get note: {str(e)}", original_error=e) from e


def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    """
    Insert multiple action items into the database.
    
    Args:
        items: List of action item texts to insert
        note_id: Optional ID of the associated note
        
    Returns:
        List of IDs of the newly created action items
        
    Raises:
        DatabaseError: If the database operation fails
    """
    if not items:
        return []
    
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            ids: list[int] = []
            for item in items:
                cursor.execute(
                    "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                    (note_id, item),
                )
                ids.append(int(cursor.lastrowid))
            logger.debug(f"Inserted {len(ids)} action items")
            return ids
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Failed to insert action items: {e}", exc_info=True)
        raise DatabaseError(f"Failed to insert action items: {str(e)}", original_error=e) from e


def list_action_items(note_id: Optional[int] = None) -> list[sqlite3.Row]:
    """
    List action items from the database.
    
    Args:
        note_id: Optional filter to only return items for a specific note
        
    Returns:
        List of action item rows ordered by ID descending
        
    Raises:
        DatabaseError: If the database operation fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            if note_id is None:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
                )
            else:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                    (note_id,),
                )
            items = list(cursor.fetchall())
            logger.debug(f"Retrieved {len(items)} action items" + (f" for note {note_id}" if note_id else ""))
            return items
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Failed to list action items: {e}", exc_info=True)
        raise DatabaseError(f"Failed to list action items: {str(e)}", original_error=e) from e


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    """
    Mark an action item as done or not done.
    
    Args:
        action_item_id: The ID of the action item to update
        done: Whether the item is done
        
    Raises:
        DatabaseError: If the database operation fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            if cursor.rowcount == 0:
                logger.warning(f"Action item {action_item_id} not found for update")
            else:
                logger.debug(f"Updated action item {action_item_id} done status to {done}")
    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Failed to mark action item {action_item_id} as done: {e}", exc_info=True)
        raise DatabaseError(f"Failed to update action item: {str(e)}", original_error=e) from e


