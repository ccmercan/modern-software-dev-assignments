#!/usr/bin/env python3
"""
Simplified test script that doesn't require FastAPI to be installed.
Tests the core refactoring components.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_all():
    """Run all tests that don't require FastAPI."""
    print("Testing TODO 3 Refactoring - Core Components")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Configuration
    print("1. Testing Configuration Module...")
    try:
        from app.config import get_settings, get_base_dir, get_data_dir, get_db_path
        settings = get_settings()
        assert settings.app_title == "Action Item Extractor"
        assert settings.ollama_model == "qwen3:1.7b"
        base_dir = get_base_dir()
        data_dir = get_data_dir()
        db_path = get_db_path()
        assert base_dir.exists()
        assert data_dir.exists() or data_dir.parent.exists()
        print("   ✓ Configuration works correctly")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Configuration failed: {e}")
        results.append(False)
    
    # Test 2: Schemas
    print("\n2. Testing Pydantic Schemas...")
    try:
        from app.schemas import ExtractRequest, CreateNoteRequest, ActionItemResponse
        # Test validation
        req = ExtractRequest(text="Valid text")
        assert req.text == "Valid text"
        try:
            ExtractRequest(text="   ")
            print("   ✗ Validation should have failed")
            results.append(False)
        except:
            print("   ✓ Schema validation works")
            results.append(True)
    except Exception as e:
        print(f"   ✗ Schemas failed: {e}")
        results.append(False)
    
    # Test 3: Exceptions
    print("\n3. Testing Custom Exceptions...")
    try:
        from app.exceptions import NoteNotFoundError, DatabaseError
        error = NoteNotFoundError(123)
        assert error.status_code == 404
        assert "123" in error.message
        print("   ✓ Custom exceptions work correctly")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Exceptions failed: {e}")
        results.append(False)
    
    # Test 4: Database
    print("\n4. Testing Database Layer...")
    try:
        from app.db import init_db, insert_note, get_note, insert_action_items
        init_db()
        note_id = insert_note("Test note")
        note = get_note(note_id)
        assert note is not None
        assert note["content"] == "Test note"
        items = insert_action_items(["Test item"], note_id)
        assert len(items) == 1
        print("   ✓ Database operations work correctly")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Database failed: {e}")
        results.append(False)
    
    # Test 5: Integration
    print("\n5. Testing Integration...")
    try:
        from app.schemas import ExtractRequest, ActionItemResponse
        from app.services.extract import extract_action_items
        from app.db import insert_action_items, list_action_items
        
        request = ExtractRequest(text="- [ ] Task 1\n* Task 2")
        items = extract_action_items(request.text)
        assert len(items) > 0
        ids = insert_action_items(items)
        db_items = list_action_items()
        assert len(db_items) > 0
        
        # Create response model
        response = ActionItemResponse(
            id=db_items[0]["id"],
            note_id=db_items[0]["note_id"],
            text=db_items[0]["text"],
            done=bool(db_items[0]["done"]),
            created_at=db_items[0]["created_at"]
        )
        assert response.id > 0
        print("   ✓ Integration test passed")
        results.append(True)
    except Exception as e:
        print(f"   ✗ Integration failed: {e}")
        import traceback
        traceback.print_exc()
        results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("✅ All core refactoring components are working!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(test_all())
