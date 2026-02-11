# Lecture Transcript: The Autonomous Coding Agent in Real Life

**Date:** Week 4 - Fall 2025
**Topic:** Building Claude Code Automations for Developer Workflows
**Target Audience:** Complete beginners (18-year-olds with no CS background)

---

## Introduction: From Tool User to Workflow Designer

"Welcome to Week 4! Over the past three weeks, you've learned how to use AI as a tool:
- Week 1: Prompting techniques
- Week 2: MCP for connecting AI to data
- Week 3: Building custom MCP servers

But here's the truth: using AI as a one-off tool is powerful, but it's not transformative.

**The real power comes when you automate your workflows.**

Think about it: you don't just use a hammer once to build a house. You design systems. You create blueprints. You set up assembly lines.

This week, we're going to learn how to **design AI-powered workflows** that automate repetitive tasks in software development. Not just 'ask Claude to write code,' but 'create a system where Claude automatically runs tests, updates docs, and deploys code—all with one command.'"

---

## The Big Picture: What Is Claude Code?

"Before we dive into specific features, let's understand what Claude Code actually is.

**Claude Code is not just a chatbot.** It's an **autonomous coding agent**—an AI system that can:
1. Read and write files
2. Run terminal commands
3. Search codebases
4. Execute multi-step workflows
5. Spawn specialized sub-agents for complex tasks

**The key word is 'autonomous.'** You don't micromanage every step. You define the goal, and Claude figures out the steps.

**Real-world example:**
- **Old way (manual):** 'Claude, write a test for this function. Now run it. Now fix the bug. Now run it again. Now update the docs.'
- **New way (automated):** '/add-feature login' → Claude writes tests, implements code, runs tests, updates docs, commits changes. All automatic.

That's what we're building this week."

---

## Analogy: Claude Code as Your Personal Dev Team

"Let me give you an analogy that will make everything click.

**Imagine you're the tech lead of a startup. You have a team of developers:**

1. **TestBot** - Only writes and runs tests
2. **CodeBot** - Only implements features
3. **DocsBot** - Only updates documentation
4. **LintBot** - Only checks code quality

When you need to add a new feature, you don't do everything yourself. You assign tasks:
- 'TestBot, write tests for login.'
- 'CodeBot, implement login to pass those tests.'
- 'DocsBot, update the API docs.'
- 'LintBot, make sure the code is clean.'

Each bot is specialized. They work in parallel. They follow strict rules.

**Claude Code lets you build this team—but the 'bots' are AI agents, not humans.**

The features we're learning today are the tools for building and managing this AI team:
- **Slash commands** = Repeatable workflows you can trigger
- **CLAUDE.md** = The company handbook (how things work here)
- **SubAgents** = Specialized team members with different roles
- **MCP servers** = External tools/APIs your team can use

Let's break down each one."

---

## Feature 1: Custom Slash Commands

### What Are They?

"Slash commands are **reusable workflows stored as Markdown files.**

You create a file like `.claude/commands/run-tests.md` and define a workflow. Then you can trigger it by typing `/run-tests` in Claude Code.

**Think of them as macros or scripts—but written in natural language instead of code.**"

### Why Do They Matter?

"As a developer, you do the same things over and over:
- Run tests before committing
- Update docs after changing APIs
- Refactor code and verify nothing broke
- Deploy to staging

Without slash commands, you have to **manually tell Claude each step every time.**

With slash commands, you **define the workflow once and reuse it.**

**Real-world example:**

Imagine you're working on a web app. Every time you add a new API endpoint, you need to:
1. Write the code
2. Run tests
3. Update the OpenAPI docs
4. Check for lint errors
5. Commit with a descriptive message

**Without slash command (manual):**
You type all of this every time:
```
'Write tests for GET /users'
'Now implement the endpoint'
'Now run pytest'
'Now update docs/API.md'
'Now run ruff'
'Now commit with message...'
```

**With slash command (automated):**
You create `/add-endpoint` once, then just type:
```
/add-endpoint GET /users 'Returns list of users'
```

Claude executes all 5 steps automatically."

### How Do They Work?

"Slash commands are Markdown files with instructions for Claude.

**Example: `.claude/commands/run-tests.md`**

```markdown
# Run Tests

Run the test suite with coverage reporting.

## Steps

1. Run pytest with these flags: `pytest -v --cov=backend/app backend/tests`
2. If tests fail:
   - Show the failing test output
   - Ask the user if they want to debug or abort
3. If tests pass:
   - Show the coverage report
   - Summarize which files have low coverage (<80%)

## Safety

- Never commit if tests fail
- Never modify test files unless explicitly asked
```

**What happens:**
1. User types `/run-tests`
2. Claude reads this file
3. Claude executes each step in order
4. Claude follows the safety rules

**The genius:** You write this **once**. Then every developer on your team can use it by typing 8 characters."

### Anatomy of a Good Slash Command

"A well-designed slash command has:

**1. Clear intent:** What is this for?
```markdown
# Add API Endpoint
Creates a new FastAPI endpoint with tests and docs.
```

**2. Inputs (optional):** What does the user provide?
```markdown
## Arguments
- $METHOD: HTTP method (GET, POST, etc.)
- $PATH: Endpoint path (e.g., /users)
- $DESCRIPTION: What this endpoint does
```

**3. Steps:** What to do, in order
```markdown
## Steps
1. Create a test file in `backend/tests/`
2. Write failing tests for the endpoint
3. Implement the endpoint in `backend/app/routers/`
4. Run tests until they pass
5. Update docs/API.md
```

**4. Safety guardrails:** What NOT to do
```markdown
## Safety
- Don't modify existing endpoints without confirmation
- Don't commit code with failing tests
- Don't delete files
```

**5. Output expectations:** What should the result look like?
```markdown
## Expected Output
- New file: `backend/tests/test_<name>.py`
- Updated file: `backend/app/routers/<name>.py`
- Updated: `docs/API.md`
- All tests passing
```

**Pro tip:** Treat your slash command like a recipe. Someone who has never seen your codebase should be able to follow it."

---

## Feature 2: CLAUDE.md Guidance Files

### What Is CLAUDE.md?

"A `CLAUDE.md` file is a **persistent instruction manual** that Claude reads at the start of every conversation.

Think of it as the **README for AI**—not for humans, for Claude.

**Where it lives:**
- Root of repo: `/CLAUDE.md` (applies to whole project)
- Subdirectories: `/backend/CLAUDE.md` (applies when working in backend)

**What it contains:**
- How to run the app
- Where important files are
- Coding standards and style
- Commands to avoid
- Testing requirements"

### Why Do You Need It?

"Without CLAUDE.md, every time you start a new conversation with Claude, you have to explain:
- 'This is a FastAPI app'
- 'Tests live in backend/tests/'
- 'Use black for formatting'
- 'Never commit without running tests'

**That's exhausting.** And you forget things.

With CLAUDE.md, Claude **automatically knows all of this** when you start a conversation.

**Real-world example:**

You're working with a teammate on a Python project. They keep forgetting to run `black` before committing, so the CI keeps failing.

**Solution:** Add to `CLAUDE.md`:
```markdown
## Code Style
- Always run `black .` before committing
- Always run `ruff check .` for linting
- Pre-commit hooks enforce this
```

Now, whenever Claude makes changes, it automatically runs these checks—no reminder needed."

### What to Put in CLAUDE.md

"**Think of CLAUDE.md as your project's 'rules of engagement.'**

#### Section 1: Project Structure
```markdown
## Project Structure
This is a FastAPI app with:
- Backend: `backend/app/` (main.py, routers/, models.py)
- Frontend: `frontend/` (static HTML/JS)
- Tests: `backend/tests/`
- Database: SQLite at `data/db.sqlite`
```

**Why this matters:** Claude knows where to create new files.

#### Section 2: How to Run
```markdown
## Running the App
1. Activate environment: `conda activate cs146s`
2. Start server: `make run` (from week4/ directory)
3. Access: http://localhost:8000
4. API docs: http://localhost:8000/docs
```

**Why this matters:** Claude can test changes automatically.

#### Section 3: Testing Policy
```markdown
## Testing
- Every new endpoint needs tests
- Run tests: `make test`
- Tests must pass before committing
- Use `pytest.mark` for categorization
```

**Why this matters:** Prevents untested code from being committed.

#### Section 4: Safety Rules
```markdown
## Do NOT
- Delete database files without confirmation
- Commit directly to main (use branches)
- Modify schema without migration
- Skip pre-commit hooks
```

**Why this matters:** Prevents destructive actions.

#### Section 5: Code Style
```markdown
## Code Standards
- Use type hints for all functions
- Pydantic for validation
- SQLAlchemy for database
- Black for formatting, Ruff for linting
```

**Why this matters:** Consistent code quality."

### CLAUDE.md vs Slash Commands

"Students often ask: 'What's the difference?'

| CLAUDE.md | Slash Commands |
|-----------|----------------|
| **Persistent knowledge** | **Executable workflows** |
| Always active | Trigger on-demand |
| 'Here's how this project works' | 'Here's a specific task' |
| Like a handbook | Like a script |
| Influences all of Claude's behavior | Executes specific steps |

**Example:**
- CLAUDE.md says: 'Tests live in backend/tests/'
- Slash command `/add-test` uses that knowledge to create tests in the right place

They work together."

---

## Feature 3: SubAgents (Role-Specialized Agents)

### What Are SubAgents?

"SubAgents are **specialized AI assistants**, each focused on a specific role.

Instead of one Claude doing everything, you spawn multiple 'mini-Claudes,' each with:
- A specialized system prompt
- Limited tool access
- A specific goal

**Analogy:** It's like hiring specialists instead of a generalist.

You wouldn't ask your dentist to also fix your car, right? Same principle here."

### Why Use SubAgents?

"**Problem:** Complex tasks require conflicting priorities.

**Example: Adding a new feature**
- Writing tests requires being **pessimistic** (think of edge cases, break things)
- Writing code requires being **optimistic** (make it work, ship fast)
- Writing docs requires being **user-focused** (explain clearly, avoid jargon)

**One AI can't be all three at once.**

**Solution:** Create three SubAgents:
1. **TestAgent:** 'You are a test engineer. Write comprehensive tests. Think of edge cases.'
2. **CodeAgent:** 'You are a pragmatic developer. Write clean, simple code that passes tests.'
3. **DocsAgent:** 'You are a technical writer. Explain this feature to a new developer.'

Each agent has a **single, clear role**—so it does that role exceptionally well."

### Real-World SubAgent Workflow

"Let's walk through a concrete example: **Adding a 'delete note' feature to our app.**

**Without SubAgents (one Claude does everything):**
1. Claude writes tests
2. Claude implements delete endpoint
3. Claude updates docs
4. ...but wait, did the tests cover the 'note doesn't exist' case?
5. ...and did we update the OpenAPI schema?
6. Context is lost, things slip through cracks

**With SubAgents:**

**Agent 1: TestAgent**
- System prompt: 'You write comprehensive tests. Think of edge cases. Use pytest.'
- Task: 'Write tests for DELETE /notes/{id}'
- Output:
  ```python
  def test_delete_note_success(...)
  def test_delete_nonexistent_note(...)  # Edge case!
  def test_delete_note_updates_count(...)
  ```

**Agent 2: CodeAgent**
- System prompt: 'You implement clean, type-hinted code. Make tests pass.'
- Input: The tests TestAgent wrote
- Task: 'Implement DELETE /notes/{id} to pass these tests'
- Output:
  ```python
  @router.delete('/{note_id}', status_code=204)
  def delete_note(note_id: int, db: Session = Depends(get_db)):
      note = db.get(Note, note_id)
      if not note:
          raise HTTPException(status_code=404)
      db.delete(note)
      db.commit()
  ```

**Agent 3: DocsAgent**
- System prompt: 'You update documentation. Check for drift between code and docs.'
- Task: 'Update docs/API.md with the new DELETE endpoint'
- Output: Adds a new section to API.md with example request/response

**Final step: Main Claude**
- Runs all tests
- Confirms everything works
- Commits: 'feat: Add DELETE /notes endpoint'

**Notice:** Each agent had **one job**. Together, they completed the feature **thoroughly** without dropping the ball."

### How to Design SubAgents

"**Rule 1: One role, one agent**

Bad:
- 'Agent1: Write code and tests'

Good:
- 'Agent1: Write tests'
- 'Agent2: Write code'

**Rule 2: Give each agent a clear persona**

Instead of:
- 'You are an agent that writes tests.'

Write:
- 'You are a senior QA engineer at Google. Your job is to find bugs before they reach production. Be thorough, think of edge cases, and never assume code works without testing.'

**Personas make agents more effective.**

**Rule 3: Limit each agent's tools**

TestAgent should:
- Read code ✅
- Write test files ✅
- Run pytest ✅

TestAgent should NOT:
- Modify app code ❌
- Commit changes ❌
- Deploy ❌

**Limiting tools prevents accidents.**

**Rule 4: Use handoffs**

Agents shouldn't run in parallel for dependent tasks. Use a sequence:

```
TestAgent → CodeAgent → DocsAgent → Main Claude (verify)
```

Each agent **hands off** to the next."

---

## Feature 4: MCP Servers in Claude Code

"You already built MCP servers in Week 3. This week, you'll **integrate them into workflows**.

**Quick recap:**
- MCP servers give Claude access to external data (GitHub, weather, databases, etc.)
- You configure them in Claude Desktop settings

**New this week:**
- Use MCP servers **inside slash commands**
- Use MCP servers **from SubAgents**

**Example workflow:**

Slash command: `/create-github-issue`
```markdown
# Create GitHub Issue

## Steps
1. Use the GitHub MCP server to create a new issue
2. Use the issue number in a commit message
3. Update the project's TASKS.md file
```

When you type `/create-github-issue 'Bug in login'`, Claude:
1. Calls the GitHub MCP server tool
2. Gets back the issue number (#42)
3. Creates a commit: 'fix: Address login bug (closes #42)'
4. Updates TASKS.md"

---

## Putting It All Together: A Complete Workflow

"Let's design a **production-quality workflow** using all four features.

**Scenario:** You're working on a FastAPI app. You want to add a new feature: 'Tag notes with categories.'

### Step 1: Define CLAUDE.md (One-time setup)

```markdown
## Project: Developer Command Center

### Structure
- Backend: FastAPI app at backend/app/
- Frontend: Static site at frontend/
- Tests: backend/tests/
- DB: SQLite at data/db.sqlite

### Testing Policy
- Every new endpoint needs tests in backend/tests/
- Run: `make test`
- Tests must pass before committing

### Style
- Use type hints
- Use Pydantic for validation
- Run `make format` before committing
```

### Step 2: Create slash command

`.claude/commands/add-feature.md`
```markdown
# Add Feature

Adds a new feature with TDD approach.

## Arguments
- $FEATURE_NAME: Name of the feature

## Steps
1. Spawn TestAgent to write failing tests
2. Spawn CodeAgent to implement the feature
3. Run tests until green
4. Spawn DocsAgent to update documentation
5. Run `make format`
6. Commit with conventional commit message

## Safety
- Don't commit if tests fail
- Don't modify existing features without confirmation
```

### Step 3: Execute

You type:
```
/add-feature 'Tag notes with categories'
```

### Step 4: Claude orchestrates

**SubAgent 1: TestAgent**
- Reads CLAUDE.md (knows where tests go)
- Writes `test_tags.py` with tests for:
  - Adding tags to notes
  - Searching notes by tag
  - Removing tags

**SubAgent 2: CodeAgent**
- Reads the tests
- Updates `models.py` (adds Tag model)
- Updates `routers/notes.py` (adds tag endpoints)
- Runs tests → all green ✅

**SubAgent 3: DocsAgent**
- Reads `/openapi.json`
- Updates `docs/API.md`
- Checks for drift

**Main Claude:**
- Runs `make format`
- Runs `make test` (final verification)
- Commits: 'feat: Add tag support for notes'

**Total time:** ~30 seconds.
**Your effort:** Typed one command.
**Result:** Complete feature with tests, docs, and clean code."

---

## Best Practices from Production Systems

"Let me share what professional teams do with Claude Code:

### Practice 1: Idempotent Slash Commands

**Idempotent** = Running it twice has the same effect as running it once.

Bad slash command:
```markdown
1. Create file foo.py
2. Add code...
```
→ Fails if foo.py already exists

Good slash command:
```markdown
1. Check if foo.py exists. If not, create it.
2. Update code...
```
→ Can run multiple times safely

### Practice 2: Escape Hatches

Always give the user a way out.

```markdown
## Steps
1. Run tests
2. If tests fail, ASK THE USER: 'Tests failed. Debug or abort?'
   - Don't automatically keep trying
   - Let the user decide
```

### Practice 3: Logging/Tracing

Tell the user what's happening.

```markdown
## Steps
1. Print: 'Running tests...'
2. Run pytest
3. Print: 'Tests passed ✓ (15/15)'
```

Users should never wonder, 'Is it still working?'

### Practice 4: Version Control Integration

Always work with git.

```markdown
## Steps
1. Create a new branch: `git checkout -b feature/$FEATURE_NAME`
2. Make changes
3. Commit
4. Print: 'Changes committed to branch feature/...'
```

Never commit directly to main.

### Practice 5: Test Before Commit

```markdown
## Safety
- MUST run tests before committing
- If tests fail, create a branch but don't push
- If tests pass, offer to push
```"

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Vague Slash Commands

**Bad:**
```markdown
# Fix Bugs
Fix all the bugs in the code.
```

**Why it's bad:**
- 'All bugs' is undefined
- No steps
- No safety checks

**Good:**
```markdown
# Fix Linting Errors

Run ruff and fix auto-fixable linting errors.

## Steps
1. Run: `ruff check . --fix`
2. Show the fixes made
3. Ask user if they want to commit
```

### Pitfall 2: No Safety Guardrails

**Bad:**
```markdown
1. Delete all test files
2. Rewrite from scratch
```

**Why it's bad:**
- Destructive
- No confirmation
- No backup

**Good:**
```markdown
1. ASK USER: 'This will delete test files. Continue? (y/n)'
2. If yes, create a backup branch
3. Delete and rewrite
```

### Pitfall 3: Trying to Do Too Much

**Bad:**
```markdown
# Do Everything
Add a feature, refactor the database, deploy to production, and write a blog post.
```

**Why it's bad:**
- Too many responsibilities
- Hard to debug if something fails
- Not reusable

**Good:**
Create **four separate slash commands:**
- `/add-feature`
- `/refactor-db`
- `/deploy`
- `/write-post`

Then chain them if needed:
```
/add-feature login
/deploy staging
```

### Pitfall 4: Not Using CLAUDE.md

**Symptom:** You keep telling Claude the same things every conversation.

**Solution:** If you find yourself typing the same instructions 3+ times, **put them in CLAUDE.md.**

---

## What You'll Build This Week

"For your assignment, you'll create **at least 2 automations** for the starter app.

**Starter app recap:**
- FastAPI backend
- Notes and action items
- Basic CRUD operations
- Minimal tests

**Your job:**
- Pick 2+ workflows that are currently manual
- Automate them with slash commands, CLAUDE.md, SubAgents, or MCP

**Example automations:**
1. **`/add-endpoint`** - Add a new API route with tests and docs
2. **`/refactor-safe`** - Rename a module, update imports, verify tests pass
3. **TestAgent + CodeAgent** - TDD workflow for new features
4. **DocsAgent** - Auto-update API.md when OpenAPI changes
5. **`/db-migrate`** - Update schema, migrate data, run tests

**Then use your automations to improve the app:**
- Add the features from docs/TASKS.md
- Document your before/after workflows
- Show how much time you saved"

---

## Conclusion: The Autonomous Future

"Three years ago, developers wrote every line of code by hand.

Two years ago, GitHub Copilot suggested completions.

One year ago, ChatGPT wrote functions on request.

Today, Claude Code can **autonomously** build features from a single command.

**The trend is clear:** AI is moving from 'assistant' to 'teammate.'

But here's the key insight: **The best developers won't be the ones who write the most code. They'll be the ones who design the best workflows.**

Your value isn't in typing. It's in:
- Knowing what to build
- Designing robust systems
- Creating automations that others can use
- Ensuring quality and safety

This week, you're learning to **architect AI workflows**—a skill that will be invaluable as AI becomes more capable.

**Remember:** You're not learning to use a tool. You're learning to **design autonomous systems.**

That's the modern software developer.

See you in the assignment."

---

## Additional Resources

- **Claude Code Best Practices:** https://www.anthropic.com/engineering/claude-code-best-practices
- **SubAgents Documentation:** https://docs.anthropic.com/en/docs/claude-code/sub-agents
- **Slash Commands Guide:** Check `.claude/commands/` examples in your repo
- **CLAUDE.md Examples:** Search GitHub for "CLAUDE.md" to see real-world examples

---

## Quick Reference: Decision Matrix

**When should I use each feature?**

| Use Case | Best Feature | Why |
|----------|--------------|-----|
| Repeatable multi-step task | Slash command | Can trigger with one command |
| Project-wide coding standards | CLAUDE.md | Always active, no trigger needed |
| Complex task with distinct roles | SubAgents | Specialized focus, better results |
| Access external data/APIs | MCP server | Standardized protocol, reusable |
| One-time custom request | Regular Claude | No need to create automation |
