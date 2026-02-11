# Assignment Bridge: From Lecture to Building Automations

**Purpose:** Connect the lecture concepts to your actual assignment tasks.

**Target Audience:** 18-year-olds with no CS background who might be feeling overwhelmed.

---

## Don't Panic: This Assignment Is Different

"I know what you're thinking: 'The previous assignments had clear deliverables—build an MCP server, write code. This assignment says 'build automations' but doesn't tell me exactly what to code. Help!'

**Take a deep breath.**

This assignment is intentionally open-ended because you're learning a different skill: **workflow design.**

You're not graded on 'did you implement function X correctly.' You're graded on:
1. **Did you identify a repetitive workflow?**
2. **Did you automate it?**
3. **Did you document it clearly?**
4. **Does it actually save time?**

Let's break this down into concrete steps."

---

## The Mental Model: Lecture → Assignment Mapping

| Lecture Concept | Assignment Requirement | What You'll Actually Do |
|----------------|------------------------|------------------------|
| Slash commands | "Custom slash commands checked into `.claude/commands/*.md`" | Create 1-2 `.md` files with workflows |
| CLAUDE.md | "`CLAUDE.md` files for repository guidance" | Write a single `CLAUDE.md` explaining your project |
| SubAgents | "Claude SubAgents working together" | Design a multi-step workflow with specialized roles |
| MCP servers | "MCP servers integrated into Claude Code" | Use an MCP server from Week 3 in a workflow |

**Key insight:** You pick **at least 2** from this menu. Mix and match. For example:
- Option A: 2 slash commands
- Option B: 1 slash command + 1 CLAUDE.md
- Option C: 1 SubAgent workflow + 1 MCP integration
- Option D: 1 slash command + 1 SubAgent workflow

**There's no single "right" answer.**

---

## Step-by-Step: From Zero to Submission

### Step 0: Understand the Starter App (30 minutes)

Before you can automate workflows, you need to understand what the app does.

**Action items:**
1. Run the app:
   ```bash
   cd week4
   conda activate cs146s
   make run
   ```

2. Open http://localhost:8000 in your browser

3. Play with it:
   - Create a note
   - Create an action item
   - Mark an item as complete

4. Look at the code structure:
   ```
   backend/app/
   ├── main.py          # Entry point
   ├── models.py        # Database models (Note, ActionItem)
   ├── schemas.py       # Pydantic validation
   ├── db.py            # Database connection
   ├── routers/
   │   ├── notes.py     # Note endpoints
   │   └── action_items.py  # Action item endpoints
   └── services/
       └── extract.py   # Text extraction logic
   ```

5. Read `docs/TASKS.md`—these are **suggested improvements** you might automate

**Why this matters:** You can't automate a workflow you don't understand.

---

### Step 1: Identify Manual Workflows (1 hour)

"A workflow is **a sequence of steps you do repeatedly.**

Look at `docs/TASKS.md`. Each task is a potential workflow. Let's analyze them:

#### Task 2: 'Add search endpoint for notes'
**Manual workflow:**
1. Open `routers/notes.py`
2. Write a new route function
3. Test it manually in browser
4. Oh wait, should write tests first
5. Open `backend/tests/test_notes.py`
6. Write tests
7. Run `make test`
8. Fix bugs
9. Run tests again
10. Update docs (if you remember)
11. Format code: `make format`
12. Commit

**Repetitive?** Yes. Every time you add an endpoint, same steps.

**Automatable?** Absolutely.

**Automation options:**
- **Slash command:** `/add-endpoint` (define the workflow in `.md` file)
- **SubAgents:** TestAgent writes tests, CodeAgent implements, DocsAgent updates docs

#### Task 4: 'Improve extraction logic'
**Manual workflow:**
1. Open `services/extract.py`
2. Modify the parsing code
3. Open `backend/tests/test_extract.py` (if it exists—it doesn't yet!)
4. Write tests for new parsing
5. Run tests
6. Debug
7. Repeat until green

**Automatable with:** SubAgent workflow (TestAgent + CodeAgent)

**Your job:** Pick 2+ workflows like these and automate them."

---

### Step 2: Choose Your Automation Type (30 minutes)

"Based on the workflow, choose the right tool.

#### Decision Matrix:

**Use a slash command if:**
- ✅ The workflow has clear, ordered steps
- ✅ You'll run it multiple times (3+ times)
- ✅ The steps are mostly the same each time
- ✅ Example: Adding a new endpoint, running tests with coverage, refactoring a module

**Use CLAUDE.md if:**
- ✅ You're tired of explaining the same things every conversation
- ✅ The information is **always** relevant (not just for one task)
- ✅ It's about 'how this project works' not 'how to do X'
- ✅ Example: Project structure, testing policy, coding standards

**Use SubAgents if:**
- ✅ The task has distinct roles (test writing vs code writing)
- ✅ One AI doing everything leads to forgotten steps
- ✅ You want specialized focus for each step
- ✅ Example: TDD workflow, docs sync, schema migrations

**Use MCP servers if:**
- ✅ You need external data or services
- ✅ You already built an MCP server in Week 3
- ✅ Example: Creating GitHub issues from notes, fetching weather for location-based features

**Still confused?** Here's a cheat sheet:

| I want to... | Use this |
|-------------|----------|
| Run tests automatically | Slash command `/test` |
| Explain project structure | CLAUDE.md |
| Add endpoint with TDD | SubAgents (TestAgent + CodeAgent) |
| Create GitHub issue when bug found | MCP + Slash command |
| Set coding standards | CLAUDE.md |
| Refactor a module safely | Slash command `/refactor` |"

---

### Step 3: Build Your First Automation (1-2 hours)

"Let's walk through building **one automation from scratch.**

#### Example: Slash Command for Adding Tests

**Goal:** Create `/add-test` that generates test files for endpoints.

**Step 3a: Create the directory**
```bash
mkdir -p .claude/commands
```

**Step 3b: Create the file**
```bash
touch .claude/commands/add-test.md
```

**Step 3c: Write the workflow**

Open `.claude/commands/add-test.md` and write:

````markdown
# Add Test

Creates a test file for an API endpoint.

## Arguments
- $ENDPOINT_PATH: The API path (e.g., /notes or /action-items/{id})

## Steps

1. Determine the router file from the endpoint path:
   - /notes → backend/app/routers/notes.py
   - /action-items → backend/app/routers/action_items.py

2. Read the router file to understand the endpoint logic

3. Create a test file if it doesn't exist:
   - Path: backend/tests/test_<router_name>.py
   - If it exists, add tests to the existing file

4. Write comprehensive tests:
   - Happy path (successful request)
   - Edge cases (404, validation errors)
   - Boundary conditions

5. Run the tests:
   ```bash
   pytest backend/tests/test_<router_name>.py -v
   ```

6. If tests fail:
   - Show the error output
   - Ask the user: "Tests failed. Would you like me to debug the tests or abort?"

7. If tests pass:
   - Show success message
   - Show coverage: `pytest --cov=backend/app backend/tests/test_<router_name>.py`

## Safety Rules

- Never modify the actual endpoint code (only write tests)
- Never commit changes (let user review first)
- If test file already exists, ask before overwriting tests

## Expected Output

- New or updated test file with at least 3 test functions
- All tests passing
- Summary of test coverage
````

**Step 3d: Test it**

In Claude Code, type:
```
/add-test /notes
```

Claude should:
1. Read `routers/notes.py`
2. Create or update `tests/test_notes.py`
3. Write tests for all `/notes` endpoints
4. Run pytest
5. Show results

**If it works:** ✅ You've built your first automation!

**If it doesn't work:** Debug by:
- Checking the `.md` file for typos
- Making instructions more specific
- Testing manually first

**Step 3e: Document it**

In `writeup.md`, fill out the Automation #1 section:
```markdown
### Automation #1

a. Design inspiration
> Based on the "Slash Commands" section of Claude Code best practices.
> Automates the repetitive task of writing tests for new endpoints.

b. Design
> **Goal:** Generate comprehensive test files for API endpoints
> **Input:** Endpoint path (e.g., /notes)
> **Output:** Test file with passing tests
> **Steps:** (1) Identify router, (2) Read endpoint logic, (3) Generate tests, (4) Run pytest

c. How to run it
> Command: `/add-test <endpoint_path>`
> Example: `/add-test /notes`
> Expected output: New test file, all tests green

d. Before vs after
> **Before:** Manually write test file, write each test case, run pytest, debug, repeat (30 minutes)
> **After:** Type one command, get comprehensive tests in 2 minutes

e. How you used it
> Used `/add-test` to create tests for the search endpoint (Task 2 in TASKS.md).
> The automation generated tests for successful search, empty results, and case-insensitive matching.
```

---

### Step 4: Build Your Second Automation (1-2 hours)

"Now that you've built one, build another using a **different technique.**

If your first was a slash command, make your second:
- A CLAUDE.md file, OR
- A SubAgent workflow, OR
- An MCP integration

#### Example: CLAUDE.md for Project Guidance

**Step 4a: Create the file**
```bash
touch CLAUDE.md
```

**Step 4b: Fill it out**

```markdown
# Developer Command Center - Project Guide

## What This Project Is

A minimal full-stack application for developers to manage notes and action items.
- **Backend:** FastAPI with SQLite
- **Frontend:** Static HTML/JS (no build step)
- **Purpose:** Practice agent-driven development workflows

## Project Structure

```
week4/
├── backend/app/          # FastAPI application
│   ├── main.py           # App entry point, routes setup
│   ├── models.py         # SQLAlchemy models (Note, ActionItem)
│   ├── schemas.py        # Pydantic schemas for validation
│   ├── db.py             # Database connection and session
│   ├── routers/          # API route handlers
│   │   ├── notes.py      # CRUD operations for notes
│   │   └── action_items.py  # CRUD operations for action items
│   └── services/
│       └── extract.py    # Text extraction utilities
├── backend/tests/        # pytest test files
├── frontend/             # Static HTML/CSS/JS
├── data/                 # SQLite database and seed data
└── docs/                 # Documentation and task lists
```

## How to Run

### Setup
1. Activate conda environment: `conda activate cs146s`
2. (Optional) Install pre-commit: `pre-commit install`

### Development
- **Run app:** `make run` (from week4/ directory)
- **Run tests:** `make test`
- **Format code:** `make format`
- **Lint code:** `make lint`

### Access Points
- Frontend: http://localhost:8000
- API docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

## Testing Policy

**Every new endpoint MUST have tests.**

- Test location: `backend/tests/test_<router_name>.py`
- Test framework: pytest
- Test structure:
  ```python
  def test_<endpoint>_<scenario>(...):
      # Arrange, Act, Assert
  ```
- Coverage goal: >80% for new code

**Run tests before committing.** Pre-commit hooks enforce formatting/linting.

## Code Standards

### Python Style
- **Formatter:** black (automated via `make format`)
- **Linter:** ruff (check with `make lint`)
- **Type hints:** Required for all function signatures
- **Imports:** Organized alphabetically within groups

### API Patterns
- **Validation:** Use Pydantic schemas for request/response models
- **Errors:** Return appropriate HTTP status codes:
  - 200: Success
  - 201: Created
  - 204: No content (delete)
  - 400: Validation error
  - 404: Not found
  - 500: Server error
- **Database:** Use SQLAlchemy ORM, no raw SQL

### Commit Messages
Follow conventional commits:
- `feat: Add search endpoint for notes`
- `fix: Handle empty search query`
- `docs: Update API documentation`
- `test: Add edge cases for note creation`

## Safety Rules

### DO
- ✅ Write tests before implementing features (TDD)
- ✅ Run `make test` before committing
- ✅ Use type hints
- ✅ Handle errors gracefully

### DO NOT
- ❌ Commit code with failing tests
- ❌ Delete database files without asking
- ❌ Modify the database schema without migration plan
- ❌ Skip pre-commit hooks
- ❌ Commit directly to main (use feature branches)

## Common Commands

```bash
# Add a new endpoint
# 1. Write tests in backend/tests/
# 2. Implement in backend/app/routers/
# 3. Run make test
# 4. Update docs/API.md

# Modify database model
# 1. Update backend/app/models.py
# 2. Consider migration impact
# 3. Update schemas.py
# 4. Update seed data if needed
# 5. Delete data/db.sqlite to reset

# Debug
# - Check logs in terminal where `make run` is running
# - Use `/docs` endpoint to test API manually
# - Use `pytest -v` for verbose test output
```

## Tasks to Practice With

See `docs/TASKS.md` for suggested improvements to the application.
These tasks are designed to practice agent-driven workflows.
```

**Step 4c: Test it**

Start a new conversation in Claude Code. Ask:
```
"Where do I add new API endpoints in this project?"
```

Claude should reference the information from CLAUDE.md without you having to explain.

**Step 4d: Document it**

Fill out Automation #2 in `writeup.md`."

---

### Step 5: Use Your Automations (1 hour)

"This is **Part II** of the assignment: Actually use your automations to enhance the app.

Pick tasks from `docs/TASKS.md` and use your automations to complete them.

**Example:**

You built `/add-test`. Now use it:

1. Run: `/add-test /notes/search`
2. Claude generates tests for the search endpoint
3. Implement the search endpoint code
4. Tests pass ✅

**Document this in writeup.md:**
```markdown
e. How you used the automation to enhance the starter application
> I used the `/add-test` automation to complete Task 2 from TASKS.md:
> 'Add search endpoint for notes.'
>
> Workflow:
> 1. Ran `/add-test /notes/search`
> 2. Claude generated 4 test cases (exact match, partial match, case-insensitive, empty query)
> 3. I implemented the search logic in routers/notes.py
> 4. Tests passed on first try
> 5. Total time: 10 minutes (vs 30+ minutes manually)
```

**Do this for both automations.**"

---

## Example Automation Ideas (If You're Stuck)

"Can't think of what to automate? Here are proven ideas:

### Easy (Good for First Automation)

1. **Slash command: `/test-coverage`**
   - Run pytest with coverage
   - Show which files need more tests
   - Highlight files below 80% coverage

2. **CLAUDE.md: Project guidance**
   - Explain project structure
   - Document how to run, test, lint
   - Set coding standards

3. **Slash command: `/format-and-lint`**
   - Run `make format`
   - Run `make lint`
   - Show any remaining issues

### Medium (Good for Second Automation)

4. **Slash command: `/add-endpoint`**
   - Input: Method, path, description
   - Generate test file
   - Generate router function
   - Run tests
   - Update docs

5. **SubAgent workflow: TDD for features**
   - TestAgent: Write failing tests
   - CodeAgent: Implement to pass tests
   - DocsAgent: Update documentation

6. **Slash command: `/refactor-safe`**
   - Input: Old name, new name
   - Rename files/functions
   - Update imports
   - Run tests to verify nothing broke

### Advanced (If You Want a Challenge)

7. **MCP integration: `/create-github-issue`**
   - Use GitHub MCP server from Week 3
   - Create issue from a note
   - Link issue number in commit message

8. **SubAgent workflow: Schema migration**
   - DBAgent: Propose schema change
   - MigrationAgent: Write migration script
   - TestAgent: Update tests
   - Verification: Run tests and check data integrity

9. **Slash command: `/docs-drift-check`**
   - Fetch `/openapi.json`
   - Compare to `docs/API.md`
   - Show endpoints that are documented but not implemented
   - Show endpoints that exist but aren't documented

**Pick 2 that excite you.**"

---

## Common Mistakes to Avoid

### Mistake 1: Making Automations Too Complex

**Bad:**
```markdown
# Do Everything
Add a feature, write tests, update docs, refactor the codebase, deploy to production, send a Slack notification, and make coffee.
```

**Good:**
```markdown
# Add Feature
Adds a new feature using TDD approach.
[Clear steps, focused scope]
```

**Why:** Complex automations are hard to debug and rarely reusable.

### Mistake 2: No Safety Guardrails

**Bad:**
```markdown
## Steps
1. Delete all test files
2. Rewrite them
```

**Good:**
```markdown
## Steps
1. ASK USER: "This will regenerate tests. Continue? (y/n)"
2. If yes, backup existing tests to tests_backup/
3. Generate new tests
4. Run both old and new tests side-by-side
```

**Why:** Automations should never be destructive without confirmation.

### Mistake 3: Forgetting to Document

**Symptom:** You build an automation, but in `writeup.md` you just write "I made a slash command."

**Solution:** Follow the writeup structure:
- Design inspiration (cite docs)
- Design (goals, inputs, outputs, steps)
- How to run it (exact commands)
- Before vs after (time savings)
- How you used it (specific example)

**Why:** The writeup is 50% of your grade. A great automation with poor docs = low score.

### Mistake 4: Not Actually Using Your Automations

**Symptom:** You build `/add-endpoint` but then manually add endpoints anyway.

**Solution:** After building an automation, **force yourself to use it** for at least one real task.

**Why:** Part II of the assignment explicitly asks: "How you used the automation to enhance the starter application."

---

## Timeline: How to Finish in 4-5 Hours

- **Hour 1:** Understand the starter app, read TASKS.md, pick 2 workflows to automate
- **Hour 2:** Build automation #1 (e.g., slash command)
- **Hour 3:** Build automation #2 (e.g., CLAUDE.md or SubAgent workflow)
- **Hour 4:** Use both automations to complete tasks from TASKS.md
- **Hour 5:** Fill out writeup.md with detailed documentation

**Buffer:** +1 hour for debugging and polish

**Total: 5-6 hours**

---

## Self-Check Before Submitting

Answer these questions honestly:

### Automation Quality

- [ ] **Does each automation have a clear, specific purpose?**
- [ ] **Can someone else use my automation by reading the docs?**
- [ ] **Does each automation have safety guardrails?** (confirmations, non-destructive)
- [ ] **Have I tested each automation at least once?**

### Documentation Quality

- [ ] **Did I fill out all TODOs in writeup.md?**
- [ ] **Did I cite the Claude Code best practices docs?**
- [ ] **Did I explain the design clearly?** (goals, inputs, outputs, steps)
- [ ] **Did I show before/after comparisons?**
- [ ] **Did I describe how I actually used the automation?**

### Demonstration

- [ ] **Did I use each automation to enhance the starter app?**
- [ ] **Can I point to specific code changes made with the automation?**
- [ ] **Did I complete at least one task from TASKS.md?**

If you answered "yes" to all of these, you're ready to submit.

---

## Rubric Translation (What Graders Look For)

"Let me decode the grading rubric for you:

### Automation Functionality (40%)

**What they're looking for:**
- Do the automations actually work?
- Can the grader run them and get the expected result?
- Are they genuinely useful (not toy examples)?

**How to get full points:**
- Test your automations before submitting
- Include clear usage instructions
- Show a real use case (not just 'it works in theory')

### Documentation Quality (30%)

**What they're looking for:**
- Is the writeup complete?
- Can someone understand your design without asking questions?
- Did you cite sources (best practices docs)?

**How to get full points:**
- Fill out every section of writeup.md
- Use concrete examples (not vague descriptions)
- Include actual commands, not just 'run the automation'

### Workflow Improvement (20%)

**What they're looking for:**
- Did you actually save time?
- Is the before/after comparison clear?
- Did you use the automation to enhance the app?

**How to get full points:**
- Show real numbers ('30 minutes manual vs 2 minutes automated')
- Point to specific code changes made with automation
- Complete at least one TASKS.md item using your automation

### Creativity & Insight (10%)

**What they're looking for:**
- Did you choose interesting workflows to automate?
- Did you combine features creatively?
- Did you go beyond the minimum?

**How to get full points:**
- Don't just copy the examples—add your own twist
- Combine features (e.g., slash command that spawns SubAgents)
- Automate something the assignment didn't suggest

---

## FAQ: Common Student Questions

**Q: Do I need to write actual code or just markdown files?**

A: Depends on your automations:
- Slash commands: Just `.md` files
- CLAUDE.md: Just a single `.md` file
- SubAgents: Mainly documentation of the workflow
- MCP: You already wrote code in Week 3, just integrate it

**Most of the assignment is configuration/documentation, not Python code.**

---

**Q: Can I use the same MCP server from Week 3?**

A: Yes! In fact, that's encouraged. Show how to integrate it into a slash command or SubAgent workflow.

---

**Q: How many automations do I need?**

A: Minimum 2. But quality > quantity. Two excellent automations > four mediocre ones.

---

**Q: Can I work with a partner?**

A: Check with your TA, but typically these are individual assignments. You can discuss ideas, but build your own automations.

---

**Q: What if my automation doesn't work perfectly?**

A: Document the limitations in your writeup:
- "Known issue: Doesn't handle nested endpoints"
- "Future improvement: Add confirmation prompts"

Acknowledging limitations shows maturity.

---

**Q: Do I have to use the starter app?**

A: Yes, the assignment specifically says to use it. The graders will run your automations on the starter app.

---

**Q: How do I know if I'm done?**

A: When you can answer "yes" to:
1. I have at least 2 working automations
2. I've documented them thoroughly in writeup.md
3. I've used each automation to enhance the starter app
4. Someone else could use my automations by reading my docs

---

## Resources

- **Claude Code Best Practices:** https://www.anthropic.com/engineering/claude-code-best-practices
- **SubAgents Documentation:** https://docs.anthropic.com/en/docs/claude-code/sub-agents
- **Example Slash Commands:** Check `.claude/commands/` in open-source repos
- **CLAUDE.md Examples:** Search GitHub for "CLAUDE.md" to see real projects

---

## Final Encouragement

"This assignment is different because there's no 'correct answer.' Two students can build completely different automations and both get full marks.

**Your creativity is the feature, not a bug.**

The best automations come from:
1. Noticing pain points in your own workflow
2. Thinking 'there must be a better way'
3. Designing a solution that saves time

You're not just completing an assignment—you're learning to think like an efficiency engineer.

Every great software tool started with someone saying, 'I'm tired of doing this manually. Let me automate it.'

That's what you're learning this week.

Good luck! 🚀"
