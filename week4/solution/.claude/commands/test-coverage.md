# Test Coverage Report

Runs the test suite with coverage analysis and provides actionable insights on what needs more testing.

## Arguments

- `$TARGET` (optional): Specific test file or directory to run. If not provided, runs all tests.
  - Examples: `backend/tests/test_notes.py`, `backend/tests/`, or leave empty for all tests

## Steps

### 1. Run Tests with Coverage

Execute pytest with coverage flags:
```bash
pytest $TARGET --cov=backend/app --cov-report=term-missing --cov-report=html -v
```

Explanation of flags:
- `--cov=backend/app`: Measure coverage for the application code
- `--cov-report=term-missing`: Show line numbers that aren't covered
- `--cov-report=html`: Generate HTML report for detailed view
- `-v`: Verbose output to see each test

### 2. Analyze Results

#### If Tests Fail

Show the failing test output and stop. Don't proceed to coverage analysis until tests pass.

Ask the user: "Tests failed. Would you like me to help debug, or do you want to fix them manually?"

#### If Tests Pass

Parse the coverage output and categorize files:

**Excellent coverage (≥90%):** List these files
**Good coverage (80-89%):** List these files
**Needs improvement (70-79%):** List these files
**Poor coverage (<70%):** List these files with specific line numbers missing

### 3. Identify Low-Coverage Areas

For each file with <80% coverage:
1. Show the file path
2. Show current coverage percentage
3. Show which lines/functions are not covered
4. Suggest what kind of tests are missing

Example:
```
backend/app/routers/notes.py: 72% coverage
Missing coverage:
- Lines 45-52: Error handling for duplicate notes
- Lines 67-70: Edge case for empty search query

Suggested tests:
- test_create_note_duplicate_title
- test_search_notes_empty_query
```

### 4. Generate HTML Report Link

The HTML coverage report is generated at: `htmlcov/index.html`

Tell the user:
```
📊 Detailed coverage report available at: htmlcov/index.html

To view:
- Open in browser: open htmlcov/index.html (Mac)
- Or: xdg-open htmlcov/index.html (Linux)
- Or: start htmlcov/index.html (Windows)

The HTML report shows exactly which lines need testing (highlighted in red).
```

### 5. Provide Summary and Recommendations

Create a summary:
```
=== Coverage Summary ===

Total Coverage: X%

Coverage by file:
✅ backend/app/main.py: 100%
✅ backend/app/db.py: 95%
⚠️  backend/app/routers/notes.py: 72%
❌ backend/app/routers/action_items.py: 45%
❌ backend/app/services/extract.py: 30%

Priority: Focus on files below 80% coverage.

Suggested next steps:
1. Add tests for action_items.py (current: 45%, need: +35%)
2. Add tests for extract.py (current: 30%, need: +50%)
3. Improve notes.py coverage (current: 72%, need: +8%)
```

### 6. Offer to Help

Ask the user:
```
Would you like me to:
a) Generate tests for the lowest coverage file?
b) Show you what specific scenarios are untested?
c) Exit and let you write tests manually?
```

Based on their choice:
- **Option a:** Use the `/add-test` command (if available) or write tests for the file
- **Option b:** Analyze the uncovered lines and list specific test scenarios
- **Option c:** Exit gracefully

## Safety Rules

- ✅ **Never modify application code** - only analyze coverage
- ✅ **Never delete the HTML report** - user might want to view it later
- ✅ **Never commit automatically** - this is an analysis tool
- ❌ **Don't generate tests automatically without asking**
- ❌ **Don't run tests in production** (check environment if possible)

## Rollback

No changes are made to code, so no rollback needed. The only artifacts created are:
- `.coverage` (coverage database)
- `htmlcov/` (HTML report directory)

These are safe to keep or delete.

## Example Usage

### Example 1: Run all tests

```
User: "/test-coverage"

Claude:
1. Runs pytest --cov=backend/app --cov-report=term-missing -v
2. All 27 tests pass ✓
3. Shows coverage summary:
   - Total: 78%
   - backend/app/main.py: 100%
   - backend/app/routers/notes.py: 85%
   - backend/app/routers/action_items.py: 60%
   - backend/app/services/extract.py: 45%
4. Highlights action_items.py and extract.py as needing work
5. Suggests specific test cases:
   - test_complete_item_already_completed (action_items.py)
   - test_extract_hashtags_multiple (extract.py)
6. Provides link to htmlcov/index.html
7. Asks if user wants help writing tests
```

### Example 2: Run specific test file

```
User: "/test-coverage backend/tests/test_notes.py"

Claude:
1. Runs pytest backend/tests/test_notes.py --cov=backend/app/routers/notes -v
2. 12 tests pass ✓
3. Shows coverage for notes.py only: 85%
4. Shows missing lines: 45-52 (error handling)
5. Suggests: test_create_note_validation_error
```

### Example 3: Tests fail

```
User: "/test-coverage"

Claude:
1. Runs pytest
2. 2 tests fail ✗
3. Shows failure output:
   - test_create_note_empty_title FAILED
   - test_delete_note_not_found FAILED
4. Stops coverage analysis
5. Asks: "Tests failed. Would you like me to help debug?"
```

## Expected Outputs

**When tests pass:**
```
=== Test Coverage Report ===

✅ All tests passed (27/27)

Total Coverage: 78%

Files by coverage:
✅ Excellent (≥90%):
   - backend/app/main.py: 100%
   - backend/app/db.py: 95%

⚠️  Good (80-89%):
   - backend/app/routers/notes.py: 85%

❌ Needs Work (<80%):
   - backend/app/routers/action_items.py: 60%
     Missing: Lines 28-35 (complete item edge cases)
   - backend/app/services/extract.py: 45%
     Missing: Lines 15-22, 40-45 (hashtag parsing)

📊 Detailed report: htmlcov/index.html

Suggestions:
1. Priority: Add tests for extract.py (need +35% coverage)
2. Add edge case tests for action_items.py (need +20%)

Would you like me to generate tests for the lowest coverage file?
```

**When tests fail:**
```
❌ Tests failed (25 passed, 2 failed)

Failures:
1. test_create_note_empty_title
   AssertionError: Expected 400 status code, got 500

2. test_delete_note_not_found
   HTTPException not raised

Coverage analysis skipped (fix failing tests first).

Would you like me to help debug these failures?
```

## Integration with Other Commands

This command works well with:
- `/add-test`: Generate tests for low-coverage files
- `/add-endpoint`: Check coverage after adding new endpoint
- Pre-commit hooks: Run before committing to ensure coverage standards

## Coverage Targets

Based on industry standards:
- **90%+**: Excellent - production ready
- **80-89%**: Good - acceptable for most projects
- **70-79%**: Fair - improve before shipping
- **<70%**: Poor - significant testing gaps

## Customization

Users can adjust coverage thresholds by modifying the categorization in step 2:
- Excellent: ≥90% → ≥95%
- Good: 80-89% → 85-94%
- Needs improvement: 70-79% → 75-84%
- Poor: <70% → <75%
