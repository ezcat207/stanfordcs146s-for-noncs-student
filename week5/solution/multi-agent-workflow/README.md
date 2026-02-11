# Multi-Agent Workflow Example

## Overview

This example demonstrates how to use git worktree with Warp AI to coordinate 3 agents working in parallel on different features for the notes application.

**Scenario:** We need to implement 3 independent features simultaneously:
1. **Agent Alpha**: Add search functionality to notes
2. **Agent Beta**: Add archive/unarchive endpoints
3. **Agent Gamma**: Add note categories/tags

**Why multi-agent?** Instead of waiting 15 minutes for 3 sequential features, we complete all 3 in ~5 minutes by running agents in parallel.

---

## Setup: Git Worktree Workspace

### Step 1: Create Worktrees

From your main project directory (`~/week5/starter`):

```bash
# Agent Alpha workspace (search feature)
git worktree add ../worktree-search -b feature/search-notes

# Agent Beta workspace (archive feature)
git worktree add ../worktree-archive -b feature/archive-notes

# Agent Gamma workspace (categories feature)
git worktree add ../worktree-categories -b feature/note-categories
```

**What this does:**
- Creates 3 separate working directories
- Each has its own branch
- All share the same git history
- Changes in one worktree don't affect others

### Step 2: Open 3 Warp Windows

Open Warp and create 3 terminal tabs:

**Tab 1: Agent Alpha**
```bash
cd ~/week5/worktree-search
pwd  # Verify: /Users/you/week5/worktree-search
git branch  # Verify: feature/search-notes
```

**Tab 2: Agent Beta**
```bash
cd ~/week5/worktree-archive
pwd  # Verify: /Users/you/week5/worktree-archive
git branch  # Verify: feature/archive-notes
```

**Tab 3: Agent Gamma**
```bash
cd ~/week5/worktree-categories
pwd  # Verify: /Users/you/week5/worktree-categories
git branch  # Verify: feature/note-categories
```

---

## Agent Instructions

### Agent Alpha: Search Functionality

**File:** `agent-alpha-instructions.md`

```markdown
# Agent Alpha: Add Note Search Endpoint

## Task
Implement a search endpoint that allows searching notes by title or content.

## Requirements
1. Endpoint: GET /notes/search?query={search_term}
2. Search both title and content fields (case-insensitive)
3. Return list of matching notes
4. Empty query returns 400 error

## TDD Workflow
1. Write tests in backend/tests/test_notes.py:
   - test_search_notes_by_title
   - test_search_notes_by_content
   - test_search_notes_empty_query
   - test_search_notes_no_results

2. Implement in backend/app/routers/notes.py

3. Run: make format && make lint && make test

4. Update docs/API.md with new endpoint

## Time Estimate
15 minutes

## When Complete
1. Commit with: git commit -m "feat: Add search endpoint for notes"
2. DO NOT PUSH YET - wait for coordination
3. Create file: ALPHA_COMPLETE.txt with commit hash
```

### Agent Beta: Archive Functionality

**File:** `agent-beta-instructions.md`

```markdown
# Agent Beta: Add Archive/Unarchive Endpoints

## Task
Implement archive and unarchive functionality for notes.

## Requirements
1. Add `archived` boolean field to Note model (default: False)
2. Endpoint: POST /notes/{id}/archive
3. Endpoint: POST /notes/{id}/unarchive
4. GET /notes should exclude archived notes by default
5. GET /notes?include_archived=true shows all notes

## TDD Workflow
1. Add migration for new field (if using Alembic) OR update models.py

2. Write tests in backend/tests/test_notes.py:
   - test_archive_note
   - test_unarchive_note
   - test_archive_note_not_found
   - test_list_notes_excludes_archived
   - test_list_notes_include_archived_param

3. Implement in backend/app/routers/notes.py

4. Run: make format && make lint && make test

5. Update docs/API.md

## Time Estimate
20 minutes

## When Complete
1. Commit with: git commit -m "feat: Add archive/unarchive for notes"
2. DO NOT PUSH YET - wait for coordination
3. Create file: BETA_COMPLETE.txt with commit hash
```

### Agent Gamma: Categories/Tags

**File:** `agent-gamma-instructions.md`

```markdown
# Agent Gamma: Add Note Categories

## Task
Implement category/tag functionality for notes.

## Requirements
1. Add `category` string field to Note model (optional, max 50 chars)
2. Valid categories: "personal", "work", "ideas", "todo"
3. Endpoint: GET /notes?category={category_name} (filter by category)
4. Update POST /notes to accept optional category
5. Update PUT /notes/{id} to allow changing category

## TDD Workflow
1. Update models.py with new field

2. Write tests in backend/tests/test_notes.py:
   - test_create_note_with_category
   - test_create_note_invalid_category
   - test_filter_notes_by_category
   - test_update_note_category

3. Update schemas.py (NoteCreate, NoteUpdate)

4. Implement in backend/app/routers/notes.py

5. Run: make format && make lint && make test

6. Update docs/API.md

## Time Estimate
20 minutes

## When Complete
1. Commit with: git commit -m "feat: Add categories for notes"
2. DO NOT PUSH YET - wait for coordination
3. Create file: GAMMA_COMPLETE.txt with commit hash
```

---

## Parallel Execution Timeline

### T+0 Minutes: Launch All Agents

**In Warp Tab 1 (Agent Alpha):**
```bash
# Give Warp AI the task
warp ask "Follow the instructions in agent-alpha-instructions.md.
Use TDD workflow from project-rules.yaml. When done, create ALPHA_COMPLETE.txt"
```

**In Warp Tab 2 (Agent Beta):**
```bash
warp ask "Follow the instructions in agent-beta-instructions.md.
Use TDD workflow from project-rules.yaml. When done, create BETA_COMPLETE.txt"
```

**In Warp Tab 3 (Agent Gamma):**
```bash
warp ask "Follow the instructions in agent-gamma-instructions.md.
Use TDD workflow from project-rules.yaml. When done, create GAMMA_COMPLETE.txt"
```

**What happens now:**
- All 3 agents start working simultaneously
- Each agent works in isolated worktree (no conflicts)
- Each follows TDD: tests → implementation → validation

### T+5 Minutes: Monitor Progress

Check each tab periodically:

```bash
# In each worktree, check status
ls *.txt  # Look for ALPHA_COMPLETE.txt, etc.
git status  # See what's been changed
git log -1  # See latest commit
```

**Signs of problems:**
- Test failures that agent can't resolve → intervene manually
- Agent stuck in loop → provide clarification
- Agent finished but no completion file → verify commit exists

### T+15-20 Minutes: All Agents Complete

You should see:
- ✅ ALPHA_COMPLETE.txt in worktree-search/
- ✅ BETA_COMPLETE.txt in worktree-archive/
- ✅ GAMMA_COMPLETE.txt in worktree-categories/

---

## Integration: Merging the Work

### Step 1: Verify Each Branch Independently

**In each worktree, run full test suite:**

```bash
# worktree-search
cd ~/week5/worktree-search
make test  # Should pass with new search tests

# worktree-archive
cd ~/week5/worktree-archive
make test  # Should pass with new archive tests

# worktree-categories
cd ~/week5/worktree-categories
make test  # Should pass with new category tests
```

**Critical checkpoint:** All tests must pass independently before merging.

### Step 2: Return to Main Directory

```bash
cd ~/week5/starter
git checkout main
```

### Step 3: Merge in Sequence

**Merge order matters:** Models → Features

```bash
# 1. Merge categories first (adds model field)
git merge feature/note-categories
make test  # Verify tests still pass

# 2. Merge archive second (adds another model field)
git merge feature/archive-notes
make test  # Verify tests still pass

# 3. Merge search last (only adds endpoint, no schema changes)
git merge feature/search-notes
make test  # Final verification
```

**Why this order?**
- Schema changes (model fields) merged first
- Feature-only changes merged last
- Minimizes merge conflicts

### Step 4: Handle Conflicts (If Any)

**Common conflict locations:**
- `backend/app/models.py` (multiple agents adding fields)
- `backend/app/schemas.py` (multiple agents updating schemas)
- `backend/tests/test_notes.py` (multiple agents adding tests)

**Resolution strategy:**
```bash
# If conflict occurs during merge:
git status  # See conflicted files

# Edit conflicted files - keep BOTH changes
# For models.py: include archived field AND category field
# For tests: include ALL new test functions

git add <resolved-files>
git commit -m "Merge feature/archive-notes (resolved conflicts)"

# Continue with remaining merges
```

### Step 5: Final Verification

```bash
# Run complete test suite
make test

# Run linting
make lint

# Check code formatting
make format

# Verify all 3 features work
pytest backend/tests/test_notes.py -v
```

**Expected output:**
```
test_search_notes_by_title PASSED              ✅ (Alpha)
test_search_notes_by_content PASSED            ✅ (Alpha)
test_archive_note PASSED                       ✅ (Beta)
test_unarchive_note PASSED                     ✅ (Beta)
test_create_note_with_category PASSED          ✅ (Gamma)
test_filter_notes_by_category PASSED           ✅ (Gamma)

Total: 27 tests passed
```

---

## Cleanup: Remove Worktrees

After successful merge:

```bash
cd ~/week5/starter

# Remove worktrees
git worktree remove ../worktree-search
git worktree remove ../worktree-archive
git worktree remove ../worktree-categories

# Delete merged branches (optional)
git branch -d feature/search-notes
git branch -d feature/archive-notes
git branch -d feature/note-categories

# Verify cleanup
git worktree list  # Should only show main directory
```

---

## Troubleshooting

### Problem: Agent Not Responding

**Symptoms:** Warp AI hasn't shown progress after 2 minutes

**Solution:**
1. Check if agent is waiting for confirmation
2. Look for prompts like "Should I proceed? (y/n)"
3. Provide explicit permission: "Yes, continue with all steps"

### Problem: Test Failures During Development

**Symptoms:** Agent reports test failures and stops

**Options:**
1. **Let agent debug:** "Analyze the failure and fix it"
2. **Manual intervention:** Review the error, fix the code yourself
3. **Restart with clearer instructions:** Provide more specific requirements

### Problem: Merge Conflicts

**Symptoms:** Git reports conflicts during merge

**Solution:**
```bash
# See what's conflicted
git status

# For models.py conflicts - example:
<<<<<<< HEAD
class Note(Base):
    archived = Column(Boolean, default=False)
=======
class Note(Base):
    category = Column(String(50), nullable=True)
>>>>>>> feature/note-categories

# Fix: Keep BOTH
class Note(Base):
    archived = Column(Boolean, default=False)
    category = Column(String(50), nullable=True)

# Mark as resolved
git add backend/app/models.py
git commit -m "Merge: combine model changes"
```

### Problem: Tests Pass Individually, Fail After Merge

**Symptoms:** Each branch's tests pass, but merged tests fail

**Likely causes:**
1. **Database state pollution:** Tests sharing data
2. **Schema conflicts:** Two fields with same name
3. **Conflicting validation rules:** One agent's validator breaks another's feature

**Solution:**
```bash
# Re-run tests with verbose output
pytest backend/tests/test_notes.py -v -s

# Check for fixture issues
# Verify test isolation (each test uses fresh database)

# If schema conflict:
# Manually review backend/app/models.py
# Ensure no duplicate field names
```

---

## Supervision Strategies

### High Supervision (Recommended for First Attempt)

**What to watch:**
- Check each agent every 3-5 minutes
- Review commits before approving merges
- Run tests manually after each merge

**Time cost:** +10 minutes supervision overhead
**Benefit:** Catch issues early, learn the workflow

### Medium Supervision

**What to watch:**
- Check agents only when completion files appear
- Review final commits (not intermediate ones)
- Run tests after all merges complete

**Time cost:** +5 minutes supervision overhead
**Benefit:** Balance between speed and safety

### Low Supervision (Advanced)

**What to watch:**
- Only intervene if agent reports blocking error
- Trust TDD workflow to catch issues
- Review final merged result only

**Time cost:** +2 minutes supervision overhead
**Risk:** May need to debug complex merge conflicts

---

## Success Metrics

**Time Savings:**
- Sequential: 3 features × 15 min = 45 minutes
- Parallel: Max(15, 20, 20) = 20 minutes + 5 min merge = 25 minutes
- **Savings: 20 minutes (44% faster)**

**Quality Maintained:**
- All features have ≥3 test cases
- Code formatting and linting pass
- No test failures in final merge

**When to Use Multi-Agent:**
- 3+ independent features needed
- Features touch different files/routers
- Deadline pressure (need speed)

**When NOT to Use:**
- Features have shared dependencies
- Major refactoring required
- First time learning the codebase

---

## Next Steps

1. **Try the workflow:** Follow this guide with your notes app
2. **Experiment with supervision levels:** Start high, reduce as you gain confidence
3. **Document your results:** Track time savings and issues encountered
4. **Expand to more agents:** Try 4-5 parallel agents for larger projects

**Remember:** The goal isn't just speed—it's learning how to coordinate AI agents effectively. Focus on understanding the workflow before optimizing for speed.
