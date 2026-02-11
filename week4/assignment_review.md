# Week 4 Assignment Review: Building Autonomous Coding Workflows

**Purpose:** Help you understand what makes excellent automation design and provide a self-grading framework.

**After completing your assignment, use this document to:**
1. Understand the "why" behind each requirement
2. Check your work against professional standards
3. Identify areas for improvement
4. Self-grade before submission

---

## The "Why" Behind This Assignment

### Why Build Automations Instead of Just Writing Code?

This assignment is fundamentally different from Weeks 1-3 because **the deliverable isn't code—it's workflow design.**

**Key insight:** As AI becomes more capable, your value as a developer shifts from:
- ❌ "I can write Python code fast"
- ✅ "I can design systems that use AI to write Python code fast"

**Real-world parallel:**

In the early 2000s, companies hired developers who could hand-write HTML/CSS.

In the 2010s, companies hired developers who could use frameworks (React, Vue, etc.) to build UIs faster.

In the 2020s, companies will hire developers who can **design AI workflows** that build UIs automatically.

**This assignment teaches you to be the 2020s developer.**

---

## What Graders Actually Look For

### The Evaluation Framework

Graders don't just check if your automations "work." They evaluate:

1. **Problem identification** - Did you identify a real, repetitive workflow worth automating?
2. **Design quality** - Is your automation well-structured and reusable?
3. **Documentation clarity** - Can someone else use your automation?
4. **Practical impact** - Did you actually use it to improve the app?
5. **Thoughtfulness** - Did you consider safety, errors, and edge cases?

**Not evaluated:**
- Lines of Python code written (this isn't a coding assignment)
- Complexity of the automation (simple but useful > complex but useless)
- Number of automations beyond the minimum 2 (quality > quantity)

---

## Anatomy of an Excellent Automation

### Example: Let's Break Down a Good Slash Command

**Bad version (will lose points):**
````markdown
# Test

Run tests

## Steps
1. Run pytest
````

**Why it's bad:**
- No specificity ("Run pytest" how? With what flags?)
- No error handling (what if tests fail?)
- No inputs (always runs the same way?)
- No safety rules (could run on production?)
- No expected outputs (user doesn't know what to expect)

**Excellent version (full points):**
````markdown
# Run Tests with Coverage

Executes the test suite with coverage analysis and provides actionable insights.

## Arguments
- $TARGET (optional): Specific test file or directory. If omitted, runs all tests.
  - Examples: `backend/tests/test_notes.py`, `backend/tests/`

## Steps

1. Run pytest with coverage:
   ```bash
   pytest $TARGET --cov=backend/app --cov-report=term-missing -v
   ```

2. Analyze results:
   - If tests fail: Show failing test output and STOP. Ask user: "Debug or abort?"
   - If tests pass: Continue to step 3

3. Parse coverage output and categorize files:
   - Excellent (≥90%): List files
   - Good (80-89%): List files
   - Needs work (<80%): List files WITH specific missing line numbers

4. For each file with <80% coverage:
   - Show current percentage
   - Show which lines are untested
   - Suggest specific test scenarios

5. Provide summary:
   ```
   Total Coverage: X%
   Priority files to improve: [list]
   Suggested next steps: [specific actions]
   ```

6. Ask user: "Would you like me to generate tests for the lowest coverage file?"

## Safety Rules
- Never modify application code - this is analysis only
- Never commit automatically
- Don't generate tests without explicit permission
- Create `.coverage` and `htmlcov/` artifacts (safe to delete)

## Expected Output
```
✅ All tests passed (27/27)
Total Coverage: 78%

Files needing work:
❌ backend/app/services/extract.py: 45%
   Missing: Lines 15-22 (hashtag parsing)
   Suggested test: test_extract_hashtags_empty

Would you like me to help?
```

## Rollback
No code changes made. Artifacts created:
- .coverage (can delete)
- htmlcov/ (can delete)
````

**Why it's excellent:**
- ✅ Clear purpose and scope
- ✅ Specific, executable steps
- ✅ Error handling (what if tests fail?)
- ✅ Safety guardrails (never modify code, ask before generating tests)
- ✅ Actionable output (not just numbers, but specific recommendations)
- ✅ User escape hatch (offer to help, but let user decide)
- ✅ Rollback plan documented

---

## Self-Grading Checklist

Use this before submitting:

### Part 1: Automation Design (40%)

#### For Each Automation:

**Problem Identification (10%)**
- [ ] I identified a real, repetitive workflow (not a made-up example)
- [ ] This workflow is something that happens 3+ times (worth automating)
- [ ] I can clearly explain why this was manual and time-consuming before

**Design Quality (20%)**
- [ ] Automation has a clear, single purpose (not "do everything")
- [ ] Steps are specific and executable (not vague like "run tests")
- [ ] Has error handling (what happens when things fail?)
- [ ] Has safety guardrails (won't accidentally delete/commit/deploy)
- [ ] Is idempotent (can run multiple times safely)
- [ ] Provides clear feedback at each step

**Reusability (10%)**
- [ ] Someone else could use this automation without asking me questions
- [ ] Works for multiple scenarios (not hardcoded for one specific case)
- [ ] Documentation is clear enough to onboard a new developer

---

### Part 2: Documentation Quality (30%)

**Writeup Completeness (15%)**
- [ ] Filled out every section of writeup.md (no TODOs remaining)
- [ ] Cited the Claude Code best practices doc in "Design inspiration"
- [ ] Explained design clearly (goals, inputs, outputs, steps)
- [ ] Included exact commands for how to run each automation
- [ ] Provided before/after comparison with real time estimates

**Clarity and Specificity (15%)**
- [ ] Examples are concrete (not "run the automation to do a thing")
- [ ] Includes actual commands I ran (copy-pasteable)
- [ ] Time savings are realistic and explained (not "saves 99% time")
- [ ] Workflow descriptions are detailed enough to reproduce

---

### Part 3: Practical Impact (20%)

**Actually Used the Automations (10%)**
- [ ] I used each automation to enhance the starter application
- [ ] I can point to specific code changes made using the automation
- [ ] I completed at least one task from docs/TASKS.md with the automation
- [ ] The before/after is based on real experience, not hypothetical

**Measurable Improvement (10%)**
- [ ] I documented time saved (with realistic estimates)
- [ ] I documented quality improvement (tests added, docs updated, etc.)
- [ ] I explained how the starter app is better now than before
- [ ] The improvements are verifiable (grader can see the changes)

---

### Part 4: Thoughtfulness (10%)

**Safety and Error Handling (5%)**
- [ ] Automations have rollback plans or are non-destructive
- [ ] Error cases are handled (what if API call fails? tests fail?)
- [ ] Safety rules prevent destructive actions (no auto-delete, auto-deploy)
- [ ] User has escape hatches (can abort, confirm, or manual intervene)

**Insight and Reflection (5%)**
- [ ] Writeup explains "why" not just "what"
- [ ] I identified limitations of my automations
- [ ] I suggested future improvements
- [ ] I demonstrated understanding of automation trade-offs

---

## Common Mistakes and How to Fix Them

### Mistake 1: Automation That's Too Complex

**Symptom:**
Your slash command tries to do 10 different things in one workflow.

**Example:**
````markdown
# Do Everything
1. Add a feature
2. Write tests
3. Update docs
4. Refactor the codebase
5. Deploy to production
6. Send Slack notification
7. Update JIRA ticket
````

**Why it's bad:**
- Hard to debug when something fails
- Not reusable (only works in this exact scenario)
- Violates single-responsibility principle

**Fix:**
Create **multiple focused automations** that do one thing well:
- `/add-endpoint` - Just add an endpoint with TDD
- `/deploy` - Just deploy
- `/update-docs` - Just update documentation

Then compose them:
```
/add-endpoint POST /notes/archive "Archives a note"
/update-docs
/deploy staging
```

**Red flag to watch for:** Your automation has >7 steps in the workflow. Consider splitting it.

---

### Mistake 2: Vague or Generic Documentation

**Symptom:**
Your writeup sounds like it could apply to any project, not specifically yours.

**Bad writeup example:**
```markdown
b. Design of each automation

I created a slash command that adds endpoints. It writes tests and then writes code. It's useful because it saves time.
```

**Why it's bad:**
- Doesn't explain the specific workflow
- No mention of inputs/outputs
- No concrete steps
- Could be copy-pasted from another assignment

**Good writeup example:**
```markdown
b. Design of each automation

**Goal:** Automate the complete workflow for adding a FastAPI endpoint using TDD.

**Inputs:**
- $METHOD: HTTP verb (GET, POST, PUT, DELETE)
- $PATH: Endpoint route (e.g., /notes/{id}/archive)
- $DESCRIPTION: Brief explanation of what the endpoint does

**Steps:**
1. Determine target router file based on $PATH prefix
   - /notes → backend/app/routers/notes.py
   - /action-items → backend/app/routers/action_items.py
2. Create/update test file at backend/tests/test_<router>.py
3. Write 3 test cases: happy path, error case, edge case
4. Run pytest - tests should fail (TDD red phase)
5. Implement the endpoint in the router file
6. Run pytest - tests should pass (TDD green phase)
7. Run make format && make lint
8. Update docs/API.md with endpoint specification
9. Show summary of changes and test results

**Outputs:**
- Test file with ≥3 comprehensive test cases
- Implemented endpoint with type hints and docstring
- Updated API documentation
- All tests passing, no lint errors
```

**Fix:** Be **extremely specific**. Pretend you're explaining this to someone who has never seen your project.

---

### Mistake 3: Not Actually Using the Automation

**Symptom:**
You built an automation but in the writeup, you don't have concrete examples of using it.

**Red flag in writeup:**
```markdown
e. How you used the automation to enhance the starter application

I would use this automation to add endpoints if I needed to add endpoints.
```

**Why it's bad:**
- "Would use" = didn't actually use it
- No concrete example
- No proof it works
- Grader can't verify the impact

**Fix:**
**Actually use your automation** for a real task. Document it:

```markdown
e. How you used the automation to enhance the starter application

I used the `/add-endpoint` automation to complete Task 2 from docs/TASKS.md:
"Add search endpoint for notes."

**What I did:**
1. Ran: `/add-endpoint GET /notes/search "Search notes by query string"`

2. The automation:
   - Created test_search_notes() in backend/tests/test_notes.py with 4 test cases:
     * test_search_notes_exact_match
     * test_search_notes_partial_match
     * test_search_notes_case_insensitive
     * test_search_notes_empty_query
   - Implemented the search endpoint in backend/app/routers/notes.py
   - All tests passed ✓
   - Updated docs/API.md with endpoint documentation

3. Manual verification:
   - Tested at http://localhost:8000/docs
   - Searched for "meeting" - returned 3 matching notes
   - Verified case-insensitive search worked

**Files changed:**
- backend/app/routers/notes.py (+15 lines)
- backend/tests/test_notes.py (+32 lines)
- docs/API.md (+22 lines)

**Time comparison:**
- Manual workflow (estimated): ~30 minutes
- With automation (actual): 3 minutes 45 seconds
- Time saved: ~26 minutes
```

**Notice:** Concrete commands, specific files, real time measurements, verifiable changes.

---

### Mistake 4: No Safety Guardrails

**Symptom:**
Your automation does destructive things without confirmation.

**Bad automation:**
````markdown
# Refactor

1. Delete all files in backend/app/
2. Rewrite from scratch
3. Commit changes
````

**Why it's terrifying:**
- Deletes code without backup
- No confirmation step
- Auto-commits (user can't review)
- No rollback plan

**Fix:**
Add **confirmations and safety checks**:

````markdown
# Refactor Module

## Steps

1. STOP and ask user:
   "This will rename <old> to <new> and update all imports.
    Continue? (y/n)"

2. If user says "no" - EXIT immediately

3. If user says "yes":
   - Create a backup branch: git checkout -b backup-refactor-$(date +%s)
   - Record current state: git add . && git commit -m "pre-refactor snapshot"
   - Switch back: git checkout -

4. Perform the refactoring

5. Run tests: make test
   - If tests fail: STOP and show errors
   - Ask: "Tests failed. Revert changes? (y/n)"

6. If tests pass:
   - Show summary of changes
   - Do NOT commit automatically
   - Tell user: "Review changes, then commit manually"

## Safety Rules
- ALWAYS create backup branch before making changes
- ALWAYS run tests before declaring success
- NEVER commit automatically - let user review
- NEVER delete files without user confirmation
````

**Golden rule:** If an action is **irreversible** or **potentially destructive**, ask first.

---

### Mistake 5: Ignoring Error Cases

**Symptom:**
Your automation assumes everything works perfectly.

**Bad:**
````markdown
# Add Endpoint

1. Write tests
2. Implement endpoint
3. Done!
````

**What could go wrong:**
- Tests fail to run (pytest not installed?)
- Endpoint already exists (name collision?)
- User provides invalid input (METHOD = "ASDF"?)
- Linting fails (code doesn't meet standards?)

**Fix:**
**Handle each error case explicitly**:

````markdown
# Add Endpoint

1. Validate inputs:
   - If $METHOD not in [GET, POST, PUT, DELETE]: Ask user to provide valid method
   - If $PATH doesn't start with '/': Ask user to fix path
   - If $DESCRIPTION is empty: Ask user to provide description

2. Check if endpoint already exists:
   - Search router file for $PATH
   - If found: Ask "Endpoint exists. Overwrite? (y/n)"

3. Write tests
   - If test file doesn't exist: Create it with proper structure
   - If tests already exist: Add new tests without deleting old ones

4. Run tests:
   - If pytest command fails: "pytest not installed. Run: pip install pytest"
   - If tests don't fail (expected): "Warning: Tests should fail before implementation. Check test logic."
   - If tests fail (expected): Continue

5. Implement endpoint
   - Use type hints
   - Include docstring

6. Run tests again:
   - If tests pass: Continue
   - If tests fail:
     * Show error output
     * Ask: "Tests failed. Options: (a) Let me debug (b) I'll fix manually"
     * If (a): Analyze error and fix implementation
     * If (b): Exit and let user fix

7. Run linting:
   - If lint errors: Show errors and STOP
   - Don't auto-fix - let user decide

8. Success! Show summary
````

**Rule of thumb:** For each step, ask "What could go wrong here?" and handle it.

---

## What Makes a Great CLAUDE.md

Many students struggle with CLAUDE.md because it's not "code" - it's documentation. Here's what makes an excellent one:

### Excellent CLAUDE.md Checklist

**Structure (Organization)**
- [ ] Clear sections with descriptive headings
- [ ] Table of contents or quick navigation
- [ ] Scannable (can find info in <10 seconds)

**Project Context (The Basics)**
- [ ] Explains what the project is (in 1-2 sentences)
- [ ] Shows directory structure with explanations
- [ ] Documents how to run, test, and deploy
- [ ] Lists access points (URLs, API docs)

**Standards and Conventions**
- [ ] Coding style (black, ruff, type hints)
- [ ] API patterns (status codes, error handling)
- [ ] Database patterns (SQLAlchemy usage)
- [ ] Commit message format
- [ ] Testing requirements

**Safety Rules (Critical)**
- [ ] DO list (what Claude should always do)
- [ ] DO NOT list (what Claude should never do)
- [ ] Explanation of why (not just rules)

**Common Workflows**
- [ ] How to add a new endpoint (step-by-step)
- [ ] How to modify existing code
- [ ] How to refactor safely
- [ ] How to debug common issues

**Tool Integration**
- [ ] Documents available slash commands (if any)
- [ ] Explains when to use which automation
- [ ] References other documentation

### Example: DO vs DO NOT Sections

**Bad (too vague):**
```markdown
## DO
- Write good code
- Test your code
- Follow standards
```

**Good (specific and actionable):**
```markdown
## DO ✅
- ✅ **Write tests before implementing features (TDD approach)**
  Example: Write test_create_note first, then implement create_note
  Why: Catches bugs early, ensures code is testable

- ✅ **Run `make test` before every commit**
  Command: make test
  Why: Prevents broken code from being committed

- ✅ **Use type hints on all function parameters and return types**
  Example: def create_note(title: str, content: str) -> Note:
  Why: Catches type errors at development time, self-documenting

## DO NOT ❌
- ❌ **Never commit code with failing tests**
  Why: Broken tests mean broken code
  If tempted: Fix the tests or the code, don't skip

- ❌ **Never delete the database without backing up important data**
  Safe command: cp data/db.sqlite data/db.sqlite.backup
  Destructive command: rm data/db.sqlite
  Why: Data loss is permanent

- ❌ **Never skip pre-commit hooks**
  Wrong: git commit --no-verify
  Right: Fix the lint errors, then commit
  Why: Hooks enforce code quality standards
```

**Notice:**
- ✅ Specific commands provided
- ✅ Examples shown
- ✅ "Why" explained (not just rules)
- ✅ Actionable (can follow immediately)

---

## Evaluating Your "Before vs After"

The before/after comparison is where you demonstrate impact. Here's how to make it compelling:

### Weak Before/After (Loses Points)

```markdown
d. Before vs. after

Before: It took a long time to add endpoints

After: Now it's fast with my automation

Saves time: A lot
```

**Problems:**
- Vague ("long time", "fast", "a lot")
- No specific steps
- No measurable improvement
- Sounds made-up

### Strong Before/After (Full Points)

```markdown
d. Before vs. after

**Before (Manual Workflow):**

Time per endpoint: ~30-45 minutes

Detailed steps:
1. Open routers/notes.py in editor (manually navigate) - 30 sec
2. Think about what tests to write - 5 min
3. Open tests/test_notes.py - 30 sec
4. Write test cases (often incomplete) - 10 min
5. Run pytest backend/tests/test_notes.py::test_new - 20 sec
6. Debug test failures - 5 min
7. Implement the endpoint - 8 min
8. Run tests again - 20 sec
9. Fix implementation bugs - 5 min
10. Remember to format: make format - 1 min
11. Remember to lint: make lint - 1 min
12. Fix linting issues - 2 min
13. Forget about docs, push broken docs - 0 min
14. Realize docs are broken after PR review - next day
15. Update docs/API.md - 5 min
16. Create PR - 2 min

**Total:** 45 minutes
**Success rate (no errors):** ~60%
**Test coverage:** 70% (sometimes forget edge cases)
**Documentation completeness:** 50% (often forget)

**After (Automated with `/add-endpoint`):**

Time per endpoint: ~3-5 minutes

Detailed steps:
1. Type: `/add-endpoint POST /notes/{id}/archive "Archives a note"` - 10 sec
2. Claude executes 8-step workflow automatically - 3 min
3. Review changes - 1 min
4. Commit - 30 sec

**Total:** 5 minutes
**Success rate (no errors):** ~95%
**Test coverage:** 100% (automation enforces comprehensive tests)
**Documentation completeness:** 100% (automation updates docs)

**Improvement:**
- Time saved: 40 minutes per endpoint (89% reduction)
- If I add 10 endpoints/week: 400 minutes = 6.7 hours saved per week
- Quality improvement:
  * Test coverage: 70% → 100%
  * Docs completeness: 50% → 100%
  * First-attempt success: 60% → 95%
- Consistency: Every endpoint follows exact same pattern
```

**Why this is excellent:**
- ✅ Specific time estimates for each step
- ✅ Real numbers (not "a lot faster")
- ✅ Explains problems with old workflow
- ✅ Quantifies quality improvements (not just time)
- ✅ Shows compound impact (weekly savings)
- ✅ Believable and verifiable

---

## Red Flags That Will Lose Points

Watch out for these in your submission:

### Red Flag 1: Hypothetical Usage

```markdown
e. How you used the automation

I would use this to add endpoints when I need to add endpoints in the future.
```

**Fix:** Actually use it NOW for a real task.

---

### Red Flag 2: Copy-Pasted Examples

If your writeup sounds suspiciously similar to the assignment examples, graders will notice.

**Instead:** Use the examples as inspiration, but make it your own:
- Different API endpoint
- Different use case
- Your own workflow
- Your own time estimates

---

### Red Flag 3: Unrealistic Time Savings

```markdown
Before: 5 hours per endpoint
After: 10 seconds per endpoint
Time saved: 99.9%
```

**Fix:** Be realistic. Most automations save 50-80%, not 99%.

---

### Red Flag 4: No Safety Considerations

If your automation has no "Safety Rules" or "Rollback" section, it's incomplete.

**Fix:** Think about:
- What could go wrong?
- How do we prevent it?
- How do we undo it if it happens?

---

### Red Flag 5: TODO Still in Writeup

```markdown
a. Design inspiration
> TODO
```

**This is an auto-fail.** Graders stop reading if TODOs remain.

---

## Rubric Decoder: What Graders Actually Mean

Let's translate the grading rubric into plain English:

### "Automation Functionality" (40%)

**What graders check:**
1. **Does it actually run?** They'll try your slash command / CLAUDE.md / workflow
2. **Does it do what you claim?** If you say it updates docs, does it?
3. **Is it genuinely useful?** Or is it a toy example?

**How to get full points:**
- Test your automation multiple times before submitting
- Have a friend try to use it following only your docs
- Show real impact on the starter application

**Common deductions:**
- -10 points: Automation doesn't work as described
- -10 points: Automation is too simple to be useful (e.g., just runs one command)
- -5 points: Works but has major bugs or edge cases not handled

---

### "Documentation Quality" (30%)

**What graders check:**
1. **Is writeup.md complete?** All TODOs filled in?
2. **Can they understand your design without asking questions?**
3. **Are examples concrete or vague?**

**How to get full points:**
- Fill in every section thoroughly
- Use specific examples (actual commands, real files)
- Include screenshots or command outputs if helpful

**Common deductions:**
- -15 points: TODOs still present (looks unfinished)
- -10 points: Vague descriptions ("it saves time", "it's useful")
- -5 points: Missing citations to official docs

---

### "Workflow Improvement" (20%)

**What graders check:**
1. **Did you actually use the automation?** Can they see evidence?
2. **Is the before/after realistic?** Or made up?
3. **Did you complete something from TASKS.md?**

**How to get full points:**
- Use automation for at least one real TASKS.md item
- Document with specifics (files changed, lines added, time measured)
- Be realistic with time estimates

**Common deductions:**
- -10 points: No evidence of actually using the automation
- -5 points: Before/after feels hypothetical
- -5 points: Unrealistic time savings (99.9% reduction)

---

### "Thoughtfulness" (10%)

**What graders check:**
1. **Did you consider safety and errors?**
2. **Did you explain "why" or just "what"?**
3. **Did you show insight beyond just completing the assignment?**

**How to get full points:**
- Include "Safety Rules" in automations
- Explain trade-offs in writeup
- Suggest future improvements
- Acknowledge limitations

**Common deductions:**
- -5 points: No safety considerations
- -3 points: No error handling
- -2 points: Shallow writeup (just facts, no insight)

---

## Final Self-Audit

Before submitting, answer these questions honestly:

### Quality Gate 1: Completeness

- [ ] writeup.md has zero TODOs remaining
- [ ] Every section is filled with substantial content (not one-liners)
- [ ] I've cited the Claude Code best practices docs
- [ ] I have at least 2 working automations
- [ ] Each automation has clear documentation

### Quality Gate 2: Functionality

- [ ] I've tested each automation at least twice
- [ ] Someone else could use my automation with only the docs
- [ ] My automations work on the week4 starter app (not a different project)
- [ ] No critical bugs or edge cases that break the automation

### Quality Gate 3: Impact

- [ ] I actually used each automation (not just built it)
- [ ] I can point to specific code changes made with the automation
- [ ] I completed at least one task from docs/TASKS.md
- [ ] My before/after comparisons are based on real experience

### Quality Gate 4: Safety

- [ ] My automations have safety guardrails (confirmations, no auto-commit)
- [ ] Destructive actions require user confirmation
- [ ] I documented rollback/undo procedures
- [ ] I handled error cases (what if tests fail? network error? invalid input?)

### Quality Gate 5: Insight

- [ ] My writeup explains "why" not just "what"
- [ ] I identified limitations of my approach
- [ ] I suggested future improvements
- [ ] I demonstrated understanding of automation trade-offs

**If you answered "yes" to all of these, you're ready to submit.**

**If you answered "no" to any, go back and address that item before submitting.**

---

## Common Questions

**Q: My automation is simple (just 3 steps). Is that okay?**

A: Simple is fine if it's **useful**. A 3-step automation that saves 20 minutes per use is better than a 20-step automation that saves 30 seconds.

---

**Q: Can I create more than 2 automations?**

A: Yes, but focus on quality over quantity. Two excellent automations > four mediocre ones.

---

**Q: Can I use an automation from the reference solution?**

A: You can be inspired by the structure, but don't copy it verbatim. Adapt it to your needs, change the specifics, make it your own.

---

**Q: Do I need to write Python code?**

A: Depends:
- Slash commands: No code, just markdown files
- CLAUDE.md: No code, just documentation
- SubAgents: Mainly workflow design, minimal code
- MCP integration: You already wrote the MCP server in Week 3

Most of this assignment is **design and documentation**, not coding.

---

**Q: What if my automation doesn't save that much time?**

A: Time savings is one metric. Other valuable outcomes:
- **Quality improvement** (better tests, better docs)
- **Consistency** (every endpoint follows same pattern)
- **Reduced errors** (automation enforces best practices)
- **Knowledge sharing** (new devs can use the automation)

Document these benefits in your writeup.

---

**Q: Can I use AI (Claude/ChatGPT) to help design my automations?**

A: Yes! That's literally the point of the assignment. Just make sure you understand what you're building and document it clearly.

---

## Resources for Improvement

### Official Documentation
- **Claude Code Best Practices:** https://www.anthropic.com/engineering/claude-code-best-practices
- **SubAgents Guide:** https://docs.anthropic.com/en/docs/claude-code/sub-agents

### Example Repositories
Search GitHub for:
- "CLAUDE.md" - See real-world project guides
- ".claude/commands" - See community slash commands

### Learning Materials
- FastAPI docs: https://fastapi.tiangolo.com/ (if working with the starter app)
- pytest docs: https://docs.pytest.org/ (for testing automations)

---

## Final Thoughts: What This Assignment Really Teaches

This assignment isn't just about slash commands or CLAUDE.md files.

**It's about:**
1. **Systems thinking** - Designing workflows, not just writing code
2. **Efficiency optimization** - Identifying and eliminating repetition
3. **Abstraction** - Turning a manual process into a repeatable automation
4. **Documentation** - Making your work usable by others
5. **Quality enforcement** - Using automation to maintain standards

**These are the skills that differentiate senior engineers from junior engineers.**

A junior engineer writes code.

A senior engineer designs systems where code writes itself.

**This assignment teaches you to think like a senior engineer.**

Good luck! 🚀
