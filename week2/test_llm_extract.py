#!/usr/bin/env python3
"""
Simple test script to test extract_action_items_llm() function.
Run this script directly to test the LLM extraction without running the full test suite.
"""

import sys
from app.services.extract import extract_action_items_llm

def test_basic():
    """Test basic extraction with bullet points."""
    print("=" * 60)
    print("Test 1: Basic bullet points and checkboxes")
    print("=" * 60)
    
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """
    
    print(f"Input text:\n{text}")
    print("\nExtracting action items...")
    
    items = extract_action_items_llm(text)
    
    print(f"\nExtracted {len(items)} action items:")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    
    return items


def test_keywords():
    """Test extraction with keyword prefixes."""
    print("\n" + "=" * 60)
    print("Test 2: Keyword-prefixed lines")
    print("=" * 60)
    
    text = """
    Meeting notes:
    todo: Review the code
    action: Fix the bug in the API
    next: Deploy to production
    Regular sentence here.
    """
    
    print(f"Input text:\n{text}")
    print("\nExtracting action items...")
    
    items = extract_action_items_llm(text)
    
    print(f"\nExtracted {len(items)} action items:")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    
    return items


def test_imperative():
    """Test extraction with imperative sentences."""
    print("\n" + "=" * 60)
    print("Test 3: Imperative sentences")
    print("=" * 60)
    
    text = """
    During the meeting we discussed:
    Create a new feature for user authentication.
    Update the documentation.
    Fix the login bug.
    """
    
    print(f"Input text:\n{text}")
    print("\nExtracting action items...")
    
    items = extract_action_items_llm(text)
    
    print(f"\nExtracted {len(items)} action items:")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    
    return items


def test_empty():
    """Test with empty input."""
    print("\n" + "=" * 60)
    print("Test 4: Empty input")
    print("=" * 60)
    
    items = extract_action_items_llm("")
    print(f"Empty input returned {len(items)} items (should be 0)")
    assert items == [], "Empty input should return empty list"
    print("✓ Passed")


def main():
    """Run all tests."""
    print("Testing extract_action_items_llm() function")
    print("Make sure Ollama is running and the model is available!")
    print()
    
    try:
        test_basic()
        test_keywords()
        test_imperative()
        test_empty()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("\nMake sure:")
        print("  1. Ollama is running (check with: ollama list)")
        print("  2. The model is available (check with: ollama list)")
        print("  3. If needed, pull the model: ollama pull qwen3:1.7b")
        sys.exit(1)


if __name__ == "__main__":
    main()
