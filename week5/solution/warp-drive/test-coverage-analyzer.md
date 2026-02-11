# Warp Drive Saved Prompt: Test Coverage Analyzer

**Name:** Test Coverage Analyzer

**Description:** Runs pytest with coverage analysis and provides actionable insights on what needs testing

**Category:** Testing & Quality

**Tags:** pytest, coverage, testing, quality-assurance

---

## Prompt

Run comprehensive test coverage analysis for `{target}`.

### Steps

1. **Execute tests with coverage:**
   ```bash
   pytest {target} --cov=backend/app --cov-report=term-missing --cov-report=html -v
   ```

2. **Handle test failures:**
   - If tests fail:
     * Show the failing test output in full
     * Stop execution immediately
     * Ask user: "Tests failed. Options: (a) Help me debug (b) I'll fix manually (c) Abort"
     * Wait for user choice before proceeding
   - If tests pass: Continue to step 3

3. **Parse and categorize coverage results:**

   Organize files into categories:
   - **Excellent (≥90%):** List all files in this category
   - **Good (80-89%):** List all files in this category
   - **Needs Work (70-79%):** List files with current percentage
   - **Poor (<70%):** List files with current percentage and priority flag

4. **Detailed analysis for low-coverage files:**

   For each file below 80% coverage:
   - Show current coverage percentage
   - List specific line ranges that are untested (from term-missing report)
   - Analyze the code to understand what those lines do
   - Suggest 2-3 specific, concrete test scenarios that would cover those lines

   Example format:
   ```
   backend/app/routers/action_items.py: 65% coverage
   Missing coverage:
   - Lines 28-35: Error handling for non-existent action item
   - Lines 42-45: Bulk complete with transaction rollback
   - Lines 58-62: Edge case for empty description

   Suggested tests:
   1. test_complete_item_not_found
      - Attempt to complete item ID 99999
      - Should return 404
      - Verify error message

   2. test_bulk_complete_partial_failure
      - Submit IDs: [1, 2, 99999, 4]
      - Should rollback transaction when ID 99999 fails
      - Verify none are completed

   3. test_create_item_empty_description
      - Submit description: ""
      - Should return 400 validation error
   ```

5. **Generate summary report:**

   ```
   === Test Coverage Summary ===

   Total Coverage: {percentage}%

   Coverage Breakdown:
   ✅ Excellent (≥90%): {count} files
      - {file1}: {pct}%
      - {file2}: {pct}%

   ⚠️ Good (80-89%): {count} files
      - {file1}: {pct}%

   ❌ Needs Work (<80%): {count} files
      - {file1}: {pct}% (PRIORITY)
      - {file2}: {pct}%

   📊 Detailed HTML Report: htmlcov/index.html
   To view: open htmlcov/index.html (Mac) or xdg-open htmlcov/index.html (Linux)

   Priority Improvements:
   1. {lowest_file}: {current}% → target 80% (need +{delta}%)
      Next tests to write:
      - {test1}
      - {test2}

   2. {second_lowest}: {current}% → target 80% (need +{delta}%)
      Next tests to write:
      - {test1}
   ```

6. **Offer assistance:**

   Ask: "Would you like me to generate tests for {lowest_coverage_file}? (y/n)"

   If yes:
   - Generate test file or add to existing
   - Write 2-3 tests covering the highest-priority gaps
   - Run tests to verify they work
   - Re-run coverage to show improvement

   If no:
   - Exit gracefully with summary

### Variables

- **target** (optional)
  - Description: Test file or directory to analyze
  - Default: `backend/tests/`
  - Examples: `backend/tests/test_notes.py`, `backend/tests/`, `backend/tests/test_routers/`

### Safety Rules

- ❌ Never modify application code (backend/app/) - analysis only
- ❌ Never commit automatically - always let user review
- ❌ Never generate tests without explicit permission (step 6)
- ✅ Artifacts created: `.coverage`, `htmlcov/` (safe to delete)
- ✅ Can run multiple times safely (idempotent)

### Expected Output

**When tests pass and coverage is analyzed:**

```
Running: pytest backend/tests/ --cov=backend/app --cov-report=term-missing -v

✅ All tests passed (27/27)

=== Test Coverage Summary ===

Total Coverage: 78%

Coverage Breakdown:
✅ Excellent (≥90%): 3 files
   - backend/app/main.py: 100%
   - backend/app/db.py: 95%
   - backend/app/schemas.py: 92%

⚠️ Good (80-89%): 1 file
   - backend/app/routers/notes.py: 85%

❌ Needs Work (<80%): 2 files
   - backend/app/routers/action_items.py: 65% (PRIORITY)
   - backend/app/services/extract.py: 58%

backend/app/routers/action_items.py: 65% coverage
Missing coverage:
- Lines 28-35: Error handling for non-existent item
- Lines 42-45: Bulk complete transaction rollback
- Lines 58-62: Empty description validation

Suggested tests:
1. test_complete_item_not_found
   - Try to complete non-existent item
   - Should return 404

2. test_bulk_complete_with_transaction_rollback
   - Submit mix of valid and invalid IDs
   - Should rollback on any failure

3. test_create_item_empty_description
   - Submit empty description
   - Should return 400

📊 Detailed HTML Report: htmlcov/index.html

Priority Improvements:
1. action_items.py: 65% → 80% (need +15%)
2. extract.py: 58% → 80% (need +22%)

Would you like me to generate tests for action_items.py? (y/n)
```

**When tests fail:**

```
Running: pytest backend/tests/ --cov=backend/app --cov-report=term-missing -v

❌ Tests failed (25 passed, 2 failed)

Failures:
1. test_create_note_empty_title
   File: backend/tests/test_notes.py, line 45
   AssertionError: Expected 400, got 500

2. test_delete_note_not_found
   File: backend/tests/test_notes.py, line 78
   HTTPException not raised

Coverage analysis skipped (fix failing tests first).

Options: (a) Help me debug (b) I'll fix manually (c) Abort
```

---

## Usage Tips

1. **Run before commits:**
   - Add to pre-commit workflow
   - Ensure coverage doesn't drop

2. **Set coverage goals:**
   - New code: >90% coverage
   - Existing code: >80% coverage
   - Critical paths: 100% coverage

3. **Focus on priority files:**
   - Start with lowest coverage
   - Work up to 80% baseline
   - Then improve from there

4. **Use HTML report:**
   - Visual view of uncovered lines
   - Click through files
   - See exactly what's missing

---

## Example Conversation

**User:** "Run test coverage on the notes router"

**Warp AI (using this prompt):**

```bash
pytest backend/tests/test_notes.py --cov=backend/app/routers/notes --cov-report=term-missing -v
```

[Analyzes results]

```
backend/app/routers/notes.py: 85% coverage

Missing coverage:
- Lines 67-70: Archive endpoint error handling

Suggested test:
test_archive_note_already_archived
  - Archive a note twice
  - Second attempt should return 400

Would you like me to generate this test?
```

**User:** "Yes"

**Warp AI:**

[Writes test in backend/tests/test_notes.py]
[Runs test - passes]
[Re-runs coverage]

```
Coverage improved: 85% → 92%

New HTML report available at: htmlcov/index.html
```

---

## Integration with Other Prompts

This prompt works well combined with:

- **Add Endpoint** prompt → Generate endpoint → Run coverage → Fill gaps
- **Refactor** prompt → Refactor code → Run coverage → Ensure no regression
- **Pre-commit hook** → Run coverage → Block commit if below threshold

---

## Customization

To adjust coverage thresholds, modify step 3 categories:

```markdown
- Excellent (≥95%)  # Stricter threshold
- Good (85-94%)
- Needs Work (75-84%)
- Poor (<75%)
```

To change default target:

```markdown
Variables:
- target (optional)
  - Default: `backend/`  # Test entire backend
```

To add automatic test generation (skip asking):

```markdown
6. **Generate tests automatically:**
   - For files below 70% coverage
   - Write 3 tests per file
   - Run and verify
   - Show improvement
```

---

## Version History

- v1.0 (2025-01-15): Initial version with basic coverage analysis
- v1.1 (2025-01-20): Added specific test suggestions
- v1.2 (2025-01-25): Added automatic test generation option
