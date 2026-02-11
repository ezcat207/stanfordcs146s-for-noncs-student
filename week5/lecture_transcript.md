# Lecture Transcript: Agentic Development with Warp

**Date:** Week 5 - Fall 2025
**Topic:** Multi-Agent Workflows and Warp Drive Automation
**Target Audience:** Complete beginners (18-year-olds with no CS background)

---

## Introduction: From Single Agent to Multi-Agent Orchestration

"Welcome to Week 5! Last week, you learned how to build automations with Claude Code—slash commands, CLAUDE.md files, and SubAgents.

This week, we're taking it to the next level: **parallel multi-agent development.**

Imagine you're working on a feature that requires:
- Writing backend code
- Writing frontend code
- Writing tests
- Updating documentation

**Old way:** Do these one at a time, sequentially. Total time: 2 hours.

**New way:** Spawn 4 AI agents, each working on one task simultaneously. Total time: 30 minutes.

That's **parallel multi-agent development**—and that's what Warp enables."

---

## The Big Picture: What Is Warp?

### Warp Is Not Just a Terminal

"Most of you have used a terminal before. You type commands, press Enter, see output. Warp looks like a terminal, but it's fundamentally different:

**Traditional terminal (bash, zsh):**
- You type commands one at a time
- No AI assistance
- No collaboration features
- Linear workflow

**Warp (AI-powered terminal):**
- AI can suggest and execute commands
- Multiple AI agents can work in parallel
- Built-in collaboration features
- Concurrent workflows

**Analogy:**

Traditional terminal = Calculator
- You do one calculation at a time

Warp = Spreadsheet
- Multiple calculations happening simultaneously
- Cells reference each other
- Real-time collaboration

**Warp isn't just faster—it enables workflows that were impossible before.**"

### Key Warp Features We'll Use This Week

"Warp has several features designed for agentic development:

1. **Warp Drive** - Shareable prompts, rules, and configurations
2. **Multi-Tab AI Agents** - Spawn multiple AI agents in different tabs
3. **Blocks** - Command outputs are structured, not just text
4. **Workflows** - Save and share command sequences
5. **MCP Integration** - Connect to Model Context Protocol servers

**This week focuses on:**
- **Warp Drive** (Part A of assignment)
- **Multi-Agent Workflows** (Part B of assignment)"

---

## Part A: Warp Drive - Shareable Automation

### What Is Warp Drive?

"Warp Drive is like 'dotfiles for AI agents'—a way to share configurations, prompts, and rules across projects and team members.

**Components:**

1. **Saved Prompts** - Reusable instructions for common tasks
2. **Rules** - Project-specific guidelines that always apply
3. **MCP Servers** - External tools and data sources
4. **Workflows** - Multi-step command sequences

**Think of it as:**
- Saved Prompts = Recipe cards
- Rules = House rules (always follow these)
- MCP Servers = Kitchen appliances (tools you can use)
- Workflows = Multi-course meal plans"

### Saved Prompts: Your Personal Automation Library

"A saved prompt is a reusable instruction you can trigger with a shortcut.

**Example: Test Coverage Prompt**

Instead of typing this every time:
```
Run pytest with coverage for the notes router.
Show me which lines aren't covered.
For any lines below 80% coverage, suggest specific test cases.
Generate the HTML report and tell me where to find it.
```

You save it as a prompt named `test-coverage` and trigger it with a click or keyboard shortcut.

**Why this matters:**
- ✅ Consistency - Same analysis every time
- ✅ Speed - One click vs typing 4 sentences
- ✅ Sharing - Team members can use the same prompt
- ✅ Version control - Prompts can be tracked in git

**Anatomy of a Good Saved Prompt:**

```markdown
Name: Test Coverage Analysis

Prompt:
Run pytest with coverage for {target}.
Show results categorized by coverage level:
- Excellent (≥90%)
- Good (80-89%)
- Needs work (<80%)

For files below 80%, list specific untested lines and suggest test scenarios.

Generate HTML report and provide the file path.

Ask if I want you to write tests for the lowest coverage file.

Variables:
- {target}: Test file or directory (default: backend/tests/)
```

**Notice:**
- Clear, specific steps
- Structured output format
- Variable support `{target}`
- Offers next steps

This is like a slash command, but in Warp instead of Claude Code."

### Rules: Always-Active Project Context

"Rules are like CLAUDE.md but for Warp—always-active instructions that apply to every AI interaction.

**Example Rule for our starter app:**

```yaml
name: FastAPI Project Standards
description: Coding standards for this FastAPI application
rules:
  - Always use type hints for function parameters and returns
  - Use Pydantic schemas for validation, not manual checks
  - Return proper HTTP status codes (200, 201, 204, 400, 404)
  - Never use print() - use proper logging
  - Run 'make test' before suggesting commits
  - Format code with 'make format' before finishing
  - Tests live in backend/tests/
  - Follow TDD: write tests before implementation
```

**How it works:**
When you ask Warp AI to add an endpoint, it automatically:
- Uses type hints ✅
- Uses Pydantic for validation ✅
- Returns correct status codes ✅
- Runs tests ✅
- Formats code ✅

**You don't have to tell it these things every time.**

**Difference from Saved Prompts:**

| Saved Prompts | Rules |
|---------------|-------|
| Triggered manually | Always active |
| Specific task | General guidelines |
| 'Run this command' | 'When doing X, remember Y' |
| Like a macro | Like a policy |"

### MCP Servers in Warp

"You already built MCP servers in Week 3. This week, you **integrate them into Warp.**

**Example workflow:**

Week 3: You built a GitHub Issues MCP server

Week 5: You use it in Warp to automate issue creation

**How it works:**

1. Configure MCP server in Warp settings:
```json
{
  "mcpServers": {
    "github-issues": {
      "command": "python",
      "args": ["/path/to/github_mcp_server.py"]
    }
  }
}
```

2. Create a Warp Drive prompt that uses the MCP server:
```markdown
Name: Create Issue from Error

Prompt:
When I paste an error message, extract:
- Error type
- File and line number
- Error message

Then use the GitHub MCP server to create an issue with:
- Title: "[Bug] {error_type} in {file}"
- Body: Error details and stack trace
- Labels: bug, automated

Return the issue URL.
```

3. Usage:
- Paste error message
- Trigger prompt
- Issue created automatically

**This combines:**
- Your custom MCP server (from Week 3)
- Warp's AI capabilities
- Automation through saved prompts

**Powerful combination.**"

---

## Part B: Multi-Agent Workflows

### The Parallel Development Problem

"Here's a scenario every developer faces:

You need to add a 'tags' feature to the app. This requires:
1. **Backend:** Add Tag model and endpoints
2. **Frontend:** Add tag UI components
3. **Tests:** Write backend tests
4. **Docs:** Update API documentation

**Sequential approach (traditional):**
```
Hour 1: Work on backend
Hour 2: Work on frontend
Hour 3: Write tests
Hour 4: Update docs
Total: 4 hours
```

**Parallel approach (multi-agent):**
```
Minute 1-30:
- Agent 1 works on backend (Tab 1)
- Agent 2 works on frontend (Tab 2)
- Agent 3 writes tests (Tab 3)
- Agent 4 updates docs (Tab 4)

All four working simultaneously.
Total: 30 minutes
```

**Challenge:** How do we coordinate 4 agents working on the same codebase without them stepping on each other's toes?

**That's what multi-agent workflows solve.**"

### How Multi-Agent Workflows Work in Warp

"Warp allows you to spawn multiple AI agents in different tabs, each with its own context and workspace.

**Architecture:**

```
Tab 1: Backend Agent
- Working directory: week5/
- Role: Implement backend logic
- Tools: Can modify backend/ files only
- Git branch: feature/tags-backend

Tab 2: Frontend Agent
- Working directory: week5/
- Role: Implement UI components
- Tools: Can modify frontend/ files only
- Git branch: feature/tags-frontend

Tab 3: Test Agent
- Working directory: week5/
- Role: Write comprehensive tests
- Tools: Can modify backend/tests/ only
- Git branch: feature/tags-tests

Tab 4: Docs Agent
- Working directory: week5/
- Role: Update documentation
- Tools: Can modify docs/ only
- Git branch: feature/tags-docs
```

**Key insight:** Each agent works in its own **git branch**. No conflicts. They work in parallel, then you merge.

**This uses `git worktree`** (advanced git feature that lets you have multiple branches checked out simultaneously)."

### Git Worktree: The Secret Sauce

"Git worktree is how we let multiple agents work on the same repo without conflicts.

**Normal git:**
```bash
# You can only have one branch checked out at a time
git checkout feature-a
# Do work
git checkout feature-b
# Do different work
# Can't work on both simultaneously
```

**With git worktree:**
```bash
# Create separate working directories for each branch
git worktree add ../week5-backend feature/tags-backend
git worktree add ../week5-frontend feature/tags-frontend
git worktree add ../week5-tests feature/tags-tests
git worktree add ../week5-docs feature/tags-docs

# Now you have 4 separate directories:
week5/                 # Main directory (main branch)
week5-backend/         # feature/tags-backend branch
week5-frontend/        # feature/tags-frontend branch
week5-tests/           # feature/tags-tests branch
week5-docs/            # feature/tags-docs branch
```

**Each Warp tab works in a different directory:**
- Tab 1: `cd week5-backend/`
- Tab 2: `cd week5-frontend/`
- Tab 3: `cd week5-tests/`
- Tab 4: `cd week5-docs/`

**No conflicts. Each agent has its own isolated workspace.**

**Analogy:**

Without worktree:
- 4 chefs, 1 kitchen
- They keep bumping into each other

With worktree:
- 4 chefs, 4 kitchens
- Each works independently
- Results combined at the end"

### Multi-Agent Workflow: Step-by-Step

"Let's walk through a complete multi-agent workflow.

**Task:** Implement tags feature (backend + frontend + tests + docs)

#### Step 1: Set Up Worktrees

In your main Warp tab:
```bash
cd week5/

# Create feature branches
git branch feature/tags-backend
git branch feature/tags-frontend
git branch feature/tags-tests
git branch feature/tags-docs

# Create worktrees
git worktree add ../week5-backend feature/tags-backend
git worktree add ../week5-frontend feature/tags-frontend
git worktree add ../week5-tests feature/tags-tests
git worktree add ../week5-docs feature/tags-docs
```

#### Step 2: Open Multiple Warp Tabs

Create 4 tabs in Warp:
- Tab 1: Backend
- Tab 2: Frontend
- Tab 3: Tests
- Tab 4: Docs

#### Step 3: Assign Tasks to Agents

**Tab 1 (Backend Agent):**
```
You are the Backend Agent.
Role: Implement the tags feature backend.

Tasks:
1. Add Tag model to backend/app/models.py
2. Add tag schemas to backend/app/schemas.py
3. Create backend/app/routers/tags.py with endpoints:
   - GET /tags (list all)
   - POST /tags (create)
   - DELETE /tags/{id} (delete)
   - POST /notes/{id}/tags (attach tag to note)
   - DELETE /notes/{id}/tags/{tag_id} (detach)
4. Run make test to verify no existing tests break
5. When done, commit to feature/tags-backend

Working directory: week5-backend/
Start now.
```

**Tab 2 (Frontend Agent):**
```
You are the Frontend Agent.
Role: Implement tags UI.

Tasks:
1. Create frontend/components/TagChip.js (display a tag)
2. Create frontend/components/TagInput.js (add tags to notes)
3. Update frontend/components/NoteCard.js to display tags
4. Add tag filtering to the notes list
5. Style components with basic CSS

Working directory: week5-frontend/
Start now.
```

**Tab 3 (Test Agent):**
```
You are the Test Agent.
Role: Write comprehensive tests for tags.

Tasks:
1. Create backend/tests/test_tags.py
2. Test all tag endpoints:
   - Happy paths
   - Error cases (404, validation errors)
   - Edge cases (duplicate tags, attaching same tag twice)
3. Test many-to-many relationship behavior
4. Aim for >90% coverage on tags router

Working directory: week5-tests/
Start now.
```

**Tab 4 (Docs Agent):**
```
You are the Docs Agent.
Role: Document the tags feature.

Tasks:
1. Update docs/API.md with tag endpoints
2. Add examples for each endpoint (request/response)
3. Update docs/TASKS.md to mark Task 5 as complete
4. Add a section to README.md explaining tags feature

Working directory: week5-docs/
Start now.
```

#### Step 4: Let Agents Work in Parallel

All 4 agents start working **simultaneously**.

**What you see:**

Tab 1 (Backend):
```bash
Creating backend/app/models.py changes...
[Agent modifies models.py]
Adding Tag model...
Creating many-to-many relationship...
Done. Running tests...
All tests pass ✓
```

Tab 2 (Frontend):
```bash
Creating TagChip component...
[Agent creates TagChip.js]
Styling with CSS...
Testing component...
Done. Component works ✓
```

Tab 3 (Tests):
```bash
Creating test_tags.py...
Writing test_create_tag...
Writing test_attach_tag_to_note...
Running tests...
All 12 tests pass ✓
Coverage: 95% ✓
```

Tab 4 (Docs):
```bash
Updating API.md...
Adding tag endpoints...
Adding examples...
Done. Documentation updated ✓
```

**All happening at once.**

#### Step 5: Monitor Progress

You can switch between tabs to check on each agent:
- Backend: 80% done
- Frontend: 60% done
- Tests: 90% done
- Docs: 100% done ✓

#### Step 6: Merge Results

Once all agents finish:

```bash
cd week5/

# Merge backend
git merge feature/tags-backend

# Merge frontend
git merge feature/tags-frontend

# Merge tests
git merge feature/tags-tests

# Merge docs
git merge feature/tags-docs

# Run full test suite
make test

# If all tests pass, you're done!
```

**Total time:** ~30 minutes (vs 4 hours sequentially)

**Success rate:** Higher (specialized agents make fewer mistakes in their domain)"

---

## Coordination Strategies

### Strategy 1: Independent Tasks (Easiest)

"Assign tasks that don't depend on each other.

**Good:**
- Agent 1: Add backend endpoint A
- Agent 2: Add frontend component B
- Agent 3: Write tests for existing code
- Agent 4: Update documentation

These can happen in parallel with no dependencies.

**Bad:**
- Agent 1: Add backend endpoint A
- Agent 2: Add frontend component that calls endpoint A
- Problem: Agent 2 depends on Agent 1 finishing first

**Fix:** Only parallelize truly independent work."

### Strategy 2: Interface-First Design

"Define interfaces before parallel work.

**Workflow:**

1. **You (main tab):** Define API contract
```python
# backend/app/schemas.py
class TagCreate(BaseModel):
    name: str

class TagRead(BaseModel):
    id: int
    name: str
```

2. **Backend Agent:** Implement this interface
3. **Frontend Agent:** Use this interface (even if backend isn't done yet)

**Benefits:**
- Agents can work in parallel
- Frontend doesn't wait for backend
- Clear contract prevents misunderstandings"

### Strategy 3: Continuous Integration

"Have one agent continuously merge and test.

**Setup:**

- Tabs 1-3: Feature agents (parallel work)
- Tab 4: Integration agent (continuous merging)

**Integration Agent's job:**
```
Every 10 minutes:
1. Merge all feature branches into integration branch
2. Run full test suite
3. If conflicts or test failures:
   - Report to user
   - Pause feature agents
   - Resolve issues
4. If all good:
   - Continue
```

**This catches integration issues early.**"

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Agents Modifying the Same File

"If two agents try to modify `models.py` simultaneously, you'll get merge conflicts.

**Solution:**
- **Plan ahead:** Assign file ownership
  - Agent 1 owns backend/app/routers/tags.py
  - Agent 2 owns backend/app/routers/notes.py
- **Use worktrees:** Each agent works in separate directory
- **Merge frequently:** Don't let branches diverge too much"

### Pitfall 2: Circular Dependencies

"Agent 1 waits for Agent 2. Agent 2 waits for Agent 1. Deadlock.

**Example:**
- Backend Agent: 'I need the frontend to tell me what fields to return'
- Frontend Agent: 'I need the backend to tell me what fields are available'

**Solution:**
- **You define the interface** before spawning agents
- Give both agents a shared schema/contract"

### Pitfall 3: Lost Context

"Agent forgets what it's working on after several steps.

**Solution:**
- **Saved prompts with clear role definition**
- **Reminder messages:** Periodically remind agent of its role
- **Scoped permissions:** Limit agent's tool access to its domain"

### Pitfall 4: Over-Parallelization

"Spawning 10 agents for 10 tiny tasks = chaos and coordination overhead.

**Rule of thumb:**
- 2-4 agents: Sweet spot
- 5-8 agents: Advanced (only if tasks are truly independent)
- 9+ agents: Diminishing returns (coordination overhead > time savings)

**Better:**
- 4 agents on 4 major features ✅
- 10 agents on 10 tiny bug fixes ❌ (just do these sequentially)"

---

## Practical Examples

### Example 1: Warp Drive Saved Prompt

**Name:** API Endpoint Generator

**Prompt:**
```markdown
Create a new FastAPI endpoint with TDD approach.

Inputs from user:
- HTTP method (GET, POST, PUT, DELETE)
- Path (e.g., /notes/{id}/archive)
- Description of what the endpoint does

Steps:
1. Determine which router file based on path prefix
   - /notes → backend/app/routers/notes.py
   - /action-items → backend/app/routers/action_items.py

2. Create test file if it doesn't exist:
   - backend/tests/test_<router>.py

3. Write 3 test cases:
   - Happy path
   - 404 error case
   - Validation error case

4. Run tests (they should fail - no implementation yet)

5. Implement the endpoint with:
   - Type hints
   - Pydantic schema validation
   - Proper status codes
   - Docstring

6. Run tests until they pass

7. Run make format && make lint

8. Update docs/API.md with endpoint documentation

9. Show summary of changes and next steps (commit message suggestion)

Rules to follow:
- Use the project rules defined in Warp
- Never commit automatically
- Always ask before destructive actions
```

**Usage:**
1. Save this as a Warp Drive prompt
2. Share with team
3. Anyone can trigger it with one click
4. Consistent endpoint creation across the team

### Example 2: Multi-Agent Task Distribution

**Scenario:** Complete Tasks 2, 3, and 4 from TASKS.md simultaneously

**Setup:**

```bash
# Main tab
git worktree add ../week5-task2 feature/search-pagination
git worktree add ../week5-task3 feature/notes-crud
git worktree add ../week5-task4 feature/action-items-filters
```

**Agent 1 (Tab 1): Search & Pagination**
```
Task: Implement GET /notes/search with pagination and sorting

You are working in: week5-task2/

Steps:
1. Add query parameters to backend/app/routers/notes.py
   - q (search query)
   - page (default: 1)
   - page_size (default: 10)
   - sort (created_desc | title_asc)

2. Implement SQLAlchemy query with filters and ordering

3. Return {items, total, page, page_size}

4. Write tests in backend/tests/test_notes.py

5. When done, commit to feature/search-pagination

Start now.
```

**Agent 2 (Tab 2): Notes CRUD**
```
Task: Add PUT and DELETE endpoints for notes

You are working in: week5-task3/

Steps:
1. Add PUT /notes/{id} to update title and content
2. Add DELETE /notes/{id}
3. Add validation in schemas.py (min/max lengths)
4. Write tests for success and error cases
5. When done, commit to feature/notes-crud

Start now.
```

**Agent 3 (Tab 3): Action Items Filters**
```
Task: Add filtering and bulk complete for action items

You are working in: week5-task4/

Steps:
1. Add GET /action-items?completed=true|false
2. Add POST /action-items/bulk-complete with list of IDs
3. Use transactions for bulk operations
4. Write tests covering filters and bulk behavior
5. When done, commit to feature/action-items-filters

Start now.
```

**Results:**
- All 3 tasks complete in ~20-30 minutes
- vs. 1-2 hours sequentially
- Higher quality (each agent focused on one thing)

---

## Best Practices for Multi-Agent Workflows

### 1. Start Small

"Don't jump into 4 agents on day one.

**Learning progression:**
1. Week 1: Single agent, single task
2. Week 2: 2 agents, simple tasks
3. Week 3: 3-4 agents, complex tasks
4. Week 4+: Advanced coordination"

### 2. Clear Role Definitions

"Each agent should have ONE clear responsibility.

**Bad:**
```
Agent 1: Work on the tags feature
```
Too vague. What part of tags?

**Good:**
```
Agent 1: Backend only - Implement Tag model and API endpoints
Agent 2: Frontend only - Create tag UI components
Agent 3: Tests only - Write comprehensive tests for tags
```

Clear boundaries = fewer conflicts."

### 3. Shared Contracts

"Define data structures before spawning agents.

**Create:** `schemas.py` with all Pydantic models
**Then:** Share with all agents
**Result:** Everyone agrees on data format"

### 4. Continuous Monitoring

"Don't spawn agents and walk away.

**Monitor:**
- Check each tab every 5-10 minutes
- Look for errors or stuck agents
- Ensure agents aren't interfering with each other

**Red flags:**
- Agent hasn't made progress in 10+ minutes
- Tests failing repeatedly
- Agent asking questions (means it's stuck)"

### 5. Have a Rollback Plan

"If multi-agent workflow fails:

```bash
# Abandon all worktrees
git worktree remove ../week5-task2
git worktree remove ../week5-task3
git worktree remove ../week5-task4

# Delete branches
git branch -D feature/search-pagination
git branch -D feature/notes-crud
git branch -D feature/action-items-filters

# Start over (or do it sequentially)
```

**Don't be afraid to abort and try a different approach.**"

---

## Measuring Success

### Time Savings

"Track time for both approaches:

**Sequential (traditional):**
- Task A: 45 min
- Task B: 60 min
- Task C: 30 min
- **Total: 135 min (2.25 hours)**

**Parallel (multi-agent):**
- All tasks: 50 min (includes setup and merge)
- **Total: 50 min**

**Time saved: 85 minutes (63% reduction)**"

### Quality Improvements

"Multi-agent can actually improve quality:

**Why?**
- **Specialized focus:** Each agent focuses on one thing
- **Parallel review:** Test agent catches backend bugs immediately
- **Consistent patterns:** Using saved prompts ensures consistency

**Metrics:**
- Bug count: 3 bugs (sequential) → 1 bug (multi-agent)
- Test coverage: 75% → 92%
- Code review feedback: 12 comments → 4 comments"

---

## Conclusion: The Future of Development

"Five years ago, developers wrote every line of code by hand.

Two years ago, AI started suggesting code completions.

Last week, you learned how one AI agent can build features autonomously.

This week, you're learning how **multiple AI agents can work together** to build features in parallel.

**The trend is clear:**
- More automation
- More parallelization
- More coordination

**The developer of the future** isn't the fastest coder. It's the best **agent orchestrator**—someone who can coordinate multiple AI agents to build complex systems efficiently.

**That's what you're becoming this week.**

Welcome to the future of software development."

---

## Additional Resources

- **Warp Official Site:** https://www.warp.dev/
- **Warp University:** https://www.warp.dev/university
- **Git Worktree Docs:** https://git-scm.com/docs/git-worktree
- **MCP Specification:** https://modelcontextprotocol.io/

---

## Quick Reference: Warp vs Claude Code

| Feature | Claude Code (Week 4) | Warp (Week 5) |
|---------|---------------------|---------------|
| **Environment** | VS Code extension | Standalone terminal |
| **Automation** | Slash commands (.md files) | Warp Drive prompts |
| **Context** | CLAUDE.md | Warp Rules |
| **Multi-agent** | SubAgents (sequential) | Multi-tab (parallel) |
| **Best for** | Single codebase, sequential tasks | Parallel development, terminal-heavy workflows |
| **Learning curve** | Moderate | Steeper (need git worktree) |
| **Collaboration** | Share .claude/ folder | Share Warp Drive links |
| **MCP** | Built-in support | Configure manually |

Both are powerful. Choose based on your workflow.
