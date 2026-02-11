# Assignment Bridge: From Lecture to Warp Automations

**Purpose:** Connect Warp concepts to your actual assignment tasks.

**Target Audience:** 18-year-olds with no CS background who might be overwhelmed by multi-agent workflows.

---

## Don't Panic: This Builds on Week 4

"I know what you're thinking: 'Week 4 was about automations in Claude Code, now Week 5 is about Warp... do I have to learn everything from scratch?'

**Good news:** The concepts are the same. You're just using a different tool.

**Week 4 → Week 5 Translation:**

| Week 4 (Claude Code) | Week 5 (Warp) | Same Concept |
|---------------------|---------------|--------------|
| Slash commands | Warp Drive saved prompts | Reusable workflows |
| CLAUDE.md | Warp Rules | Always-active context |
| SubAgents | Multi-tab AI agents | Specialized roles |
| MCP servers | MCP servers in Warp | External tools |

**The difference:** Week 5 adds **parallel execution**—multiple agents working simultaneously.

**Think of it like:**
- Week 4: One chef cooking a 4-course meal (2 hours)
- Week 5: Four chefs cooking simultaneously (30 minutes)

Same meal, different approach."

---

## Understanding the Assignment Structure

### Two Required Parts

**Part A: Warp Drive Automation (at least 1)**
- Create saved prompts, rules, or MCP integrations
- Like slash commands from Week 4, but in Warp
- **Goal:** Build reusable automations

**Part B: Multi-Agent Workflow (at least 1)**
- Spawn multiple AI agents in parallel
- Each agent works on a different task
- **Goal:** Experience parallel development

**You need at least one from each category.**

**Recommended approach:**
1. Start with Part A (easier, builds on Week 4 knowledge)
2. Then try Part B (more advanced, requires git worktree)

---

## Step-by-Step: Part A (Warp Drive Automations)

### Step 0: Install and Set Up Warp (15 minutes)

**If you haven't already:**

1. **Download Warp:** https://www.warp.dev/
2. **Install and open Warp**
3. **Sign in** (required for Warp Drive features)
4. **Enable AI features** in Settings → AI

**Test it works:**
```bash
# In Warp, type:
cd /path/to/week5
make test

# You should see test output
```

If this works, you're ready.

### Step 1: Choose What to Automate (15 minutes)

"Look at `docs/TASKS.md` in week5. These are the features you could implement.

**Pick tasks that are:**
- ✅ Repetitive (you'll do multiple times)
- ✅ Well-defined (clear inputs/outputs)
- ✅ Suitable for automation

**Good candidates for Warp Drive automation:**

**Easy:**
- Task 10: Test coverage improvements
  - **Automation:** Saved prompt that runs tests, analyzes coverage, suggests improvements
- Task 8: List endpoint pagination
  - **Automation:** Saved prompt that adds pagination to any endpoint

**Medium:**
- Task 2: Notes search with pagination
  - **Automation:** Saved prompt for adding search + pagination to any resource
- Task 7: Robust error handling
  - **Automation:** Rule that enforces error handling patterns

**Hard:**
- Task 1: Migrate to Vite + React
  - **Automation:** Multi-step workflow for framework migration
- Task 5: Tags with many-to-many
  - **Automation:** Saved prompt for adding many-to-many relationships

**My recommendation:** Start with Task 10 (test coverage) or Task 8 (pagination). These are well-scoped and useful."

### Step 2: Create Your First Warp Drive Saved Prompt (30 minutes)

"Let's create a saved prompt for test coverage analysis.

#### Step 2a: Open Warp Drive

In Warp:
1. Press `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux)
2. Type "Warp Drive"
3. Select "Create New Prompt"

#### Step 2b: Define the Prompt

**Name:** Test Coverage Analyzer

**Description:** Runs pytest with coverage and provides actionable insights

**Prompt text:**
```markdown
Run pytest with coverage analysis for {target}.

Steps:
1. Execute: pytest {target} --cov=backend/app --cov-report=term-missing --cov-report=html -v

2. If tests fail:
   - Show the failing test output
   - Stop and ask: "Tests failed. Debug or abort?"

3. If tests pass:
   - Parse coverage results
   - Categorize files:
     * Excellent (≥90%): List files
     * Good (80-89%): List files
     * Needs work (<80%): List files with missing line numbers

4. For each file below 80%:
   - Show current percentage
   - List specific untested line numbers
   - Suggest concrete test scenarios

5. Generate summary:
   ```
   Total Coverage: X%

   Priority improvements:
   1. [File]: X% → target 80% (need +Y%)
      Suggested tests:
      - test_scenario_1
      - test_scenario_2
   ```

6. Provide HTML report location: htmlcov/index.html

7. Ask: "Would you like me to generate tests for the lowest coverage file?"

Variables:
- target: Test file or directory (default: backend/tests/)

Rules to follow:
- Never modify application code
- Never commit automatically
- Show specific, actionable recommendations
```

**Arguments:**
- `target` (optional): `backend/tests/` (default)

#### Step 2c: Save and Test

1. Click "Save Prompt"
2. Test it:
   - Press `Cmd+P` → Search for "Test Coverage Analyzer"
   - Run it with default arguments
   - Verify it works

**Expected output:**
```
Running: pytest backend/tests/ --cov=backend/app --cov-report=term-missing -v

✅ All tests passed (15/15)

Coverage Analysis:
✅ Excellent (≥90%):
   - backend/app/main.py: 100%
   - backend/app/db.py: 95%

⚠️ Needs work (<80%):
   - backend/app/routers/action_items.py: 65%
     Missing: Lines 28-35, 42-45
     Suggested tests:
     - test_complete_item_already_completed
     - test_bulk_complete_with_invalid_ids

Total Coverage: 78%

HTML report: htmlcov/index.html

Would you like me to generate tests for action_items.py?
```

If you see this, ✅ you've created your first Warp automation!

### Step 3: Create a Warp Rule (20 minutes)

"Rules are like CLAUDE.md but for Warp—always active.

#### Step 3a: Create the Rule

In Warp:
1. Open Settings → AI → Rules
2. Click "Add Rule"

**Rule name:** FastAPI Project Standards

**Rule content:**
```yaml
# FastAPI Project Coding Standards

## Code Style
- Always use type hints for all function parameters and return types
- Use Pydantic schemas for request/response validation
- Never use print() for debugging - use proper logging
- Format code with 'make format' before finishing any task

## API Patterns
- Return proper HTTP status codes:
  * 200: Success (GET, PUT, PATCH)
  * 201: Created (POST)
  * 204: No content (DELETE)
  * 400: Validation error
  * 404: Not found
  * 500: Server error (avoid by handling exceptions)
- Always raise HTTPException for errors, never return error strings

## Testing
- Write tests BEFORE implementation (TDD)
- Test files live in backend/tests/
- Every endpoint needs at least 3 tests:
  * Happy path
  * Error case (404 or 400)
  * Edge case
- Run 'make test' before declaring task complete

## Database
- Use SQLAlchemy ORM, never raw SQL
- Use db.flush() + db.refresh() when you need ID immediately
- Use transactions for bulk operations

## Git Workflow
- Never commit without running tests first
- Follow conventional commit format:
  * feat: New feature
  * fix: Bug fix
  * test: Add tests
  * docs: Documentation
- Never commit directly to main - use feature branches

## File Structure
- Routers: backend/app/routers/
- Models: backend/app/models.py
- Schemas: backend/app/schemas.py
- Tests: backend/tests/
- Frontend: frontend/

## When Asked to Add an Endpoint
1. Write tests first in backend/tests/test_<router>.py
2. Run tests (should fail)
3. Implement in backend/app/routers/<router>.py
4. Run tests (should pass)
5. Run make format && make lint
6. Update docs/API.md

## Safety
- Never delete database files without confirmation
- Never skip pre-commit hooks
- Always ask before destructive actions
```

#### Step 3b: Activate the Rule

1. Save the rule
2. Enable it for your project directory

#### Step 3c: Test It

Start a new Warp session:
```
Ask Warp AI: "Add a new endpoint for archiving notes"
```

**Without the rule:**
```
Warp: "Where should I add this? What framework are you using?"
```

**With the rule:**
```
Warp: "I'll add POST /notes/{id}/archive following TDD:
1. First, I'll write tests in backend/tests/test_notes.py
2. Then implement in backend/app/routers/notes.py
3. Use HTTPException for errors, return 200 status code
4. Run make test, make format, make lint
5. Update docs/API.md

Should I proceed?"
```

**See the difference?** The rule provides automatic context."

### Step 4: Document Your Automation (15 minutes)

"In `writeup.md`, document what you built:

```markdown
## Automation #1: Warp Drive Saved Prompt - Test Coverage Analyzer

### Design

**Goal:** Automate test coverage analysis with actionable insights

**Type:** Warp Drive Saved Prompt

**Inputs:**
- target (optional): Test file or directory to analyze

**Outputs:**
- Coverage percentages by file
- Categorized results (excellent/good/needs work)
- Specific untested line numbers
- Concrete test scenario suggestions
- HTML report location
- Offer to generate tests

**Steps:**
[Copy the 7 steps from your prompt]

### Before vs. After

**Before (Manual):**
Time: ~10-15 minutes
1. Run pytest --cov manually
2. Stare at coverage numbers
3. Open htmlcov/index.html
4. Click through each file
5. Manually identify what's missing
6. Try to remember line numbers
7. Come up with test ideas

**After (Automated):**
Time: ~30 seconds
1. Trigger saved prompt
2. Read categorized results
3. See specific recommendations
4. Choose whether to generate tests

**Time saved:** ~14 minutes per coverage check (93% reduction)
**Quality improvement:** Specific suggestions (not just "improve coverage")

### How I Used It

I used this automation to complete Task 10 from TASKS.md:
"Test coverage improvements"

Workflow:
1. Triggered "Test Coverage Analyzer" prompt
2. Saw that action_items.py had 65% coverage
3. Prompt suggested specific test scenarios:
   - test_complete_item_already_completed
   - test_bulk_complete_with_invalid_ids
4. I implemented these tests
5. Re-ran the prompt
6. Coverage increased to 92%

Result: Increased overall test coverage from 78% to 87%
```

---

## Step-by-Step: Part B (Multi-Agent Workflow)

### Step 1: Understand Git Worktree (30 minutes reading + practice)

"Git worktree lets you have multiple branches checked out simultaneously.

#### Why You Need This

**Problem:**
- Agent 1 working on backend/app/routers/notes.py
- Agent 2 working on backend/app/routers/notes.py
- **Conflict!** They overwrite each other's changes

**Solution:**
- Agent 1 works in `week5-backend/` directory (feature/backend branch)
- Agent 2 works in `week5-frontend/` directory (feature/frontend branch)
- No conflict! Different directories

#### How to Use Worktrees

**Step 1a: Create branches**
```bash
cd week5/

git branch feature/task2-backend
git branch feature/task2-frontend
git branch feature/task2-tests
```

**Step 1b: Create worktrees**
```bash
git worktree add ../week5-task2-backend feature/task2-backend
git worktree add ../week5-task2-frontend feature/task2-frontend
git worktree add ../week5-task2-tests feature/task2-tests
```

**Step 1c: Verify**
```bash
ls ../

# You should see:
week5/                    # Original (main branch)
week5-task2-backend/      # Worktree (feature/task2-backend)
week5-task2-frontend/     # Worktree (feature/task2-frontend)
week5-task2-tests/        # Worktree (feature/task2-tests)
```

**Step 1d: Navigate to worktrees**
```bash
# Each is a complete copy of the repo on a different branch
cd ../week5-task2-backend/
git branch  # Shows: feature/task2-backend

cd ../week5-task2-frontend/
git branch  # Shows: feature/task2-frontend
```

**Practice this before using with AI agents!**"

### Step 2: Pick Tasks for Parallel Execution (15 minutes)

"Choose tasks that are **truly independent**—no dependencies between them.

**Good combinations (independent):**

**Option A: Different resources**
- Agent 1: Task 2 (notes search)
- Agent 2: Task 4 (action items filters)
- Agent 3: Task 10 (test coverage for existing code)

**Option B: Same feature, different layers**
- Agent 1: Backend for tags (Task 5)
- Agent 2: Frontend for tags (Task 5)
- Agent 3: Tests for tags (Task 5)

**Bad combinations (dependent):**
- ❌ Agent 1: Add endpoint
- ❌ Agent 2: Add frontend that calls that endpoint
- Problem: Agent 2 depends on Agent 1 finishing first

**My recommendation:** Start with Option A (different resources) for your first multi-agent workflow."

### Step 3: Set Up Multi-Agent Workspace (20 minutes)

"Let's say you picked Tasks 2, 4, and 10.

#### Step 3a: Create worktrees

```bash
cd week5/

# Create branches
git branch feature/task2-search
git branch feature/task4-filters
git branch feature/task10-tests

# Create worktrees
git worktree add ../week5-task2 feature/task2-search
git worktree add ../week5-task4 feature/task4-filters
git worktree add ../week5-task10 feature/task10-tests
```

#### Step 3b: Open 3 Warp tabs

1. **Tab 1:** Search Agent
   ```bash
   cd ../week5-task2/
   ```

2. **Tab 2:** Filters Agent
   ```bash
   cd ../week5-task4/
   ```

3. **Tab 3:** Tests Agent
   ```bash
   cd ../week5-task10/
   ```

#### Step 3c: Verify isolation

In each tab:
```bash
pwd         # Should show different directories
git branch  # Should show different branches
```

If each tab is in a different directory and branch, ✅ you're ready."

### Step 4: Define Agent Roles (15 minutes)

"Write clear instructions for each agent.

**Tab 1 (Search Agent):**
```
You are the Search Agent.

Your ONLY job: Implement Task 2 from docs/TASKS.md
"Notes search with pagination and sorting"

Working directory: week5-task2/
Git branch: feature/task2-search

Tasks:
1. Modify backend/app/routers/notes.py
   - Add GET /notes/search endpoint
   - Parameters: q, page, page_size, sort
   - Use SQLAlchemy for filtering and pagination
   - Return: {items, total, page, page_size}

2. Write tests in backend/tests/test_notes.py
   - test_search_notes_exact_match
   - test_search_notes_partial_match
   - test_search_notes_case_insensitive
   - test_search_pagination
   - test_search_sorting

3. Run make test to verify

4. When done, commit to feature/task2-search:
   "feat: Add notes search with pagination and sorting"

Files you can modify:
- backend/app/routers/notes.py
- backend/app/schemas.py (if needed)
- backend/tests/test_notes.py

Files you CANNOT modify:
- backend/app/routers/action_items.py
- frontend/ (different agent's job)
- Any file not listed above

Start now. Work autonomously. Report back when done or if you encounter blockers.
```

**Tab 2 (Filters Agent):**
```
You are the Filters Agent.

Your ONLY job: Implement Task 4 from docs/TASKS.md
"Action items: filters and bulk complete"

Working directory: week5-task4/
Git branch: feature/task4-filters

Tasks:
1. Modify backend/app/routers/action_items.py
   - Add query param to GET /action-items?completed=true|false
   - Add POST /action-items/bulk-complete
   - Accept list of IDs, mark as completed in transaction

2. Write tests in backend/tests/test_action_items.py
   - test_filter_by_completed
   - test_filter_by_not_completed
   - test_bulk_complete_success
   - test_bulk_complete_partial_failure
   - test_bulk_complete_rollback

3. Run make test

4. Commit to feature/task4-filters:
   "feat: Add action items filtering and bulk complete"

Files you can modify:
- backend/app/routers/action_items.py
- backend/app/schemas.py (if needed)
- backend/tests/test_action_items.py

Files you CANNOT modify:
- backend/app/routers/notes.py (different agent)
- frontend/
- Any file not listed above

Start now. Work autonomously. Report when done or blocked.
```

**Tab 3 (Tests Agent):**
```
You are the Tests Agent.

Your ONLY job: Implement Task 10 from docs/TASKS.md
"Test coverage improvements"

Working directory: week5-task10/
Git branch: feature/task10-tests

Tasks:
1. Run pytest --cov to identify low-coverage areas

2. Add tests for 400/404 scenarios:
   - All notes endpoints
   - All action items endpoints

3. Add edge case tests:
   - Empty results
   - Invalid IDs
   - Validation errors

4. Target: 90%+ coverage for all routers

5. Commit to feature/task10-tests:
   "test: Improve coverage to 90%+ for all routers"

Files you can modify:
- backend/tests/test_notes.py
- backend/tests/test_action_items.py
- backend/tests/conftest.py (fixtures)

Files you CANNOT modify:
- backend/app/ (application code)
- frontend/

Start now. Work autonomously. Report when done or blocked.
```"

### Step 5: Launch Agents and Monitor (30-60 minutes)

"Now the exciting part: launch all agents simultaneously.

#### Step 5a: Start all agents

In each Warp tab, paste the agent instructions and press Enter.

All 3 agents start working **at the same time**.

#### Step 5b: Monitor progress

Switch between tabs every 5-10 minutes:

**Tab 1 (Search Agent):**
```
Creating search endpoint...
Adding pagination logic...
Writing tests...
Running tests...
✓ All tests pass (12/12)
Committing...
Done!
```

**Tab 2 (Filters Agent):**
```
Adding query parameter...
Implementing bulk complete...
Writing tests...
Running tests...
✓ All tests pass (8/8)
Committing...
Done!
```

**Tab 3 (Tests Agent):**
```
Analyzing coverage...
Coverage: 78%
Adding 404 tests...
Adding validation tests...
Running tests...
Coverage: 91% ✓
Committing...
Done!
```

#### Step 5c: Handle issues

If an agent gets stuck:
- **Read the error message**
- **Provide clarification** (don't abandon the workflow)
- **Resume the agent**

If an agent conflicts with another:
- **This shouldn't happen** if you set up worktrees correctly
- **Check:** Are they in different directories?
- **Fix:** Make sure each agent has its own worktree"

### Step 6: Merge Results (15 minutes)

"Once all agents finish:

#### Step 6a: Return to main directory

```bash
cd week5/
```

#### Step 6b: Merge branches one by one

```bash
# Merge search feature
git merge feature/task2-search
# Should merge cleanly (no conflicts)

# Merge filters feature
git merge feature/task4-filters
# Should merge cleanly

# Merge tests
git merge feature/task10-tests
# Should merge cleanly
```

#### Step 6c: Run full test suite

```bash
make test
```

**If all tests pass:** ✅ Success! Your multi-agent workflow worked!

**If tests fail:**
- Read the error
- It's likely an integration issue (agents' code doesn't work together)
- Fix it manually (this is expected sometimes)

#### Step 6d: Clean up worktrees

```bash
# Remove worktrees
git worktree remove ../week5-task2
git worktree remove ../week5-task4
git worktree remove ../week5-task10

# Optionally delete branches
git branch -d feature/task2-search
git branch -d feature/task4-filters
git branch -d feature/task10-tests
```"

### Step 7: Document Your Multi-Agent Workflow (20 minutes)

"In `writeup.md`:

```markdown
## Automation #2: Multi-Agent Parallel Development

### Design

**Goal:** Complete 3 independent tasks simultaneously using parallel agents

**Tasks:**
- Task 2: Notes search with pagination (Search Agent)
- Task 4: Action items filters (Filters Agent)
- Task 10: Test coverage improvements (Tests Agent)

**Setup:**
- Used git worktree to create isolated workspaces
- 3 separate Warp tabs, each with dedicated agent
- Each agent had clear file ownership boundaries

**Agent Roles:**
1. **Search Agent** (Tab 1)
   - Files: routers/notes.py, tests/test_notes.py
   - Branch: feature/task2-search
   - Working dir: ../week5-task2/

2. **Filters Agent** (Tab 2)
   - Files: routers/action_items.py, tests/test_action_items.py
   - Branch: feature/task4-filters
   - Working dir: ../week5-task4/

3. **Tests Agent** (Tab 3)
   - Files: all test files (read-only app code)
   - Branch: feature/task10-tests
   - Working dir: ../week5-task10/

### Coordination Strategy

**Independence:**
- Each agent worked on different files
- No dependencies between tasks
- Minimal risk of conflicts

**Monitoring:**
- Checked each tab every 5-10 minutes
- All agents completed within 45 minutes
- No blockers or conflicts encountered

**Merge:**
- Merged branches sequentially
- Zero merge conflicts (as expected)
- All tests passed after merge

### Before vs. After

**Before (Sequential):**
- Task 2: 60 minutes
- Task 4: 45 minutes
- Task 10: 30 minutes
- **Total: 135 minutes (2.25 hours)**

**After (Parallel with 3 agents):**
- Setup worktrees: 10 minutes
- All agents working: 45 minutes (longest task)
- Merge and verify: 10 minutes
- **Total: 65 minutes**

**Time saved:** 70 minutes (52% reduction)

### Autonomy Levels

**Search Agent:** High autonomy
- Permissions: Modify routers/notes.py, schemas.py, tests
- Supervision: Checked progress every 10 minutes
- Why: Well-defined task, low risk

**Filters Agent:** High autonomy
- Permissions: Modify routers/action_items.py, schemas.py, tests
- Supervision: Checked progress every 10 minutes
- Why: Independent task, clear boundaries

**Tests Agent:** Medium autonomy
- Permissions: Modify test files only (read-only app code)
- Supervision: Checked coverage reports
- Why: Could write too many tests (diminishing returns)

### Risks and Failures

**Risks considered:**
1. Agents modifying the same file → Mitigated with worktrees
2. Integration issues after merge → Mitigated with clear contracts
3. Agent getting stuck → Monitored regularly

**Failures encountered:**
- None during execution
- One minor linting error after merge (fixed in 2 minutes)

**What worked well:**
- Clear role boundaries prevented conflicts
- Worktrees worked perfectly
- Time savings were significant

**What to improve:**
- Could have added a 4th agent for docs updates
- Could have set up continuous integration agent to merge frequently
```"

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Skipping Worktree Setup

**Symptom:** Agents overwrite each other's changes

**Fix:**
- **Always use git worktree** for multi-agent work
- Each agent gets its own directory
- Verify with `git branch` in each tab

### Mistake 2: Vague Agent Instructions

**Bad:**
```
Work on the tags feature
```

**Good:**
```
You are the Backend Agent.
Files you can modify: backend/app/routers/tags.py, backend/app/models.py
Files you CANNOT modify: frontend/, other routers
Task: Add Tag model and CRUD endpoints
When done: Commit to feature/tags-backend
```

**Fix:** Be extremely specific about:
- What files they can touch
- What files they cannot touch
- When they're done
- Where to commit

### Mistake 3: Dependent Tasks in Parallel

**Bad:**
- Agent 1: Add backend endpoint
- Agent 2: Add frontend that calls it
- Problem: Agent 2 depends on Agent 1

**Fix:**
- Only parallelize **independent** tasks
- Or: Define interface contract first, then both agents work from that

### Mistake 4: Not Monitoring Agents

**Symptom:** Agent gets stuck for 30 minutes, you don't notice

**Fix:**
- Set a timer: check every 5-10 minutes
- Look for:
  - Agent hasn't made progress
  - Agent asking questions (means stuck)
  - Error messages

### Mistake 5: Forgetting to Document Autonomy Levels

**In writeup.md, you must explain:**
- What permissions each agent had
- How you supervised them
- Why you chose that level of autonomy

**Example:**
```markdown
### Autonomy Levels

Backend Agent: High autonomy
- Permissions: Full write access to backend/app/routers/
- Supervision: Checked every 10 minutes
- Why: Clear task boundaries, low risk of breaking things

Test Agent: Medium autonomy
- Permissions: Write to backend/tests/ only
- Supervision: Reviewed test quality after completion
- Why: Could write too many redundant tests
```

---

## Timeline: How to Finish in 4-5 Hours

**Part A: Warp Drive Automation (2 hours)**
- Hour 1: Create saved prompt for test coverage
- Hour 2: Create Warp rule for project standards
- Document both in writeup.md

**Part B: Multi-Agent Workflow (2.5 hours)**
- 30 min: Learn and practice git worktree
- 30 min: Set up worktrees for 2-3 tasks
- 45 min: Run agents in parallel
- 15 min: Merge results
- 30 min: Document workflow in writeup.md

**Buffer:** 30 minutes for debugging

**Total: 5 hours**

---

## Self-Check Before Submitting

### Part A Checklist

- [ ] I created at least one Warp Drive saved prompt
- [ ] The prompt has clear steps and expected outputs
- [ ] I tested the prompt and it works
- [ ] I documented it in writeup.md with before/after comparison
- [ ] (Optional) I created a Warp rule for project standards

### Part B Checklist

- [ ] I completed at least one multi-agent workflow
- [ ] I used git worktree to isolate agents
- [ ] Each agent had clear role boundaries
- [ ] I documented coordination strategy
- [ ] I explained autonomy levels and supervision
- [ ] I measured time savings (before/after)
- [ ] I documented risks and how I mitigated them

### Documentation Checklist

- [ ] writeup.md has zero TODOs
- [ ] Each automation has design, before/after, and usage sections
- [ ] I explained autonomy levels (required for Part B)
- [ ] I included multi-agent coordination notes (if applicable)
- [ ] Time savings are realistic and measured

---

## FAQ

**Q: Can I use Claude Code automations from Week 4 in Warp?**

A: Conceptually yes—you can recreate slash commands as Warp saved prompts. But they need to be adapted to Warp's format.

---

**Q: Do I need to use git worktree for Part B?**

A: Technically no, but it's **highly recommended**. Without it, agents will conflict when editing the same files.

---

**Q: How many agents should I run in parallel?**

A: Start with 2-3. Advanced users can try 4-5. More than 5 is rarely worth it (coordination overhead).

---

**Q: What if my agents conflict even with worktrees?**

A: Double-check:
- Each agent is in a different directory (`pwd` in each tab)
- Each agent is on a different branch (`git branch`)
- Agents aren't modifying the same file

---

**Q: Can I do Part B without Part A?**

A: No, the assignment requires **at least one from each part**.

---

**Q: What autonomy level should I use?**

A: Depends on risk:
- **High autonomy:** Well-defined tasks, low risk (adding tests)
- **Medium autonomy:** Some discretion needed (adding features)
- **Low autonomy:** High risk or unclear requirements

Document your reasoning in writeup.md.

---

## Resources

- **Warp Official Docs:** https://www.warp.dev/
- **Git Worktree Tutorial:** https://git-scm.com/docs/git-worktree
- **Warp University:** https://www.warp.dev/university
- **Week 4 Assignment Bridge:** (review for automation concepts)

---

## Final Encouragement

"Week 5 is harder than Week 4 because you're adding parallelization.

But the payoff is huge: **2-4x speedup** on multi-task projects.

**Start simple:**
1. Get comfortable with Warp Drive (Part A)
2. Practice git worktree manually
3. Try 2 agents on simple tasks
4. Scale up to 3-4 agents

**Don't try to run 5 agents on complex tasks on your first attempt.**

Build up gradually. You'll get there.

Good luck! 🚀"
