# Week 5 Assignment Review: Warp Agentic Development

**Course:** CS146S - Modern Software Development
**Week:** 5
**Topic:** Warp Drive Automations & Multi-Agent Workflows
**Target Audience:** 18-year-olds with no CS background

---

## Overview

This review guide helps you evaluate your Week 5 assignment on Warp agentic development. You'll learn how to assess the quality of your automations, identify common mistakes, and understand what makes excellent AI-assisted workflows.

**What you built:**
- **Part A:** Two Warp Drive automations (saved prompts, rules, or workflows)
- **Part B:** Multi-agent workflow using git worktree with 3+ agents in parallel
- **Documentation:** Writeup with before/after metrics and supervision strategies

---

## Self-Grading Rubric

### Part A: Warp Drive Automations (50 points)

#### Automation Quality (30 points)

**Excellent (27-30 points):**
- ✅ Automations solve real, repetitive problems (not toy examples)
- ✅ Clear, detailed instructions that AI can follow autonomously
- ✅ Includes variables/parameters for flexibility
- ✅ Safety rules prevent destructive actions
- ✅ Handles errors gracefully (tells AI what to do when things fail)
- ✅ Expected output examples show what success looks like
- ✅ Integration with project context (uses existing tools/structure)

**Good (24-26 points):**
- ✅ Automations solve real problems
- ✅ Instructions are mostly clear but may need human clarification
- ✅ Basic error handling (stops on failure, asks for help)
- ✅ Some expected output examples
- ⚠️ May require high supervision to work correctly

**Adequate (21-23 points):**
- ✅ Automations address legitimate tasks
- ⚠️ Instructions are vague or incomplete
- ⚠️ Limited error handling (AI gets stuck easily)
- ⚠️ Missing expected output examples
- ⚠️ Requires constant supervision

**Needs Improvement (<21 points):**
- ❌ Automations don't solve real problems (trivial tasks)
- ❌ Instructions are unclear or incorrect
- ❌ No error handling (fails catastrophically)
- ❌ No expected outputs
- ❌ Doesn't integrate with project

**Common mistakes in Part A:**

1. **Automation is too simple**
   - ❌ Bad: "Run pytest" (one command, no added value)
   - ✅ Good: "Run pytest, analyze coverage, suggest tests, offer to generate them"

2. **Instructions lack specificity**
   - ❌ Bad: "Fix the code" (AI doesn't know what to fix or how)
   - ✅ Good: "If tests fail, show error output, ask: (a) Debug (b) Fix manually (c) Abort"

3. **No variables/parameters**
   - ❌ Bad: Hardcoded file paths that only work for one specific file
   - ✅ Good: `{target}` variable that accepts any test file or directory

4. **Missing safety rules**
   - ❌ Bad: Automation can delete files without confirmation
   - ✅ Good: "Never delete files without explicit user approval"

5. **No expected outputs**
   - ❌ Bad: User doesn't know what success looks like
   - ✅ Good: Clear examples showing successful and failed executions

#### Documentation Quality (20 points)

**Excellent (18-20 points):**
- ✅ Clear before/after metrics with real numbers
- ✅ Concrete usage examples showing actual commands
- ✅ Honest assessment of autonomy level (Level 1-5 with explanation)
- ✅ Specific supervision strategy (what to watch, when to intervene)
- ✅ Real impact described with evidence (time saved, errors prevented)

**Good (16-17 points):**
- ✅ Before/after metrics present
- ✅ Usage examples included
- ✅ Autonomy level stated
- ⚠️ Supervision strategy is generic ("check occasionally")
- ⚠️ Impact is described but lacks specific evidence

**Adequate (14-15 points):**
- ⚠️ Vague metrics ("saves time" without numbers)
- ⚠️ Usage examples are incomplete
- ⚠️ Autonomy level not explained
- ⚠️ Supervision strategy missing

**Needs Improvement (<14 points):**
- ❌ No metrics provided
- ❌ No usage examples
- ❌ Autonomy level not stated
- ❌ No supervision strategy

**Common mistakes in documentation:**

1. **Vague metrics**
   - ❌ Bad: "This saves a lot of time"
   - ✅ Good: "Reduced from 25 min to 3 min (88% faster)"

2. **No usage examples**
   - ❌ Bad: Only describing what the automation does
   - ✅ Good: Showing actual commands and expected output

3. **Unrealistic autonomy claims**
   - ❌ Bad: "Fully autonomous" when it requires constant supervision
   - ✅ Good: "Semi-autonomous (Level 3/5) - runs automatically but requires approval for destructive actions"

4. **Missing supervision details**
   - ❌ Bad: "I monitor the automation"
   - ✅ Good: "I review suggested test scenarios before approving generation (30 seconds), then verify tests pass"

---

### Part B: Multi-Agent Workflow (50 points)

#### Workflow Design (25 points)

**Excellent (23-25 points):**
- ✅ 3+ agents working on truly independent features (minimal file overlap)
- ✅ Clear, detailed instructions for each agent
- ✅ Agents follow consistent coding standards (from rules file)
- ✅ Git worktree used correctly (separate branches, isolated workspaces)
- ✅ Merge strategy planned ahead (order matters, conflicts expected)
- ✅ All agents complete successfully with passing tests

**Good (20-22 points):**
- ✅ 3+ agents with mostly independent work
- ✅ Instructions are clear but may lack some details
- ✅ Git worktree used correctly
- ⚠️ Some file overlap causes merge conflicts (but resolved)
- ⚠️ Merge strategy is reactive rather than planned

**Adequate (17-19 points):**
- ✅ 3 agents launched
- ⚠️ Significant file overlap causes complex merge conflicts
- ⚠️ Instructions are incomplete (agents get stuck)
- ⚠️ Git worktree setup is incorrect or inefficient
- ⚠️ Tests fail after merge (quality issues)

**Needs Improvement (<17 points):**
- ❌ Fewer than 3 agents
- ❌ Agents work on dependent tasks (defeats the purpose of parallel work)
- ❌ Git worktree not used or used incorrectly
- ❌ Final merge fails or tests don't pass
- ❌ No evidence of actual parallel work

**Common mistakes in Part B:**

1. **Agents work on dependent tasks**
   - ❌ Bad: Agent 1 creates model, Agent 2 uses that model (sequential dependency)
   - ✅ Good: Agent 1 adds search, Agent 2 adds archive, Agent 3 adds categories (independent)

2. **No agent instructions**
   - ❌ Bad: Telling AI "add search feature" without specifics
   - ✅ Good: Detailed instructions with requirements, test cases, expected files

3. **Git worktree misused**
   - ❌ Bad: Creating worktrees but working in main directory
   - ✅ Good: Each agent in separate worktree, isolated branches

4. **Merging without verification**
   - ❌ Bad: Merging all branches without running tests first
   - ✅ Good: Test each branch independently BEFORE merging

5. **No merge strategy**
   - ❌ Bad: Merging in random order, surprised by conflicts
   - ✅ Good: Merge schema changes first, features last (predictable)

#### Coordination & Results (25 points)

**Excellent (23-25 points):**
- ✅ Clear coordination notes (what you did at T+0, T+5, T+15 min)
- ✅ Honest assessment of challenges encountered
- ✅ Specific solutions to problems (not "I fixed it" but "I did X because Y")
- ✅ Measurable time savings (sequential vs parallel comparison)
- ✅ Quality maintained (all tests pass, coverage doesn't drop)
- ✅ Evidence of work (git history, test output, coverage reports)

**Good (20-22 points):**
- ✅ Coordination timeline present
- ✅ Challenges mentioned
- ✅ Time savings calculated
- ⚠️ Solutions to problems are vague
- ⚠️ Limited evidence of work

**Adequate (17-19 points):**
- ⚠️ Timeline is incomplete or unclear
- ⚠️ Challenges mentioned but not solved
- ⚠️ Time savings not calculated or unrealistic
- ⚠️ Quality dropped (test coverage decreased, tests failing)

**Needs Improvement (<17 points):**
- ❌ No coordination notes
- ❌ No challenges mentioned (unrealistic - there are always challenges)
- ❌ No time comparison
- ❌ Quality issues (tests don't pass, code doesn't work)
- ❌ No evidence (could be fabricated)

**Common mistakes in coordination:**

1. **No timeline**
   - ❌ Bad: "I ran 3 agents and they finished"
   - ✅ Good: "T+0: Launched agents. T+5: Agent 1 done, Agents 2-3 in progress. T+15: All complete"

2. **Ignoring challenges**
   - ❌ Bad: Claiming everything worked perfectly (unlikely)
   - ✅ Good: "Agent 2 failed due to database migration issue. Fixed by deleting db.sqlite"

3. **Unrealistic time savings**
   - ❌ Bad: Claiming 90% time savings with parallel work (overhead exists)
   - ✅ Good: Realistic calculation including merge time and conflict resolution

4. **No evidence**
   - ❌ Bad: Claiming work was done with no screenshots, git history, or test output
   - ✅ Good: Git log showing 3 branches, test output showing all tests pass

---

## Common Mistakes Across Both Parts

### 1. Automations Don't Actually Save Time

**The problem:**
You create an automation for a task that only happens once, or the automation takes longer to run than doing the task manually.

**Example:**
- ❌ Bad: Automation to "create a new file" (takes 1 second manually)
- ❌ Bad: Automation for one-time setup task

**Why it matters:**
The point of automation is to save time on *repetitive* tasks. One-off tasks aren't worth automating.

**How to fix:**
Choose tasks you do multiple times per assignment:
- ✅ Running tests with coverage analysis (done 10+ times)
- ✅ Adding new endpoints (done 5+ times)
- ✅ Enforcing code standards (applies to every line of code)

### 2. Supervision Level Doesn't Match Reality

**The problem:**
You claim "fully autonomous" but actually had to intervene constantly, or claim "high supervision" but never checked the agent's work.

**Example:**
- ❌ Bad: Claiming Level 5 autonomy when AI asked for confirmation 5 times
- ❌ Bad: Claiming "minimal supervision" when you had to fix errors every 2 minutes

**Why it matters:**
Honest assessment helps you understand when AI assistance is actually effective vs when it creates more work.

**How to fix:**
Be truthful:
- Level 5: Runs start to finish, zero human input needed
- Level 4: Runs independently, human reviews output at end
- Level 3: Runs but asks for approval on key decisions (most common)
- Level 2: Requires frequent guidance and corrections
- Level 1: Essentially manual work with AI suggestions

### 3. Multi-Agent Work Isn't Actually Parallel

**The problem:**
You launch 3 agents but they're working on sequential tasks, or you wait for Agent 1 to finish before starting Agent 2.

**Example:**
- ❌ Bad: Agent 1 creates database model, Agent 2 adds endpoint using that model (sequential dependency)
- ❌ Bad: Starting agents at T+0, T+10, T+20 (not parallel)

**Why it matters:**
The entire point of multi-agent workflow is parallelism. If tasks are sequential, you gain no time savings.

**How to fix:**
Ensure true independence:
- ✅ Good: 3 agents adding different routers (notes, action_items, users)
- ✅ Good: 3 agents adding independent features to same router (search, archive, categories)
- ✅ Start all agents at the same time (T+0 for all)

### 4. No Error Handling in Automations

**The problem:**
Your automation doesn't tell AI what to do when things fail, so it gets stuck or does the wrong thing.

**Example:**
- ❌ Bad: "Run tests" → AI runs tests, they fail, AI stops (user doesn't know what happened)
- ❌ Bad: "Add endpoint" → AI tries to add to wrong file, continues anyway

**Why it matters:**
Real-world automation must handle failures gracefully. Without error handling, automations are brittle and unreliable.

**How to fix:**
Add explicit failure handling:
```markdown
2. **Handle test failures:**
   - If tests fail:
     * Show the failing test output in full
     * Stop execution immediately
     * Ask user: "Tests failed. Options: (a) Help me debug (b) I'll fix manually (c) Abort"
     * Wait for user choice before proceeding
   - If tests pass: Continue to step 3
```

### 5. Git Worktree Confusion

**The problem:**
You create worktrees but don't actually use them (work in main directory), or you use them incorrectly (same branch in multiple worktrees).

**Example:**
- ❌ Bad: Create 3 worktrees but run all commands in `~/week5/starter`
- ❌ Bad: Create worktrees but use the same branch for multiple agents

**Why it matters:**
Git worktree is what enables conflict-free parallel development. Using it wrong defeats the purpose.

**How to fix:**
Verify your setup:
```bash
# Create worktrees (each with unique branch)
git worktree add ../worktree-1 -b feature/task-1
git worktree add ../worktree-2 -b feature/task-2
git worktree add ../worktree-3 -b feature/task-3

# Verify correct setup
git worktree list
# Should show 3 worktrees with 3 different branches

# Work in separate directories
cd ../worktree-1  # Agent 1 works here
cd ../worktree-2  # Agent 2 works here
cd ../worktree-3  # Agent 3 works here
```

### 6. Merge Conflicts Panic

**The problem:**
When merge conflicts occur, you give up or force-push, rather than resolving them properly.

**Example:**
- ❌ Bad: See merge conflict → delete branch → start over
- ❌ Bad: See merge conflict → force push main branch (loses work)

**Why it matters:**
Merge conflicts are EXPECTED when multiple agents modify similar files. Learning to resolve them is critical.

**How to fix:**
Embrace conflicts:
1. See what's conflicted: `git status`
2. Open conflicted file
3. Look for `<<<<<<< HEAD` markers
4. Keep BOTH changes (usually):
   ```python
   # Keep both fields
   class Note(Base):
       category = Column(String(50))    # From Agent 1
       archived = Column(Boolean)        # From Agent 2
   ```
5. Mark resolved: `git add <file>`
6. Commit: `git commit -m "merge: Resolved conflicts in models.py"`

### 7. Fabricated Metrics

**The problem:**
You make up time savings or metrics without actually measuring them.

**Example:**
- ❌ Bad: "This saved 90% of my time" (but you didn't time the before/after)
- ❌ Bad: "Coverage improved by 30%" (but coverage report shows 5% improvement)

**Why it matters:**
The assignment teaches you to measure productivity gains honestly. Fabricated metrics defeat the learning objective.

**How to fix:**
Actually measure:
- Time before: Use a stopwatch for manual approach
- Time after: Time the automated approach including supervision
- Calculate: (Before - After) / Before = % improvement
- Be honest: If automation didn't save time, explain why

### 8. Writeup is Generic

**The problem:**
Your writeup could apply to anyone's assignment (no specific details, examples, or evidence unique to your work).

**Example:**
- ❌ Bad: "I used Warp to create automations that save time"
- ❌ Bad: "I ran 3 agents in parallel and they finished fast"

**Why it matters:**
Specific details prove you did the work and thought critically about it.

**How to fix:**
Include concrete details:
- ✅ Actual commit hashes from your git log
- ✅ Specific line numbers of untested code
- ✅ Real file names and commands from your project
- ✅ Screenshots or terminal output from your work
- ✅ Honest challenges YOU encountered (not generic problems)

---

## Red Flags (Automatic Deductions)

These issues result in significant point deductions:

### Critical Issues (−20 points each)

1. **No evidence of work**
   - No git commits showing branches
   - No test output showing tests pass
   - Writeup describes work that doesn't match submitted files

2. **Automations don't work**
   - Saved prompts have syntax errors
   - Rules file has invalid YAML
   - Following automation instructions produces errors

3. **Multi-agent workflow is fake**
   - Only 1-2 agents used (requirement is 3+)
   - Git history shows sequential commits (not parallel)
   - Claims of time savings don't match timeline

### Major Issues (−10 points each)

1. **Safety violations**
   - Automation can delete files without confirmation
   - Automation can force-push to main branch
   - No safeguards against destructive actions

2. **Final code doesn't work**
   - Tests fail after merge
   - Code has syntax errors
   - Features claimed in writeup don't exist in code

3. **Plagiarism from reference solution**
   - Copied example writeup word-for-word
   - Copied saved prompts without customization
   - No original thought or adaptation

### Minor Issues (−5 points each)

1. **Incomplete documentation**
   - Missing before/after metrics
   - No usage examples
   - No supervision strategy

2. **Poor code quality**
   - No type hints (violated project rules)
   - Tests have poor coverage (<70%)
   - Linting errors present

3. **Unrealistic claims**
   - Claims 95% time savings (overhead makes this impossible)
   - Claims Level 5 autonomy on complex tasks (unlikely)
   - No challenges encountered (unrealistic)

---

## Excellence Indicators

These elements indicate exceptional work:

### Part A Excellence

1. **Sophisticated automation logic**
   - Conditionals (if tests fail, do X; if pass, do Y)
   - Loops (for each low-coverage file, suggest tests)
   - Integration (combines multiple tools: pytest, coverage, test generation)

2. **Real productivity gains**
   - Measured 50%+ time savings with evidence
   - Automation used multiple times during assignment
   - Clear ROI (time to create vs time saved)

3. **Production quality**
   - Comprehensive error handling
   - Detailed expected outputs for multiple scenarios
   - Safety rules prevent all destructive actions
   - Variables make automation flexible and reusable

### Part B Excellence

1. **Complex coordination**
   - 4+ agents (beyond minimum requirement)
   - Agents work on different routers/modules
   - Minimal merge conflicts due to smart planning

2. **Thoughtful merge strategy**
   - Merge order planned based on dependencies
   - Conflicts anticipated and resolved smoothly
   - All tests pass after each merge (not just final)

3. **Honest, detailed analysis**
   - Specific challenges with exact error messages
   - Solutions explained with reasoning
   - Realistic time calculations including overhead
   - Evidence: git log, test output, screenshots

---

## Self-Assessment Questions

Before submitting, answer these honestly:

### Part A: Warp Drive Automations

1. **Would I actually use these automations again next week?**
   - If no → automations may be too simple or not useful

2. **Can someone else use my automation by reading the saved prompt?**
   - If no → instructions may be unclear or incomplete

3. **Did I actually measure the time savings?**
   - If no → metrics may be fabricated or guessed

4. **Does my automation handle errors gracefully?**
   - If no → automation will fail in real use

5. **Is my supervision strategy specific enough that someone could replicate it?**
   - If no → documentation needs more detail

### Part B: Multi-Agent Workflow

1. **Did all agents start at the same time (T+0)?**
   - If no → work wasn't truly parallel

2. **Are my agent tasks truly independent?**
   - If Agent 2 needs Agent 1's work → not independent

3. **Did I verify each branch's tests BEFORE merging?**
   - If no → you merged untested code (risky)

4. **Did I encounter ANY challenges or problems?**
   - If no → may be unrealistic or fabricated

5. **Can I show git history proving 3 parallel branches were merged?**
   - If no → evidence is missing

### Overall Assignment

1. **Did I spend at least 4-5 hours on this assignment?**
   - If no → work may be too shallow

2. **Is my writeup specific to MY work (not generic)?**
   - Test: Could this writeup apply to someone else's assignment?
   - If yes → add more specific details

3. **Have I been honest about autonomy levels and supervision?**
   - If no → revise to match reality

4. **Do I have evidence for every claim I make?**
   - If no → add screenshots, git logs, test output

---

## Improvement Checklist

Use this checklist to improve your assignment before submission:

### Part A: Warp Drive Automations

- [ ] Each automation solves a real, repetitive problem
- [ ] Instructions are detailed enough for AI to follow autonomously
- [ ] Variables/parameters make automations flexible
- [ ] Safety rules prevent destructive actions
- [ ] Error handling tells AI what to do when things fail
- [ ] Expected output examples show success and failure scenarios
- [ ] Before/after metrics are measured (not guessed)
- [ ] Usage examples show actual commands and output
- [ ] Autonomy level is realistic and explained
- [ ] Supervision strategy is specific (what, when, how to monitor)
- [ ] Real impact described with evidence

### Part B: Multi-Agent Workflow

- [ ] 3+ agents working on independent features
- [ ] Clear, detailed instructions for each agent
- [ ] Git worktree used correctly (separate directories and branches)
- [ ] All agents started at T+0 (parallel work)
- [ ] Each branch's tests verified BEFORE merging
- [ ] Merge strategy planned (order matters)
- [ ] Merge conflicts resolved (if any occurred)
- [ ] Final tests pass after all merges
- [ ] Coordination timeline with specific timestamps
- [ ] Challenges encountered are described honestly
- [ ] Solutions to problems are specific (not vague)
- [ ] Time savings calculated realistically (including overhead)
- [ ] Quality maintained (test coverage, linting, no bugs)
- [ ] Evidence provided (git log, test output, screenshots)

### Documentation Quality

- [ ] Writeup is specific to MY work (unique details)
- [ ] Metrics are backed by measurements or evidence
- [ ] Examples use actual commands and file names from my project
- [ ] Challenges are honest (not everything went perfectly)
- [ ] Claims match evidence (don't exaggerate)
- [ ] Autonomy assessment is realistic
- [ ] Supervision strategy is actionable
- [ ] Files submitted match what's described in writeup

---

## Example Self-Grading

**Student:** Alex Chen
**Part A Score:** 48/50
**Part B Score:** 47/50
**Total:** 95/100

### Part A Breakdown

**Automation Quality: 29/30**
- ✅ Test Coverage Analyzer solves real problem (manual coverage analysis is tedious)
- ✅ Clear, step-by-step instructions with error handling
- ✅ Variables for flexibility ({target})
- ✅ Safety rules (never modify app code, never commit automatically)
- ✅ Expected output examples for success and failure
- ✅ Integration with project (uses pytest, coverage, existing test structure)
- ⚠️ Minor: Could add more customization options (coverage thresholds)

**Documentation Quality: 19/20**
- ✅ Before/after metrics measured (25 min → 3 min)
- ✅ Concrete usage examples with actual commands
- ✅ Realistic autonomy level (Level 3/5, explained)
- ✅ Specific supervision strategy (review suggestions before approval)
- ✅ Real impact with evidence (improved coverage 65% → 92%)
- ⚠️ Minor: Could include screenshots of actual usage

### Part B Breakdown

**Workflow Design: 24/25**
- ✅ 3 agents on independent features (search, archive, categories)
- ✅ Clear instructions with requirements and test cases
- ✅ Git worktree used correctly (3 separate worktrees and branches)
- ✅ Merge strategy planned (schema changes first, features last)
- ✅ All agents completed with passing tests
- ⚠️ Minor: One merge conflict in models.py (expected, but could plan better)

**Coordination & Results: 23/25**
- ✅ Clear timeline (T+0, T+5, T+15, T+20)
- ✅ Honest challenges (Agent Beta database issue, merge conflict)
- ✅ Specific solutions (delete db.sqlite, combine both fields)
- ✅ Time savings calculated (45 min → 29 min = 36% faster)
- ✅ Quality maintained (40 tests passing, 89% coverage)
- ✅ Evidence (git log with commit hashes, test output)
- ⚠️ Could provide more detail on monitoring strategy (what exactly to check at T+5)
- ⚠️ Could include screenshot of worktree list or git log

### What Could Be Improved

1. **Add screenshots:** Visual evidence would strengthen claims
2. **More customization:** Test coverage analyzer could accept threshold parameters
3. **Better merge planning:** Anticipate model.py conflict by coordinating field names upfront
4. **More monitoring detail:** Specify exactly what to check at each timestamp

### What Was Done Well

1. **Realistic metrics:** Time measurements include overhead and conflict resolution
2. **Honest challenges:** Didn't claim perfection, described real issues encountered
3. **Specific details:** Commit hashes, actual file names, real commands used
4. **Quality maintained:** All tests pass, high coverage, no bugs introduced
5. **Thoughtful analysis:** Explained when multi-agent is worth it vs not worth it

---

## Final Submission Checklist

Before submitting your assignment:

- [ ] All required files are present:
  - [ ] warp-drive/ directory with saved prompts and/or rules
  - [ ] multi-agent-workflow/ directory with instructions and documentation
  - [ ] writeup.md with both Part A and Part B

- [ ] Code quality verified:
  - [ ] All tests pass: `make test`
  - [ ] No linting errors: `make lint`
  - [ ] Code formatted: `make format`

- [ ] Git history clean:
  - [ ] Commits show 3+ feature branches
  - [ ] Branches were merged to main
  - [ ] Commit messages follow conventional format

- [ ] Documentation complete:
  - [ ] Before/after metrics for each automation
  - [ ] Usage examples with actual commands
  - [ ] Autonomy levels stated and explained
  - [ ] Supervision strategies described
  - [ ] Coordination timeline for multi-agent work
  - [ ] Challenges and solutions documented

- [ ] Evidence provided:
  - [ ] Git log showing parallel branches
  - [ ] Test output showing all tests pass
  - [ ] (Optional) Screenshots of automation in action

- [ ] Self-assessment honest:
  - [ ] Autonomy levels realistic
  - [ ] Challenges documented honestly
  - [ ] Metrics measured (not fabricated)
  - [ ] Claims match evidence

---

## Getting Help

If you're unsure about your work:

1. **Use the rubric:** Score yourself honestly on each section
2. **Check common mistakes:** Make sure you didn't fall into these traps
3. **Ask specific questions:** "Is my automation too simple?" (with details)
4. **Share evidence:** Show your git log, test output, or automation file

**Good questions:**
- "My coverage analyzer automation saves 88% time. Is that realistic?"
- "I had zero merge conflicts. Is that a red flag?"
- "Here's my git log. Does this prove parallel work?"

**Vague questions (avoid):**
- "Is my assignment good?"
- "How many points will I get?"
- "Did I do it right?"

---

## Summary

**Excellent assignments demonstrate:**
1. Automations that solve real, repetitive problems with measurable impact
2. Multi-agent workflows that truly run in parallel with evidence
3. Honest, detailed documentation with specific examples and evidence
4. Realistic autonomy assessments and supervision strategies
5. Quality code that passes all tests and follows project standards

**Common pitfalls to avoid:**
1. Trivial automations that don't save time
2. Sequential "multi-agent" work (not actually parallel)
3. Fabricated metrics without measurement
4. Generic writeups without specific details
5. Missing evidence (no git log, test output, or screenshots)

**Remember:** The goal isn't perfection—it's learning how to coordinate AI agents effectively and honestly assess their value. Good documentation of challenges and limitations is more valuable than pretending everything worked flawlessly.

Good luck! 🚀
