#!/usr/bin/env python3
"""
Test script to verify TODO 3 refactoring changes.
Tests configuration, schemas, database, and basic functionality.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config():
    """Test configuration module."""
    print("=" * 60)
    print("Test 1: Configuration Module")
    print("=" * 60)
    
    try:
        from app.config import get_settings, get_base_dir, get_data_dir, get_db_path, get_frontend_dir
        
        settings = get_settings()
        print(f"  ✓ Settings loaded")
        print(f"    - App title: {settings.app_title}")
        print(f"    - Ollama model: {settings.ollama_model}")
        print(f"    - Debug mode: {settings.debug}")
        
        base_dir = get_base_dir()
        data_dir = get_data_dir()
        db_path = get_db_path()
        frontend_dir = get_frontend_dir()
        
        print(f"  ✓ Paths configured")
        print(f"    - Base dir: {base_dir}")
        print(f"    - Data dir: {data_dir}")
        print(f"    - DB path: {db_path}")
        print(f"    - Frontend dir: {frontend_dir}")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("\n" + "=" * 60)
    print("Test 2: Pydantic Schemas")
    print("=" * 60)
    
    try:
        from app.schemas import (
            ExtractRequest,
            CreateNoteRequest,
            MarkDoneRequest,
            ActionItemResponse,
            NoteResponse,
            ExtractResponse,
            MarkDoneResponse,
        )
        
        # Test ExtractRequest
        request = ExtractRequest(text="Test text", save_note=False)
        print(f"  ✓ ExtractRequest created: text='{request.text}', save_note={request.save_note}")
        
        # Test validation
        try:
            invalid = ExtractRequest(text="   ")  # Should fail
            print(f"  ✗ Validation failed - should have raised error")
            return False
        except Exception:
            print(f"  ✓ ExtractRequest validation works (rejected empty text)")
        
        # Test CreateNoteRequest
        note_request = CreateNoteRequest(content="Note content")
        print(f"  ✓ CreateNoteRequest created: content='{note_request.content}'")
        
        # Test MarkDoneRequest
        done_request = MarkDoneRequest(done=True)
        print(f"  ✓ MarkDoneRequest created: done={done_request.done}")
        
        # Test response models
        action_item = ActionItemResponse(
            id=1,
            note_id=None,
            text="Test item",
            done=False,
            created_at="2024-01-01T00:00:00"
        )
        print(f"  ✓ ActionItemResponse created: id={action_item.id}, text='{action_item.text}'")
        
        note_response = NoteResponse(
            id=1,
            content="Test note",
            created_at="2024-01-01T00:00:00"
        )
        print(f"  ✓ NoteResponse created: id={note_response.id}")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_exceptions():
    """Test custom exceptions."""
    print("\n" + "=" * 60)
    print("Test 3: Custom Exceptions")
    print("=" * 60)
    
    try:
        from app.exceptions import (
            NoteNotFoundError,
            ActionItemNotFoundError,
            DatabaseError,
            ValidationError,
        )
        
        # Test NoteNotFoundError
        note_error = NoteNotFoundError(123)
        assert note_error.status_code == 404
        assert "123" in note_error.message
        print(f"  ✓ NoteNotFoundError: {note_error.message} (status {note_error.status_code})")
        
        # Test ActionItemNotFoundError
        item_error = ActionItemNotFoundError(456)
        assert item_error.status_code == 404
        print(f"  ✓ ActionItemNotFoundError: {item_error.message} (status {item_error.status_code})")
        
        # Test DatabaseError
        db_error = DatabaseError("Test database error")
        assert db_error.status_code == 500
        print(f"  ✓ DatabaseError: {db_error.message} (status {db_error.status_code})")
        
        # Test ValidationError
        val_error = ValidationError("Invalid input")
        assert val_error.status_code == 400
        print(f"  ✓ ValidationError: {val_error.message} (status {val_error.status_code})")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database():
    """Test database layer."""
    print("\n" + "=" * 60)
    print("Test 4: Database Layer")
    print("=" * 60)
    
    try:
        from app.db import init_db, insert_note, get_note, list_notes, insert_action_items, list_action_items
        
        # Initialize database
        init_db()
        print("  ✓ Database initialized")
        
        # Test insert_note
        note_id = insert_note("Test note content")
        print(f"  ✓ Note inserted with id: {note_id}")
        
        # Test get_note
        note = get_note(note_id)
        assert note is not None
        assert note["content"] == "Test note content"
        print(f"  ✓ Note retrieved: id={note['id']}, content='{note['content']}'")
        
        # Test list_notes
        notes = list_notes()
        assert len(notes) > 0
        print(f"  ✓ Listed {len(notes)} notes")
        
        # Test insert_action_items
        items = ["Task 1", "Task 2", "Task 3"]
        item_ids = insert_action_items(items, note_id=note_id)
        assert len(item_ids) == 3
        print(f"  ✓ Inserted {len(item_ids)} action items: {item_ids}")
        
        # Test list_action_items
        action_items = list_action_items(note_id=note_id)
        assert len(action_items) >= 3
        print(f"  ✓ Listed {len(action_items)} action items for note {note_id}")
        
        # Test list all action items
        all_items = list_action_items()
        assert len(all_items) >= 3
        print(f"  ✓ Listed {len(all_items)} total action items")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_routers():
    """Test router imports and basic functionality."""
    print("\n" + "=" * 60)
    print("Test 5: Router Imports")
    print("=" * 60)
    
    try:
        from app.routers import action_items, notes
        
        # Check that routers are properly configured
        assert action_items.router is not None
        assert notes.router is not None
        print("  ✓ Routers imported successfully")
        
        # Check that schemas are used
        from app.schemas import ExtractRequest, CreateNoteRequest
        print("  ✓ Router schemas available")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_app():
    """Test main application setup."""
    print("\n" + "=" * 60)
    print("Test 6: Main Application")
    print("=" * 60)
    
    try:
        from app.main import app
        
        # Check that app is created
        assert app is not None
        print("  ✓ FastAPI app created")
        
        # Check that routers are included
        routes = [route.path for route in app.routes]
        assert "/action-items/extract" in routes or any("/action-items" in r for r in routes)
        assert "/notes" in routes or any("/notes" in r for r in routes)
        print(f"  ✓ Routers included ({len(routes)} routes)")
        
        # Check exception handlers
        assert len(app.exception_handlers) > 0
        print(f"  ✓ Exception handlers registered ({len(app.exception_handlers)} handlers)")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test integration: schema validation with database."""
    print("\n" + "=" * 60)
    print("Test 7: Integration Test")
    print("=" * 60)
    
    try:
        from app.schemas import ExtractRequest, ActionItemResponse
        from app.services.extract import extract_action_items
        from app.db import insert_action_items, list_action_items
        
        # Create a request
        request = ExtractRequest(text="- [ ] Task 1\n* Task 2", save_note=False)
        print(f"  ✓ Created ExtractRequest: text='{request.text[:30]}...'")
        
        # Extract action items
        items = extract_action_items(request.text)
        print(f"  ✓ Extracted {len(items)} action items")
        
        # Insert into database
        if items:
            ids = insert_action_items(items)
            print(f"  ✓ Inserted {len(ids)} items into database")
            
            # Retrieve and create response
            db_items = list_action_items()
            if db_items:
                response_item = ActionItemResponse(
                    id=db_items[0]["id"],
                    note_id=db_items[0]["note_id"],
                    text=db_items[0]["text"],
                    done=bool(db_items[0]["done"]),
                    created_at=db_items[0]["created_at"]
                )
                print(f"  ✓ Created ActionItemResponse from database: id={response_item.id}")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("Testing TODO 3 Refactoring Changes")
    print("=" * 60)
    print()
    
    tests = [
        ("Configuration", test_config),
        ("Schemas", test_schemas),
        ("Exceptions", test_exceptions),
        ("Database", test_database),
        ("Routers", test_routers),
        ("Main App", test_main_app),
        ("Integration", test_integration),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ Test crashed: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
