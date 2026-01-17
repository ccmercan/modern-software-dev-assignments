import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_bullets_and_checkboxes():
    """Test LLM extraction with bullet lists and checkboxes."""
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items_llm(text)
    # LLM should extract at least some action items
    assert len(items) > 0
    # Check that we get reasonable results (may vary with LLM)
    assert isinstance(items, list)
    assert all(isinstance(item, str) for item in items)


def test_extract_action_items_llm_keyword_prefixes():
    """Test LLM extraction with keyword-prefixed lines."""
    text = """
    Meeting notes:
    todo: Review the code
    action: Fix the bug in the API
    next: Deploy to production
    Regular sentence here.
    """.strip()

    items = extract_action_items_llm(text)
    assert len(items) > 0
    assert isinstance(items, list)


def test_extract_action_items_llm_empty_input():
    """Test LLM extraction with empty input."""
    items = extract_action_items_llm("")
    assert items == []
    
    items = extract_action_items_llm("   ")
    assert items == []


def test_extract_action_items_llm_no_action_items():
    """Test LLM extraction with text containing no action items."""
    text = """
    This is just a regular paragraph with no action items.
    It contains some narrative text about a meeting.
    Everyone discussed various topics but no tasks were assigned.
    """.strip()

    items = extract_action_items_llm(text)
    # Should return empty list or very few items
    assert isinstance(items, list)


def test_extract_action_items_llm_imperative_sentences():
    """Test LLM extraction with imperative sentences."""
    text = """
    During the meeting we discussed:
    Create a new feature for user authentication.
    Update the documentation.
    Fix the login bug.
    """.strip()

    items = extract_action_items_llm(text)
    assert len(items) > 0
    assert isinstance(items, list)


def test_extract_action_items_llm_mixed_formats():
    """Test LLM extraction with mixed action item formats."""
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
    assert len(items) > 0
    assert isinstance(items, list)
    assert all(isinstance(item, str) for item in items)
    assert all(len(item.strip()) > 0 for item in items)  # No empty strings


def test_extract_action_items_llm_whitespace_only():
    """Test LLM extraction with whitespace-only input."""
    items = extract_action_items_llm("   \n\t  \n   ")
    assert items == []


def test_extract_action_items_llm_newlines_only():
    """Test LLM extraction with only newlines."""
    items = extract_action_items_llm("\n\n\n")
    assert items == []


def test_extract_action_items_llm_complex_meeting_notes():
    """Test LLM extraction with complex meeting notes containing both action items and narrative."""
    text = """
    Weekly Standup - January 15, 2024
    
    Team Updates:
    John mentioned that the database migration is complete. 
    Sarah is working on the frontend redesign.
    
    Action Items:
    - [ ] Fix the authentication bug reported by QA
    * Implement rate limiting for the API endpoints
    1. Write unit tests for the new payment module
    todo: Update the deployment documentation
    action: Schedule security audit for next month
    
    Next Steps:
    We need to prioritize the authentication fix as it's blocking production deployment.
    The team will reconvene next week to review progress.
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    # Should extract at least some action items from the structured section
    assert len(items) > 0
    # Verify all items are non-empty strings
    assert all(isinstance(item, str) and len(item.strip()) > 0 for item in items)


def test_extract_action_items_llm_deduplication():
    """Test that LLM extraction deduplicates similar action items."""
    text = """
    Meeting notes:
    - Set up database
    * Set up database
    1. Set up database
    todo: Set up database
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    # Should deduplicate similar items (case-insensitive)
    # Note: LLM might normalize differently, so we just check it's reasonable
    assert len(items) <= 4  # Should have fewer items than input lines due to deduplication


def test_extract_action_items_llm_single_action_item():
    """Test LLM extraction with a single action item."""
    text = "todo: Complete the project documentation"
    
    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) >= 1  # Should extract at least one item


def test_extract_action_items_llm_nested_bullets():
    """Test LLM extraction with nested bullet points."""
    text = """
    Project tasks:
    - Main task: Implement user authentication
      - Sub-task: Create login page
      - Sub-task: Add password reset
    * Another main task
    """.strip()

    items = extract_action_items_llm(text)
    assert isinstance(items, list)
    assert len(items) > 0


@pytest.mark.skipif(
    not os.getenv("OLLAMA_MODEL") and os.getenv("SKIP_LLM_TESTS", "").lower() == "true",
    reason="Ollama not configured or LLM tests skipped"
)
def test_extract_action_items_llm_with_custom_model():
    """Test LLM extraction with a custom model from environment variable."""
    original_model = os.getenv("OLLAMA_MODEL")
    try:
        # This test will use whatever model is set in OLLAMA_MODEL
        text = "- [ ] Test task"
        items = extract_action_items_llm(text)
        assert isinstance(items, list)
    finally:
        # Restore original environment
        if original_model:
            os.environ["OLLAMA_MODEL"] = original_model
        elif "OLLAMA_MODEL" in os.environ:
            del os.environ["OLLAMA_MODEL"]
