# Developer Command Center - Claude Code Guide

## Project Overview

This is a minimal full-stack "developer's command center" application built with FastAPI and SQLite. It's designed as a learning playground for practicing AI-driven development workflows.

**Purpose:** Manage notes and action items through a simple web interface and REST API.

**Tech Stack:**
- Backend: FastAPI (Python web framework)
- Database: SQLite with SQLAlchemy ORM
- Frontend: Static HTML/CSS/JavaScript (no build tools needed)
- Testing: pytest
- Code Quality: black (formatter) + ruff (linter)

## Project Structure

```
week4/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── schemas.py           # Pydantic validation schemas
│   │   ├── db.py                # Database connection and session management
│   │   ├── routers/
│   │   │   ├── notes.py         # Notes CRUD endpoints
│   │   │   └── action_items.py  # Action items CRUD endpoints
│   │   └── services/
│   │       └── extract.py       # Text extraction utilities
│   └── tests/
│       ├── conftest.py          # Pytest fixtures and configuration
│       ├── test_notes.py        # Tests for notes endpoints
│       └── test_action_items.py # Tests for action items endpoints
├── frontend/
│   ├── index.html               # Main UI
│   ├── style.css                # Styling
│   └── app.js                   # Frontend logic
├── data/
│   ├── db.sqlite                # SQLite database (generated on first run)
│   └── seed.sql                 # Initial data (loaded automatically)
├── docs/
│   ├── TASKS.md                 # List of suggested improvements
│   └── API.md                   # API documentation (maintain manually)
├── .claude/
│   └── commands/                # Custom slash commands
├── Makefile                     # Common development commands
├── pre-commit-config.yaml       # Pre-commit hooks configuration
└── CLAUDE.md                    # This file
```

## Quick Start

### Initial Setup

1. **Activate environment:**
   ```bash
   conda activate cs146s
   ```

2. **(Optional) Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```
   This automatically runs black and ruff before each commit.

### Development Workflow

#### Running the Application

From the `week4/` directory:
```bash
make run
```

Access points:
- **Frontend:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (interactive Swagger UI)
- **OpenAPI Spec:** http://localhost:8000/openapi.json

Press `Ctrl+C` to stop the server.

#### Running Tests

```bash
make test          # Run all tests
make test-verbose  # Run with detailed output
```

Test a specific file:
```bash
pytest backend/tests/test_notes.py -v
```

Test a specific function:
```bash
pytest backend/tests/test_notes.py::test_list_notes -v
```

#### Code Quality

```bash
make format        # Auto-format with black
make lint          # Check linting with ruff
```

**Important:** Always run these before committing. Pre-commit hooks enforce this if installed.

## Coding Standards

### API Design Patterns

#### Endpoint Structure

Follow RESTful conventions:
- `GET /resource` - List all resources
- `GET /resource/{id}` - Get specific resource
- `POST /resource` - Create new resource
- `PUT /resource/{id}` - Update entire resource
- `PATCH /resource/{id}` - Partial update
- `DELETE /resource/{id}` - Delete resource

#### Response Models

Always use Pydantic schemas:
```python
from ..schemas import NoteRead, NoteCreate

@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    # Implementation
    pass
```

#### HTTP Status Codes

Use appropriate status codes:
- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation error
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server error (avoid by handling exceptions)

#### Error Handling

Always raise `HTTPException` for errors:
```python
from fastapi import HTTPException

note = db.get(Note, note_id)
if not note:
    raise HTTPException(status_code=404, detail="Note not found")
```

Never return error strings or generic exceptions.

### Database Patterns

#### Using SQLAlchemy

```python
from sqlalchemy import select
from ..models import Note

# Query all
notes = db.execute(select(Note)).scalars().all()

# Query with filter
note = db.execute(select(Note).where(Note.id == note_id)).scalar_one_or_none()

# Get by ID (shorthand)
note = db.get(Note, note_id)

# Create
note = Note(title="...", content="...")
db.add(note)
db.flush()      # Get ID without committing
db.refresh(note)

# Update
note.title = "New Title"
db.add(note)
db.commit()

# Delete
db.delete(note)
db.commit()
```

**Important:** Use `db.flush()` + `db.refresh()` when you need the ID immediately (e.g., to return in response).

#### Schema Changes

If you modify `models.py`:
1. **Delete the database:**
   ```bash
   rm data/db.sqlite
   ```
2. **Restart the app** - database will be recreated with new schema
3. **Update** `data/seed.sql` if seed data needs to change
4. **Update** `schemas.py` to match new models

**Note:** This app doesn't use migrations (Alembic) because it's a learning project. In production, always use migrations.

### Python Code Style

#### Type Hints (Required)

All function signatures must have type hints:
```python
# ✅ Good
def create_note(title: str, content: str) -> Note:
    pass

# ❌ Bad
def create_note(title, content):
    pass
```

#### Imports Organization

Organize imports in this order:
1. Standard library
2. Third-party packages
3. Local imports

```python
# Standard library
from typing import List

# Third-party
from fastapi import APIRouter, Depends
from sqlalchemy import select

# Local
from ..models import Note
from ..schemas import NoteRead
```

Black and ruff enforce this automatically.

#### Docstrings

Use docstrings for non-obvious functions:
```python
def search_notes(q: str, db: Session) -> List[Note]:
    """
    Search for notes by title or content.

    Args:
        q: Search query string (case-insensitive)
        db: Database session

    Returns:
        List of notes matching the query
    """
    pass
```

## Testing Standards

### Test Organization

- **One test file per router:** `test_notes.py`, `test_action_items.py`
- **Test fixtures in** `conftest.py` (shared across all tests)
- **Use descriptive names:** `test_<method>_<endpoint>_<scenario>`

### Test Structure

Follow Arrange-Act-Assert pattern:
```python
def test_create_note_success(client):
    # Arrange
    payload = {"title": "Test", "content": "Test content"}

    # Act
    response = client.post("/notes/", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test"
    assert "id" in data
```

### Coverage Goals

- **Minimum:** 70% overall coverage
- **Target:** 80% overall coverage
- **Ideal:** 90%+ overall coverage

Use `/test-coverage` command (if available) to check coverage.

### What to Test

For each endpoint, test:
1. **Happy path:** Valid request, successful response
2. **Validation:** Invalid data, 400 error
3. **Not found:** Non-existent resource, 404 error
4. **Edge cases:** Empty strings, boundary values, special characters

Example:
```python
# Happy path
def test_get_note_success(client, sample_note):
    response = client.get(f"/notes/{sample_note.id}")
    assert response.status_code == 200

# Not found
def test_get_note_not_found(client):
    response = client.get("/notes/99999")
    assert response.status_code == 404

# Edge case
def test_create_note_empty_title(client):
    response = client.post("/notes/", json={"title": "", "content": "test"})
    assert response.status_code == 400  # or 422 for validation
```

## Common Workflows

### Adding a New Endpoint

**Recommended approach (TDD):**

1. **Write the test first** (in appropriate test file):
   ```python
   def test_new_endpoint_success(client):
       response = client.post("/notes/archive", json={"note_id": 1})
       assert response.status_code == 200
   ```

2. **Run the test** - it should fail:
   ```bash
   pytest backend/tests/test_notes.py::test_new_endpoint_success
   ```

3. **Implement the endpoint** (in appropriate router file):
   ```python
   @router.post("/archive", response_model=NoteRead)
   def archive_note(note_id: int, db: Session = Depends(get_db)):
       # Implementation
       pass
   ```

4. **Run tests** until they pass:
   ```bash
   make test
   ```

5. **Format and lint:**
   ```bash
   make format
   make lint
   ```

6. **Update documentation** in `docs/API.md`

7. **Commit:**
   ```bash
   git add .
   git commit -m "feat: Add note archiving endpoint"
   ```

**Shortcut:** Use `/add-endpoint` command (if available) to automate this workflow.

### Modifying an Existing Endpoint

1. **Read existing tests** to understand current behavior
2. **Add new test cases** for the modification
3. **Update the endpoint** implementation
4. **Verify all tests pass** (not just new ones)
5. **Update documentation**

### Refactoring

1. **Ensure all tests pass** before refactoring:
   ```bash
   make test
   ```

2. **Make the refactoring** (rename, move, restructure)

3. **Run tests again** - they should still pass:
   ```bash
   make test
   ```

4. **If tests fail:**
   - The refactoring broke something - fix it
   - Tests were too tightly coupled to implementation - update tests

5. **Commit:**
   ```bash
   git commit -m "refactor: Rename extract_todos to extract_action_items"
   ```

## Safety Rules

### DO ✅

- ✅ **Write tests before implementing features** (TDD approach)
- ✅ **Run** `make test` **before every commit**
- ✅ **Use type hints** on all function parameters and return types
- ✅ **Handle errors gracefully** with HTTPException
- ✅ **Format code** with `make format` before committing
- ✅ **Work on feature branches**, not main
- ✅ **Use Pydantic schemas** for all request/response validation
- ✅ **Check** `make lint` **and fix issues** before committing
- ✅ **Update docs** when changing APIs

### DO NOT ❌

- ❌ **Never commit code with failing tests**
- ❌ **Never delete the database** without backing up important data
- ❌ **Never modify database schema** without a plan for existing data
- ❌ **Never skip pre-commit hooks** (`--no-verify` flag)
- ❌ **Never commit directly to main** - use feature branches
- ❌ **Never push secrets** to the repository
- ❌ **Never write raw SQL** - use SQLAlchemy ORM
- ❌ **Never use** `print()` **for debugging** - use proper logging or just read test output
- ❌ **Never deploy without running tests** first

## Debugging Tips

### API Debugging

1. **Use the interactive API docs:**
   - Go to http://localhost:8000/docs
   - Click "Try it out" on any endpoint
   - Enter test data and execute
   - See request/response in real-time

2. **Check server logs:**
   - The terminal where `make run` is running shows all requests
   - Look for stack traces on errors

3. **Use pytest verbose mode:**
   ```bash
   pytest -vv backend/tests/test_notes.py
   ```

### Database Debugging

1. **Check if database exists:**
   ```bash
   ls -la data/db.sqlite
   ```

2. **Reset database:**
   ```bash
   rm data/db.sqlite
   make run  # Database will be recreated
   ```

3. **Inspect database directly:**
   ```bash
   sqlite3 data/db.sqlite
   sqlite> .tables
   sqlite> SELECT * FROM notes;
   sqlite> .exit
   ```

### Test Debugging

1. **Run single test:**
   ```bash
   pytest backend/tests/test_notes.py::test_create_note_success -v
   ```

2. **Show print statements:**
   ```bash
   pytest -s backend/tests/test_notes.py
   ```

3. **Drop into debugger on failure:**
   ```bash
   pytest --pdb backend/tests/test_notes.py
   ```

## Git Workflow

### Branch Naming

Use descriptive branch names:
- `feature/search-notes` - New features
- `fix/note-validation` - Bug fixes
- `refactor/rename-models` - Refactoring
- `docs/api-documentation` - Documentation updates
- `test/coverage-improvement` - Test additions

### Commit Messages

Follow conventional commits format:
```
<type>: <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding tests
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `style`: Formatting changes (no code logic change)
- `chore`: Maintenance tasks

Examples:
```bash
git commit -m "feat: Add search endpoint for notes"
git commit -m "fix: Handle empty search query correctly"
git commit -m "test: Add edge cases for note creation"
git commit -m "docs: Update API.md with new endpoints"
```

### Pre-Commit Hooks

If you've run `pre-commit install`, these checks run automatically before each commit:
- **black** - Auto-formats Python code
- **ruff** - Lints Python code

If pre-commit fails:
1. Check the error message
2. Fix the issues (often black will auto-fix)
3. Stage the changes: `git add .`
4. Commit again

To skip hooks (NOT recommended):
```bash
git commit --no-verify
```

## Available Slash Commands

If custom commands are configured in `.claude/commands/`, you can use them:

### `/add-endpoint`
Creates a new API endpoint with TDD workflow.

Usage:
```
/add-endpoint POST /notes/archive "Archives a note"
```

### `/test-coverage`
Runs tests with coverage analysis.

Usage:
```
/test-coverage
/test-coverage backend/tests/test_notes.py
```

**Check `.claude/commands/` directory for available commands.**

## Troubleshooting

### "Address already in use" error

Port 8000 is already occupied.

Solution:
```bash
# Find the process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use a different port
uvicorn backend.app.main:app --reload --port 8001
```

### Tests fail with database errors

The test database might be corrupt.

Solution:
```bash
# Delete test database (separate from main db)
rm data/test_db.sqlite

# Run tests again
make test
```

### Pre-commit hooks not running

You haven't installed them.

Solution:
```bash
pre-commit install
```

### Imports failing

You might not be in the right directory.

Solution:
```bash
# Always run commands from week4/ directory
cd week4/
make run
```

## Resources

### Internal Documentation

- `docs/TASKS.md` - Suggested features to implement
- `docs/API.md` - API endpoint reference
- `.claude/commands/` - Custom automation commands

### External Documentation

- **FastAPI:** https://fastapi.tiangolo.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Pydantic:** https://docs.pydantic.dev/
- **pytest:** https://docs.pytest.org/

### Getting Help

1. **Check this file first** - most common questions are answered here
2. **Read the error message** - they're usually descriptive
3. **Check the API docs** - http://localhost:8000/docs
4. **Ask Claude** - but be specific about what's wrong

## Development Philosophy

This project follows these principles:

1. **Test-Driven Development (TDD):** Write tests before code
2. **Type Safety:** Use type hints everywhere
3. **Simplicity:** Avoid over-engineering
4. **Documentation:** Code should be self-documenting, but docs should exist
5. **Automation:** Repetitive tasks should be automated
6. **Standards:** Follow PEP 8 (enforced by black and ruff)

These principles make the codebase maintainable and reduce bugs.
