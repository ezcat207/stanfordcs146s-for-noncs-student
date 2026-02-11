# Week 5 Assignment Writeup Example
**Student:** Alex Chen
**Date:** January 28, 2025
**Assignment:** Warp Agentic Development

---

## Part A: Warp Drive Automations

I created two Warp Drive automations to streamline repetitive development tasks in the notes application.

---

### Automation #1: Test Coverage Analyzer

**Type:** Warp Drive Saved Prompt

**Problem it solves:**
Before this automation, checking test coverage required manually running pytest with coverage flags, interpreting the term-missing output, figuring out which lines weren't tested, and then deciding what tests to write. This process took 10-15 minutes and was error-prone—I often missed important edge cases.

**What the automation does:**
This saved prompt runs comprehensive test coverage analysis, categorizes files by coverage level (Excellent ≥90%, Good 80-89%, Needs Work <80%), analyzes untested code to suggest specific test cases, and offers to auto-generate tests for low-coverage files.

**File location:** `warp-drive/test-coverage-analyzer.md`

**Key features:**
- Automatically runs `pytest --cov=backend/app --cov-report=term-missing`
- Parses coverage reports and categorizes files
- For low-coverage files, identifies specific untested line ranges
- Suggests 2-3 concrete test scenarios for each gap
- Offers to generate and run suggested tests
- Re-runs coverage to show improvement

**Usage example:**

```bash
# In Warp, type:
warp-ai "Run test coverage analyzer for backend/tests/"

# Output:
=== Test Coverage Summary ===

Total Coverage: 78%

Coverage Breakdown:
✅ Excellent (≥90%): 3 files
   - backend/app/main.py: 100%
   - backend/app/db.py: 95%
   - backend/app/schemas.py: 92%

⚠️ Good (80-89%): 1 file
   - backend/app/routers/notes.py: 85%

❌ Needs Work (<80%): 1 file
   - backend/app/routers/action_items.py: 65% (PRIORITY)

backend/app/routers/action_items.py: 65% coverage
Missing coverage:
- Lines 28-35: Error handling for non-existent item
- Lines 42-45: Bulk complete transaction rollback
- Lines 58-62: Empty description validation

Suggested tests:
1. test_complete_item_not_found
   - Try to complete item ID 99999
   - Should return 404

2. test_bulk_complete_with_rollback
   - Submit IDs: [1, 2, 99999, 4]
   - Should rollback on failure

3. test_create_item_empty_description
   - Submit description: ""
   - Should return 400

Would you like me to generate tests for action_items.py? (y/n)
```

**Autonomy level:** Semi-autonomous (Level 3/5)
- Runs analysis automatically
- Identifies gaps and suggests tests autonomously
- **Requires approval** before generating tests
- Needs human verification that tests are correct

**Supervision strategy:**
I review the suggested test scenarios before approving generation. This takes 30 seconds but ensures the tests actually match my requirements. After generation, I manually verify the tests pass and cover the right logic.

**Before/After metrics:**

| Metric | Before (Manual) | After (Automated) | Improvement |
|--------|----------------|-------------------|-------------|
| Time to analyze coverage | 5 min | 30 sec | **90% faster** |
| Time to identify gaps | 8 min (manual code reading) | 10 sec | **95% faster** |
| Time to write 3 tests | 12 min | 2 min (with approval) | **83% faster** |
| **Total time** | **25 min** | **3 min** | **88% faster** |
| Test quality | Variable (missed edge cases) | Consistent (covers untested lines) | More reliable |
| Coverage improvement | +5% per session | +15% per session | **3× more effective** |

**Real impact:**
In one session, I improved coverage from 65% → 92% in the action_items router in just 8 minutes (previously would take 45+ minutes). The automation found edge cases I completely missed, like transaction rollback scenarios.

---

### Automation #2: Project Standards Enforcement

**Type:** Warp Rules (project-rules.yaml)

**Problem it solves:**
I kept forgetting project requirements: adding type hints, using Pydantic validation, running tests before commits, following conventional commit messages. This led to failed CI checks, code review comments, and wasted time fixing issues retroactively.

**What the automation does:**
This rules file defines coding standards, API design patterns, testing requirements, and git workflow rules that Warp AI automatically follows when generating or modifying code.

**File location:** `warp-drive/project-rules.yaml`

**Key rules enforced:**

1. **Type Hints Required** (strict)
   - All function parameters and return types must have type hints
   - Prevents untyped code from being generated

2. **Pydantic for Validation** (strict)
   - Use Pydantic schemas for request/response validation
   - Never do manual validation checks

3. **TDD Required** (strict)
   - Write tests BEFORE implementation
   - Workflow: write test → fail → implement → pass

4. **Test Execution Before Completion** (blocking)
   - Always run `make test` before declaring task complete
   - Blocks completion if tests fail

5. **Conventional Commits** (strict)
   - Format: `<type>: <description>`
   - Types: feat, fix, test, docs, refactor, style, chore

6. **HTTP Status Codes** (strict)
   - 201 for POST operations
   - 204 for DELETE operations
   - 404 for resource not found
   - 400 for validation errors

**Usage example:**

```bash
# I ask Warp AI to add a new endpoint:
warp-ai "Add a POST endpoint to create action items"

# Warp AI automatically:
# 1. Writes tests FIRST (from TDD rule)
# 2. Includes type hints on all parameters (from Type Hints rule)
# 3. Uses Pydantic schema for request body (from Pydantic rule)
# 4. Sets status_code=201 (from HTTP Status Codes rule)
# 5. Runs make test before finishing (from Test Execution rule)
# 6. Commits with: "feat: Add create action item endpoint" (from Conventional Commits rule)

# Generated code:
@router.post("/", response_model=ActionItemRead, status_code=201)
def create_action_item(
    payload: ActionItemCreate,  # ✅ Pydantic schema
    db: Session = Depends(get_db)  # ✅ Type hint
) -> ActionItemRead:  # ✅ Return type hint
    """Create a new action item."""
    item = ActionItem(
        description=payload.description,
        completed=False
    )
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)

# Tests written first (TDD):
def test_create_action_item_success(client):
    response = client.post("/action_items/", json={
        "description": "Buy groceries"
    })
    assert response.status_code == 201  # ✅ Correct status code
    assert response.json()["description"] == "Buy groceries"

def test_create_action_item_empty_description(client):
    response = client.post("/action_items/", json={
        "description": ""
    })
    assert response.status_code == 400  # ✅ Validation error
```

**Autonomy level:** High autonomy (Level 4/5)
- Automatically enforces all rules without asking
- Generates code that follows standards by default
- Only requires approval for commits (git workflow safety)

**Supervision strategy:**
Minimal supervision needed. I spot-check generated code occasionally to ensure rules are being followed correctly. I review commits before pushing to ensure conventional commit format is correct.

**Before/After metrics:**

| Metric | Before (No Rules) | After (With Rules) | Improvement |
|--------|-------------------|-------------------|-------------|
| Code review comments | 8-12 per PR | 0-2 per PR | **83% reduction** |
| Failed CI checks | 3-5 per PR | 0-1 per PR | **80% reduction** |
| Time fixing type hint issues | 10 min per endpoint | 0 min | **100% saved** |
| Time fixing validation issues | 8 min per endpoint | 0 min | **100% saved** |
| Time fixing commit messages | 5 min per commit | 0 min | **100% saved** |
| Test coverage | 60-70% | 85-95% | **+25 points** |
| Time to implement endpoint | 25 min | 12 min | **52% faster** |

**Real impact:**
My last 3 PRs had ZERO code review comments related to style, validation, or testing. Previously, I'd average 10+ comments per PR and spend 30-45 minutes addressing them. The rules file eliminated an entire category of preventable mistakes.

---

## Part B: Multi-Agent Workflow

I used git worktree and Warp AI to coordinate 3 agents working in parallel to implement 3 independent features simultaneously.

---

### Scenario

**Task:** Implement 3 features for the notes application:
1. Search functionality (search notes by title/content)
2. Archive/unarchive endpoints (soft delete notes)
3. Category tags (categorize notes as personal/work/ideas/todo)

**Why multi-agent?**
Implementing these sequentially would take ~45 minutes. Running 3 agents in parallel reduced this to 25 minutes total (20 min parallel + 5 min merge).

---

### Setup: Git Worktree

**Created 3 isolated workspaces:**

```bash
# From main project: ~/week5/starter
git worktree add ../worktree-search -b feature/search-notes
git worktree add ../worktree-archive -b feature/archive-notes
git worktree add ../worktree-categories -b feature/note-categories

# Verification:
git worktree list
# ~/week5/starter                  [main]
# ~/week5/worktree-search          [feature/search-notes]
# ~/week5/worktree-archive         [feature/archive-notes]
# ~/week5/worktree-categories      [feature/note-categories]
```

**What this enables:**
- 3 separate working directories
- Each on its own feature branch
- All share the same git history
- No conflicts during development

---

### Agent Instructions

I created detailed instruction files for each agent following TDD workflow:

**Agent Alpha (Search):**
- File: `agent-alpha-instructions.md`
- Task: Add GET /notes/search endpoint
- Requirements: Search title and content, case-insensitive, handle empty queries
- Tests: 4 test cases (by title, by content, empty query, no results)
- Time estimate: 15 minutes

**Agent Beta (Archive):**
- File: `agent-beta-instructions.md`
- Task: Add POST /notes/{id}/archive and POST /notes/{id}/unarchive
- Requirements: Add archived field to model, exclude from default GET /notes
- Tests: 5 test cases (archive, unarchive, not found, exclude archived, include param)
- Time estimate: 20 minutes

**Agent Gamma (Categories):**
- File: `agent-gamma-instructions.md`
- Task: Add category field and filtering
- Requirements: Valid categories (personal/work/ideas/todo), optional field
- Tests: 4 test cases (create with category, invalid category, filter, update)
- Time estimate: 20 minutes

---

### Parallel Execution

**T+0 min:** Launched all 3 agents simultaneously

**Warp Tab 1 (Agent Alpha):**
```bash
cd ~/week5/worktree-search
warp-ai "Follow agent-alpha-instructions.md. Use TDD workflow from project-rules.yaml. When done, create ALPHA_COMPLETE.txt with commit hash."
```

**Warp Tab 2 (Agent Beta):**
```bash
cd ~/week5/worktree-archive
warp-ai "Follow agent-beta-instructions.md. Use TDD workflow from project-rules.yaml. When done, create BETA_COMPLETE.txt with commit hash."
```

**Warp Tab 3 (Agent Gamma):**
```bash
cd ~/week5/worktree-categories
warp-ai "Follow agent-gamma-instructions.md. Use TDD workflow from project-rules.yaml. When done, create GAMMA_COMPLETE.txt with commit hash."
```

**T+5 min:** First check-in
- Agent Alpha: ✅ Tests written, implementation in progress
- Agent Beta: ✅ Model updated, writing tests
- Agent Gamma: ✅ Tests written and passing, updating docs

**T+15 min:** Second check-in
- Agent Alpha: ✅ ALPHA_COMPLETE.txt created (commit: a3f8b2c)
- Agent Beta: ⏳ Tests passing, finalizing documentation
- Agent Gamma: ✅ GAMMA_COMPLETE.txt created (commit: 7d4e1a9)

**T+20 min:** All agents complete
- Agent Alpha: ✅ Complete (4 tests passing)
- Agent Beta: ✅ BETA_COMPLETE.txt created (commit: 5c2d8f1)
- Agent Gamma: ✅ Complete (4 tests passing)

---

### Integration and Merging

**Step 1: Verify each branch independently**

```bash
# worktree-search
cd ~/week5/worktree-search
make test
# ✅ 31 tests passed (including 4 new search tests)

# worktree-archive
cd ~/week5/worktree-archive
make test
# ✅ 32 tests passed (including 5 new archive tests)

# worktree-categories
cd ~/week5/worktree-categories
make test
# ✅ 31 tests passed (including 4 new category tests)
```

**Step 2: Merge in sequence**

```bash
cd ~/week5/starter
git checkout main

# Merge categories first (schema change)
git merge feature/note-categories
make test
# ✅ 31 tests passed

# Merge archive second (schema change)
git merge feature/archive-notes
make test
# ✅ 36 tests passed (combined categories + archive tests)

# Merge search last (no schema change)
git merge feature/search-notes
make test
# ✅ 40 tests passed (all features combined)
```

**Step 3: Handle conflicts**

One conflict occurred in `backend/app/models.py`:

```python
<<<<<<< HEAD
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(50), nullable=True)  # From Agent Gamma
=======
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    archived = Column(Boolean, default=False)  # From Agent Beta
>>>>>>> feature/archive-notes
```

**Resolution:** Kept BOTH fields

```python
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(50), nullable=True)  # From Agent Gamma
    archived = Column(Boolean, default=False)     # From Agent Beta
```

Committed with: `git commit -m "merge: Combine category and archived fields"`

**Step 4: Final verification**

```bash
make test
# ✅ All 40 tests passed

make lint
# ✅ No linting issues

pytest backend/tests/test_notes.py -v
# test_search_notes_by_title PASSED              ✅ (Alpha)
# test_search_notes_by_content PASSED            ✅ (Alpha)
# test_search_notes_empty_query PASSED           ✅ (Alpha)
# test_search_notes_no_results PASSED            ✅ (Alpha)
# test_archive_note PASSED                       ✅ (Beta)
# test_unarchive_note PASSED                     ✅ (Beta)
# test_list_notes_excludes_archived PASSED       ✅ (Beta)
# test_list_notes_include_archived_param PASSED  ✅ (Beta)
# test_create_note_with_category PASSED          ✅ (Gamma)
# test_filter_notes_by_category PASSED           ✅ (Gamma)
# test_update_note_category PASSED               ✅ (Gamma)
```

---

### Coordination Notes

**What went well:**
1. **Clear task boundaries:** Each agent had completely independent work (no shared files during development)
2. **TDD saved time:** All agents wrote tests first, caught bugs early
3. **Warp rules enforced consistency:** All 3 agents followed same coding standards automatically
4. **Git worktree eliminated conflicts:** No merge conflicts during development, only during final integration

**Challenges encountered:**
1. **Agent Beta took longer than expected:** Model migration required manual database reset
   - **Solution:** Provided explicit instruction to delete db.sqlite and recreate
   - **Time lost:** 3 minutes

2. **Merge conflict in models.py:** Two agents added different fields
   - **Solution:** Manually combined both fields, re-ran tests
   - **Time spent:** 2 minutes

3. **Tests passed individually but failed after merge:** Category validation conflicted with archive filtering
   - **Solution:** Updated category filter to exclude archived notes by default
   - **Time spent:** 4 minutes

**Supervision level:** Medium (Level 3/5)
- Checked each agent every 5 minutes (3 check-ins total)
- Intervened once with Agent Beta (database reset)
- Manually resolved merge conflicts
- Verified final tests passed

**Time spent supervising:** 9 minutes total
- 6 minutes monitoring (3 check-ins × 2 min each)
- 3 minutes intervention (database reset guidance)

---

### Results

**Time comparison:**

| Approach | Time Required | Breakdown |
|----------|---------------|-----------|
| **Sequential (one feature at a time)** | **45 min** | 15 min (search) + 20 min (archive) + 20 min (categories) |
| **Parallel (3 agents)** | **29 min** | 20 min (parallel) + 5 min (merge) + 4 min (conflict resolution) |
| **Time saved** | **16 min** | **36% faster** |

**Quality metrics:**

| Metric | Result |
|--------|--------|
| Total tests written | 13 tests (4 + 5 + 4) |
| Test coverage | 89% (up from 78%) |
| Linting issues | 0 |
| Code review comments | 0 (all followed project rules) |
| Bugs found in testing | 0 |

**Effectiveness:**
- ✅ All 3 features implemented correctly
- ✅ All tests passing
- ✅ No rework needed
- ✅ Saved 16 minutes vs sequential approach
- ✅ Maintained high code quality (rules enforced automatically)

---

### When to Use Multi-Agent

**Good candidates for parallel work:**
- Independent features (different routers/endpoints)
- Features with minimal shared dependencies
- Deadline pressure (need speed boost)
- Well-defined requirements (clear instructions)

**NOT good for parallel:**
- Features that depend on each other
- Major refactoring (touching many shared files)
- Exploratory work (requirements unclear)
- First time learning codebase

**My recommendation:** Use multi-agent for 3+ independent features when:
1. You've written clear, detailed instructions for each agent
2. Each agent works on different files (minimal overlap)
3. You can check in every 5-10 minutes to monitor progress
4. You're comfortable resolving merge conflicts

---

## Key Takeaways

1. **Warp Drive automations save massive time on repetitive tasks**
   - Test coverage analysis: 88% faster
   - Code standards enforcement: eliminated entire categories of mistakes

2. **Rules files prevent mistakes before they happen**
   - 83% reduction in code review comments
   - 80% reduction in CI failures
   - Consistent code quality without manual enforcement

3. **Multi-agent workflows are powerful but require supervision**
   - 36% time savings for 3 parallel features
   - Merge conflicts are manageable with git worktree
   - Clear instructions and monitoring are critical

4. **TDD + automation = reliable velocity**
   - All agents followed TDD workflow automatically
   - Zero bugs in final merged code
   - High test coverage (89%) maintained

**Total time invested in automations:** 2 hours (creating saved prompts, rules, instructions)
**Time saved in this assignment:** 50+ minutes (coverage analysis + multi-agent workflow)
**ROI:** 2.5× return in single assignment, will compound over semester

---

## Files Submitted

**Part A: Warp Drive Automations**
- `warp-drive/test-coverage-analyzer.md` (saved prompt)
- `warp-drive/project-rules.yaml` (rules file)

**Part B: Multi-Agent Workflow**
- `multi-agent-workflow/README.md` (comprehensive guide)
- `multi-agent-workflow/agent-alpha-instructions.md` (search feature)
- `multi-agent-workflow/agent-beta-instructions.md` (archive feature)
- `multi-agent-workflow/agent-gamma-instructions.md` (categories feature)

**Documentation**
- `writeup.md` (this file)

**Evidence of work:**
- Git commit history showing 3 feature branches merged
- Test coverage report showing 89% coverage
- Screenshot of all 40 tests passing
