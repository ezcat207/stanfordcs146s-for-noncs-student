# Add API Endpoint

Creates a new FastAPI endpoint with full TDD workflow: tests first, then implementation, then documentation.

## Arguments

- `$METHOD`: HTTP method (GET, POST, PUT, DELETE)
- `$PATH`: Endpoint path (e.g., `/notes/archive` or `/action-items/{id}/priority`)
- `$DESCRIPTION`: Brief description of what this endpoint does

## Steps

### 1. Analyze the Endpoint

First, determine where this endpoint should live:
- If path starts with `/notes` → add to `backend/app/routers/notes.py`
- If path starts with `/action-items` → add to `backend/app/routers/action_items.py`
- Otherwise, ask user which router file to use

### 2. Write Tests First (TDD Approach)

Create or update the test file:
- Test file location: `backend/tests/test_<router_name>.py`
- Write at least 3 test cases:
  1. **Happy path:** Test successful request with valid data
  2. **Error case:** Test appropriate error response (404, 400, etc.)
  3. **Edge case:** Test boundary conditions or special scenarios

Test naming convention:
```python
def test_<method>_<endpoint>_<scenario>(client):
    # Example: test_post_notes_archive_success
    pass
```

Use the existing test fixtures (check the test file to see what's available).

### 3. Run Tests (They Should Fail)

Run the tests to verify they fail (since endpoint doesn't exist yet):
```bash
pytest backend/tests/test_<router_name>.py::test_<new_test> -v
```

Expected: Tests fail with appropriate error (endpoint not found or similar).

If tests don't fail, something is wrong with the test setup.

### 4. Implement the Endpoint

Add the new endpoint function to the appropriate router file:

```python
@router.$METHOD("$PATH", response_model=<ResponseSchema>, status_code=<StatusCode>)
def <function_name>(<parameters>, db: Session = Depends(get_db)):
    """
    $DESCRIPTION

    Parameters:
    - <param>: Description

    Returns:
    - <ResponseSchema>: Description

    Raises:
    - HTTPException: When and why
    """
    # Implementation here
    pass
```

Guidelines:
- Use type hints for all parameters
- Use Pydantic schemas for request/response validation
- Handle errors with appropriate HTTP status codes
- Add docstring explaining the endpoint

### 5. Run Tests Again (They Should Pass)

```bash
pytest backend/tests/test_<router_name>.py -v
```

If tests fail:
- Read the error message carefully
- Fix the implementation
- Run tests again
- Repeat until green

If tests pass:
- Run the full test suite to ensure nothing broke: `make test`

### 6. Check Code Quality

Run formatting and linting:
```bash
make format
make lint
```

Fix any linting errors that appear.

### 7. Update Documentation

Update `docs/API.md` (create if it doesn't exist):

Add a new section:
```markdown
### $METHOD $PATH

**Description:** $DESCRIPTION

**Request:**
```json
{
  // Example request body if applicable
}
```

**Response (Success):**
```json
{
  // Example response
}
```

**Errors:**
- 400: Validation error
- 404: Resource not found (if applicable)
- 500: Server error
```

### 8. Manual Verification (Optional but Recommended)

If `make run` is already running in another terminal:
- Open http://localhost:8000/docs
- Find your new endpoint
- Click "Try it out"
- Test with sample data
- Verify response matches expectations

### 9. Summary

Print a summary of what was created/modified:
```
✅ Endpoint Added Successfully!

Files Modified:
- backend/app/routers/<router>.py (added $METHOD $PATH)
- backend/tests/test_<router>.py (added X tests)
- docs/API.md (documented endpoint)

Tests: All passing ✓
Linting: Clean ✓

Next Steps:
1. Review the changes
2. Test manually at http://localhost:8000/docs
3. Commit: git add . && git commit -m "feat: Add $METHOD $PATH endpoint"
```

## Safety Rules

- ❌ **Never commit automatically** - let user review first
- ❌ **Never modify existing endpoints** without explicit user confirmation
- ❌ **Never delete tests or code** - only add/update
- ✅ **Always write tests before implementation** (TDD)
- ✅ **Always run full test suite** before declaring success
- ✅ **Always format and lint** before finishing

## Rollback

If something goes wrong:
1. The changes haven't been committed (safe)
2. User can manually undo with `git restore <file>`
3. Or use `git stash` to save changes for later

## Example Usage

```
User: "/add-endpoint POST /notes/{id}/archive 'Archives a note for later viewing'"

Claude:
1. Determines this goes in backend/app/routers/notes.py
2. Creates tests in backend/tests/test_notes.py:
   - test_post_notes_archive_success
   - test_post_notes_archive_not_found
   - test_post_notes_archive_already_archived
3. Runs tests → they fail (expected)
4. Implements the archive endpoint in notes.py
5. Runs tests → they pass ✓
6. Runs make format, make lint → clean ✓
7. Updates docs/API.md with new endpoint
8. Shows summary

Total time: ~3-5 minutes
```

## Expected Inputs/Outputs

**Valid inputs:**
- `$METHOD`: GET, POST, PUT, DELETE, PATCH
- `$PATH`: Any valid FastAPI path pattern
- `$DESCRIPTION`: Clear explanation of endpoint purpose

**Invalid inputs (will ask for clarification):**
- $METHOD: "ASDF" (not a valid HTTP method)
- $PATH: "notes" (missing leading slash)
- $DESCRIPTION: "" (empty description)

**Outputs:**
- New test functions in test file
- New endpoint function in router file
- Updated documentation
- Test results showing all green
- Lint/format confirmation
- Summary of changes
