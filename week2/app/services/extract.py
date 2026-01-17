from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(text: str) -> List[str]:
    """
    Extract action items from text using an LLM via Ollama.
    
    This function uses Ollama's structured output feature to extract action items
    from free-form text. It identifies tasks, todos, and actionable items mentioned
    in the input text.
    
    Args:
        text: The input text to extract action items from.
        
    Returns:
        A list of extracted action items as strings. Returns empty list if no
        action items are found or if an error occurs.
    """
    if not text or not text.strip():
        return []
    
    # Get the model name from environment variable, default to a small model
    model_name = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")
    
    # Define the JSON schema for structured output (array of strings)
    schema = {
        "type": "object",
        "properties": {
            "action_items": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["action_items"]
    }
    
    # System prompt to guide the LLM
    system_prompt = """You are a helpful assistant that extracts action items from text.
An action item is a specific task, todo, or actionable item that needs to be completed.
Extract all action items from the given text, including:
- Items in bullet lists (with -, *, •, or numbers)
- Items prefixed with keywords like "todo:", "action:", "next:"
- Items with checkboxes like [ ] or [todo]
- Imperative sentences that describe tasks to be done
- Any other clearly actionable items

Return only the action items, cleaned of their prefixes and formatting.
Each action item should be a clear, concise description of what needs to be done.
If there are no action items, return an empty array."""
    
    try:
        # Call Ollama with structured output
        # Set temperature to 0 for more deterministic outputs
        response = chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract action items from the following text:\n\n{text}"}
            ],
            format=schema,
            options={"temperature": 0}  # More deterministic output
        )
        
        # Parse the response - Ollama returns response.message.content
        if response and hasattr(response, "message") and hasattr(response.message, "content"):
            content = response.message.content
            # The content should be a JSON string
            if isinstance(content, str):
                parsed = json.loads(content)
            else:
                # If it's already a dict, use it directly
                parsed = content if isinstance(content, dict) else {}
            
            # Extract the action_items array
            action_items = parsed.get("action_items", [])
            
            # Ensure we return a list of strings and filter out empty items
            result = [str(item).strip() for item in action_items if item and str(item).strip()]
            
            # Deduplicate while preserving order
            seen: set[str] = set()
            unique: List[str] = []
            for item in result:
                lowered = item.lower()
                if lowered not in seen:
                    seen.add(lowered)
                    unique.append(item)
            
            return unique
        else:
            # Fallback: try to extract from response if structure is unexpected
            return []
            
    except json.JSONDecodeError:
        # If JSON parsing fails, return empty list
        return []
    except Exception as e:
        # Log error and return empty list to gracefully handle failures
        # In production, you might want to log this error
        print(f"Error in extract_action_items_llm: {e}")
        return []
