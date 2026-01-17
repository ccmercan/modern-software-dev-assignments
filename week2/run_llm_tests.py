#!/usr/bin/env python3
"""
Simple test runner for extract_action_items_llm() tests.
This bypasses pytest to avoid environment conflicts.
"""

import sys
import os

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.extract import extract_action_items_llm


def test_bullets_and_checkboxes():
    """Test LLM extraction with bullet lists and checkboxes."""
    print("Test 1: Bullets and checkboxes")
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()
    
    items = extract_action_items_llm(text)
    assert len(items) > 0, "Should extract at least one item"
    assert isinstance(items, list), "Should return a list"
    assert all(isinstance(item, str) for item in items), "All items should be strings"
    print(f"  ✓ Passed - extracted {len(items)} items")
    return True


def test_keyword_prefixes():
    """Test LLM extraction with keyword-prefixed lines."""
    print("Test 2: Keyword prefixes")
    text = """
    Meeting notes:
    todo: Review the code
    action: Fix the bug in the API
    next: Deploy to production
    Regular sentence here.
    """.strip()
    
    items = extract_action_items_llm(text)
    assert len(items) > 0, "Should extract at least one item"
    assert isinstance(items, list), "Should return a list"
    print(f"  ✓ Passed - extracted {len(items)} items")
    return True


def test_empty_input():
    """Test LLM extraction with empty input."""
    print("Test 3: Empty input")
    items = extract_action_items_llm("")
    assert items == [], "Empty input should return empty list"
    
    items = extract_action_items_llm("   ")
    assert items == [], "Whitespace-only input should return empty list"
    print("  ✓ Passed")
    return True


def test_no_action_items():
    """Test LLM extraction with text containing no action items."""
    print("Test 4: No action items")
    text = """
    This is just a regular paragraph with no action items.
    It contains some narrative text about a meeting.
    Everyone discussed various topics but no tasks were assigned.
    """.strip()
    
    items = extract_action_items_llm(text)
    assert isinstance(items, list), "Should return a list"
    print(f"  ✓ Passed - returned {len(items)} items")
    return True


def test_imperative_sentences():
    """Test LLM extraction with imperative sentences."""
    print("Test 5: Imperative sentences")
    text = """
    During the meeting we discussed:
    Create a new feature for user authentication.
    Update the documentation.
    Fix the login bug.
    """.strip()
    
    items = extract_action_items_llm(text)
    assert len(items) > 0, "Should extract at least one item"
    assert isinstance(items, list), "Should return a list"
    print(f"  ✓ Passed - extracted {len(items)} items")
    return True


def test_mixed_formats():
    """Test LLM extraction with mixed action item formats."""
    print("Test 6: Mixed formats")
    text = """
    Team meeting summary:
    - [ ] Task one: Set up CI/CD pipeline
    * Task two: Write integration tests
    1. Task three: Update API documentation
    todo: Review pull requests
    action: Schedule demo meeting
    next: Deploy to staging
    We also need to refactor the authentication module.
    """.strip()
    
    items = extract_action_items_llm(text)
    assert len(items) > 0, "Should extract at least one item"
    assert isinstance(items, list), "Should return a list"
    assert all(isinstance(item, str) for item in items), "All items should be strings"
    assert all(len(item.strip()) > 0 for item in items), "No empty strings"
    print(f"  ✓ Passed - extracted {len(items)} items")
    return True


def test_whitespace_only():
    """Test LLM extraction with whitespace-only input."""
    print("Test 7: Whitespace only")
    items = extract_action_items_llm("   \n\t  \n   ")
    assert items == [], "Whitespace-only should return empty list"
    print("  ✓ Passed")
    return True


def test_single_action_item():
    """Test LLM extraction with a single action item."""
    print("Test 8: Single action item")
    text = "todo: Complete the project documentation"
    
    items = extract_action_items_llm(text)
    assert isinstance(items, list), "Should return a list"
    assert len(items) >= 1, "Should extract at least one item"
    print(f"  ✓ Passed - extracted {len(items)} items")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running extract_action_items_llm() Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_bullets_and_checkboxes,
        test_keyword_prefixes,
        test_empty_input,
        test_no_action_items,
        test_imperative_sentences,
        test_mixed_formats,
        test_whitespace_only,
        test_single_action_item,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"  ✗ Failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
