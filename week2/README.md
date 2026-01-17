# Action Item Extractor

A FastAPI-based web application that extracts actionable items from free-form text notes. The application supports both heuristic-based extraction and LLM-powered extraction using Ollama, allowing users to convert meeting notes, to-do lists, and other text into structured action items.

## Overview

This application provides a simple yet powerful interface for extracting and managing action items from unstructured text. It features:

- **Dual Extraction Methods**: Heuristic-based pattern matching and LLM-powered intelligent extraction
- **Note Management**: Save and retrieve notes with associated action items
- **Action Item Tracking**: Mark items as done/not done with persistent storage
- **RESTful API**: Well-documented API endpoints with Pydantic schemas
- **Web Interface**: Simple HTML frontend for easy interaction

## Features

- ✅ Extract action items using rule-based heuristics (fast, pattern-based)
- 🤖 Extract action items using LLM (intelligent, context-aware)
- 📝 Save notes with extracted action items
- ✅ Mark action items as complete/incomplete
- 📋 List all notes and action items
- 🔍 Filter action items by note ID
- 🎯 Type-safe API with automatic validation
- 📊 Interactive web interface

## Project Structure

```
week2/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── db.py                # Database layer
│   ├── exceptions.py        # Custom exception classes
│   ├── schemas.py           # Pydantic request/response models
│   ├── routers/
│   │   ├── action_items.py  # Action items endpoints
│   │   └── notes.py          # Notes endpoints
│   └── services/
│       └── extract.py       # Extraction logic (heuristic + LLM)
├── frontend/
│   └── index.html           # Web interface
├── tests/
│   └── test_extract.py      # Unit tests
├── data/
│   └── app.db               # SQLite database (created automatically)
└── README.md                # This file
```

## Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/) (for dependency management)
- [Ollama](https://ollama.com/) (for LLM extraction - optional but recommended)
- An Ollama model (e.g., `qwen3:1.7b`, `llama3.2`, etc.)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd week2
```

### 2. Set Up Python Environment

If using conda (as mentioned in the assignment):

```bash
conda activate cs146s
```

### 3. Install Dependencies

Using Poetry:

```bash
poetry install
```

Or using pip:

```bash
pip install fastapi uvicorn pydantic python-dotenv ollama
```

### 4. Set Up Ollama (for LLM Extraction)

1. Install Ollama from [https://ollama.com](https://ollama.com)

2. Pull a model (start with a small one):

```bash
ollama pull qwen3:1.7b
```

3. Verify Ollama is running:

```bash
ollama list
```

## Configuration

The application can be configured using environment variables or a `.env` file:

```bash
# Database settings (optional)
DB_PATH=/path/to/database.db
DATA_DIR=/path/to/data/directory

# Ollama settings
OLLAMA_MODEL=qwen3:1.7b
OLLAMA_BASE_URL=http://localhost:11434

# Application settings
APP_TITLE=Action Item Extractor
DEBUG=false
```

Create a `.env` file in the project root with these variables, or set them in your environment.

## Running the Application

### Start the Server

From the project root:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Or if not using Poetry:

```bash
uvicorn week2.app.main:app --reload
```

The application will be available at:
- **Web Interface**: http://127.0.0.1:8000/
- **API Documentation**: http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative API Docs**: http://127.0.0.1:8000/redoc (ReDoc)

### Access the Web Interface

Open your browser and navigate to http://127.0.0.1:8000/

You can:
- Paste text into the textarea
- Click "Extract" for heuristic extraction
- Click "Extract LLM" for LLM-powered extraction
- Click "List Notes" to view all saved notes
- Toggle action items as done/not done

## API Endpoints

### Action Items

#### Extract Action Items (Heuristic)
```http
POST /action-items/extract
Content-Type: application/json

{
  "text": "Meeting notes:\n- [ ] Task 1\n* Task 2",
  "save_note": false
}
```

**Response:**
```json
{
  "note_id": null,
  "items": [
    {
      "id": 1,
      "note_id": null,
      "text": "Task 1",
      "done": false,
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

#### Extract Action Items (LLM)
```http
POST /action-items/extract-llm
Content-Type: application/json

{
  "text": "We should update the documentation and fix the bug.",
  "save_note": true
}
```

**Response:** Same as heuristic extraction

#### List Action Items
```http
GET /action-items?note_id=1
```

**Response:**
```json
[
  {
    "id": 1,
    "note_id": 1,
    "text": "Update documentation",
    "done": false,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Mark Action Item as Done
```http
POST /action-items/{action_item_id}/done
Content-Type: application/json

{
  "done": true
}
```

**Response:**
```json
{
  "id": 1,
  "done": true
}
```

### Notes

#### Create Note
```http
POST /notes
Content-Type: application/json

{
  "content": "Meeting notes content here"
}
```

**Response:**
```json
{
  "id": 1,
  "content": "Meeting notes content here",
  "created_at": "2024-01-01T00:00:00"
}
```

#### Get Single Note
```http
GET /notes/{note_id}
```

**Response:**
```json
{
  "id": 1,
  "content": "Meeting notes content here",
  "created_at": "2024-01-01T00:00:00"
}
```

#### List All Notes
```http
GET /notes
```

**Response:**
```json
[
  {
    "id": 1,
    "content": "Meeting notes content here",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

## Testing

### Run Unit Tests

Using pytest:

```bash
# Run all tests
poetry run pytest tests/

# Run only LLM extraction tests
poetry run pytest tests/test_extract.py -k "llm" -v

# Run with verbose output
poetry run pytest tests/test_extract.py -v
```

### Run Simple Test Scripts

The project includes several test scripts:

```bash
# Test LLM extraction functionality
python3 run_llm_tests.py

# Test refactored components
python3 test_refactor_simple.py
```

### Test the API

You can test the API using:

1. **Swagger UI**: Visit http://127.0.0.1:8000/docs
2. **curl**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/action-items/extract" \
        -H "Content-Type: application/json" \
        -d '{"text": "- [ ] Task 1", "save_note": false}'
   ```
3. **Web Interface**: Use the browser interface at http://127.0.0.1:8000/

## Extraction Methods

### Heuristic Extraction

The heuristic method uses pattern matching to identify action items:

- Bullet points: `-`, `*`, `•`, numbered lists (`1.`, `2.`, etc.)
- Keyword prefixes: `todo:`, `action:`, `next:`
- Checkboxes: `[ ]`, `[todo]`
- Imperative sentences starting with verbs like "Create", "Fix", "Update", etc.

**Pros:**
- Fast (instant)
- No external dependencies
- Predictable results

**Cons:**
- May miss items in natural language
- Limited to specific patterns

### LLM Extraction

The LLM method uses Ollama to intelligently extract action items:

- Understands context and natural language
- Can extract items from narrative text
- Handles various phrasings and structures

**Pros:**
- More intelligent extraction
- Handles natural language better
- Can extract items from complex text

**Cons:**
- Slower (10-20 seconds)
- Requires Ollama to be running
- Results may vary

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database for storing notes and action items
- **Ollama**: Local LLM inference for intelligent extraction
- **Uvicorn**: ASGI server for running FastAPI

## Development

### Code Structure

The application follows a clean architecture:

- **Routers**: Handle HTTP requests and responses
- **Schemas**: Define API contracts with Pydantic models
- **Services**: Business logic (extraction algorithms)
- **Database Layer**: Data persistence with error handling
- **Configuration**: Centralized settings management
- **Exceptions**: Custom exception hierarchy for error handling

### Adding New Features

1. **New Endpoint**: Add to appropriate router in `app/routers/`
2. **New Schema**: Define in `app/schemas.py`
3. **New Service**: Add to `app/services/`
4. **Database Operation**: Add function to `app/db.py`

## Troubleshooting

### Ollama Connection Issues

If LLM extraction fails:

1. Verify Ollama is running: `ollama list`
2. Check the model is available: `ollama pull qwen3:1.7b`
3. Verify `OLLAMA_BASE_URL` in configuration
4. Check application logs for detailed error messages

### Database Issues

If database operations fail:

1. Check `data/` directory exists and is writable
2. Verify database path in configuration
3. Check application logs for SQL errors

### Import Errors

If you see import errors:

1. Ensure all dependencies are installed: `poetry install`
2. Activate the correct Python environment
3. Check Python version: `python --version` (should be 3.11+)

## License

This project is part of a course assignment.

## Contributing

This is a course project. For questions or issues, please refer to the assignment instructions.
