# Week 6 Assignment Bridge: From Lecture to Implementation

**CS146S - Modern Software Development**
**Assignment:** Security Scanning with Semgrep
**Time Estimate:** 3-4 hours
**Difficulty:** Medium

---

## What You Learned in Lecture

In the lecture, you learned about:

1. **Static analysis** - Finding bugs without running code
2. **Three types of security findings:**
   - SAST (code vulnerabilities like SQL injection, XSS)
   - Secrets (hardcoded passwords/API keys)
   - SCA (vulnerable dependencies)
3. **How Semgrep works** - Pattern matching using Abstract Syntax Trees
4. **Common vulnerabilities:** SQL injection, XSS, weak crypto, permissive CORS, outdated dependencies
5. **Using AI to fix security issues** - Writing clear prompts and verifying fixes

---

## What You'll Do in This Assignment

You'll apply those concepts to find and fix REAL security vulnerabilities in the week6 starter app.

**Your mission:**
1. Install and run Semgrep
2. Scan the week6 codebase
3. Understand the findings (triage)
4. Pick 3+ security issues to fix
5. Use AI tools to help fix them
6. Verify your fixes work
7. Document everything in your writeup

**Why this matters:** You're learning the same process security engineers use at companies like Google, Meta, and Stripe.

---

## Prerequisites Checklist

Before starting, make sure you have:

- [ ] Week 6 starter code (`week6/` directory)
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Node.js installed (for frontend scanning, optional)
- [ ] AI coding tool ready (Claude Code, Warp, Cursor, or GitHub Copilot)
- [ ] Basic understanding of the starter app (FastAPI backend + vanilla JS frontend)

---

## Part 1: Setup and Installation (30 minutes)

### Step 1: Install Semgrep

**Choose your installation method:**

**Option A: Using pip (Recommended)**

```bash
# Install Semgrep
pip install semgrep

# Verify installation
semgrep --version
# Expected output: 1.x.x or higher
```

**Option B: Using Homebrew (Mac only)**

```bash
brew install semgrep

# Verify
semgrep --version
```

**Option C: Using Docker (if pip/brew don't work)**

```bash
# Pull the image
docker pull semgrep/semgrep

# Create an alias for convenience
alias semgrep='docker run --rm -v "$(pwd):/src" semgrep/semgrep semgrep'

# Verify
semgrep --version
```

**Troubleshooting:**

If you get `command not found: semgrep`:
```bash
# Check if Python's bin directory is in your PATH
python3 -m pip show semgrep

# Add to PATH (Mac/Linux)
export PATH="$HOME/.local/bin:$PATH"

# Add to PATH (Windows)
# Add %USERPROFILE%\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.x\LocalCache\local-packages\Python3x\Scripts to PATH
```

### Step 2: Understand the Starter App Structure

Before scanning, let's understand what we're scanning:

```bash
cd week6

# Explore the structure
tree -L 2
```

**Key directories:**

```
week6/
├── backend/              ← Python FastAPI application
│   ├── app/
│   │   ├── routers/     ← API endpoints (notes.py, action_items.py)
│   │   ├── models.py    ← Database models
│   │   ├── schemas.py   ← Pydantic validation
│   │   └── main.py      ← App entry point
│   └── tests/           ← Test files
├── frontend/            ← Vanilla JavaScript frontend
│   ├── app.js          ← Main application logic
│   └── index.html      ← HTML structure
├── requirements.txt     ← Python dependencies
└── Makefile            ← Build commands
```

**Run the app to see what it does:**

```bash
# Install dependencies
pip install -r requirements.txt

# Start the backend
make run

# Open browser to http://localhost:8000
# Try creating notes and action items
```

**What you should see:**
- A simple note-taking app
- Ability to create, search, and view notes
- Ability to create and complete action items

**Stop the server (Ctrl+C) before continuing.**

### Step 3: Run Your First Scan

From the repository root (NOT inside week6/), run:

```bash
semgrep ci --subdir week6
```

**What this command does:**
- `semgrep ci` - Runs Semgrep with CI-style rules (curated for real-world use)
- `--subdir week6` - Only scans the week6 directory

**Expected output:**

```
Scanning 15 files with 1000+ Code, 50+ Secrets, 200+ Supply Chain rules

━━━ 8 CODE FINDINGS ━━━
backend/app/routers/notes.py
  ...
━━━ 3 SECRETS FINDINGS ━━━
backend/app/config.py
  ...
━━━ 12 DEPENDENCY FINDINGS ━━━
requirements.txt
  ...

Summary: 23 total findings
```

**If you see "23 total findings" (or similar), you're ready to proceed!**

**If you see errors:**
- Make sure you're in the repository root, not inside week6/
- Check that Semgrep is installed correctly
- Try `semgrep --version` to verify

---

## Part 2: Understanding and Triaging Findings (45 minutes)

### Step 1: Save the Full Output

Let's save Semgrep's output to a file for easy reference:

```bash
semgrep ci --subdir week6 > semgrep_output.txt 2>&1
```

Now you can read `semgrep_output.txt` in your editor without re-running the scan.

### Step 2: Categorize Findings

Open `semgrep_output.txt` and create a table in a new file `triage_notes.md`:

```markdown
# Semgrep Triage Notes

## Summary
- Total findings: XX
- SAST (Code): XX findings
- Secrets: XX findings
- SCA (Dependencies): XX findings

## Severity Breakdown
- CRITICAL: XX
- HIGH: XX
- MEDIUM: XX
- LOW: XX

## Findings by Category

### SAST (Static Application Security Testing)

| # | File | Line | Rule | Severity | Description | Decision |
|---|------|------|------|----------|-------------|----------|
| 1 | backend/app/routers/notes.py | 71 | sqli.string-format-sql | HIGH | SQL injection via f-string | **FIX** |
| 2 | backend/app/routers/notes.py | 98 | insecure-hash-function-md5 | MEDIUM | MD5 used for hashing | **FIX** |
| 3 | backend/app/main.py | 24 | fastapi-cors-allow-all | HIGH | CORS allows any origin | **FIX** |
| 4 | frontend/app.js | 14 | insecure-document-method | HIGH | XSS via innerHTML | FIX |
| ... | ... | ... | ... | ... | ... | ... |

### Secrets

| # | File | Line | Rule | Severity | Description | Decision |
|---|------|------|------|----------|-------------|----------|
| 1 | backend/app/config.py | 5 | detected-generic-secret | CRITICAL | Hardcoded password | FIX |
| ... | ... | ... | ... | ... | ... | ... |

### SCA (Software Composition Analysis)

| # | Package | Current | CVE | Severity | Fix Version | Decision |
|---|---------|---------|-----|----------|-------------|----------|
| 1 | requests | 2.19.1 | CVE-2018-18074 | HIGH | >=2.31.0 | FIX |
| 2 | PyYAML | 5.1 | CVE-2020-1747 | CRITICAL | >=5.4 | FIX |
| ... | ... | ... | ... | ... | ... | ... |
```

**How to fill this in:**

1. Read each finding in `semgrep_output.txt`
2. Look for patterns like:
   ```
   backend/app/routers/notes.py
     python.lang.security.audit.sqli.string-format-sql
       SQL injection: f-string used in sql.text()

       71│     sql = text(f"SELECT * FROM notes WHERE title LIKE '%{q}%'")

       ⚠️  Severity: HIGH
   ```
3. Extract:
   - File: `backend/app/routers/notes.py`
   - Line: `71`
   - Rule: `sqli.string-format-sql`
   - Severity: `HIGH`
   - Description: `SQL injection via f-string`

### Step 3: Decide What to Fix

**Required for this assignment: Fix at least 3 issues**

**Suggested strategy:**

**Priority 1: Pick at least one HIGH or CRITICAL SAST finding**
- These are actively exploitable code vulnerabilities
- Examples: SQL injection, XSS, CORS misconfiguration

**Priority 2: Pick at least one dependency (SCA) issue**
- Easy to fix (just upgrade version)
- Shows you understand supply chain security

**Priority 3: Pick one more of your choice**
- Could be another SAST issue
- Could be weak crypto
- Could be a secrets finding

**What about the rest?**
- CRITICAL/HIGH: Document why you're not fixing (if you're not)
- MEDIUM/LOW: You can skip these for the assignment
- False positives: Document in your writeup ("This finding is a false positive because...")

### Step 4: Research Unfamiliar Vulnerabilities

For each issue you'll fix, make sure you understand:
1. **What is the vulnerability?**
2. **Why is it dangerous?**
3. **How could an attacker exploit it?**
4. **What's the proper fix?**

**Resources:**
- Lecture notes (search for the vulnerability type)
- Semgrep rule documentation: `https://semgrep.dev/r/[rule-id]`
- OWASP: `https://owasp.org/www-community/vulnerabilities/`
- CVE details: `https://cve.mitre.org/cgi-bin/cvename.cgi?name=[CVE-ID]`

**Example:**

For SQL injection (`sqli.string-format-sql`):
1. **What:** User input is inserted into SQL query without sanitization
2. **Why dangerous:** Attacker can execute arbitrary SQL commands
3. **How to exploit:** Input like `'; DROP TABLE notes; --`
4. **Fix:** Use parameterized queries or ORM (SQLAlchemy)

---

## Part 3: Fixing Issues with AI (90 minutes)

Now comes the fun part: actually fixing the vulnerabilities!

### General Workflow for Each Fix

```
1. Understand the issue (from triage)
   ↓
2. Read the vulnerable code
   ↓
3. Write AI prompt (clear + specific)
   ↓
4. Review AI's suggested fix
   ↓
5. Apply the fix
   ↓
6. Verify with Semgrep
   ↓
7. Test functionality
   ↓
8. Document the fix
```

---

### Example Fix #1: SQL Injection

**Issue:** `backend/app/routers/notes.py:71` - SQL injection via f-string

**Step 1: Read the vulnerable code**

```bash
# View the code
code backend/app/routers/notes.py

# Or use less
less backend/app/routers/notes.py
```

Find line 71:
```python
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)):
    sql = text(
        f"""
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
        ORDER BY created_at DESC
        LIMIT 50
        """
    )
    rows = db.execute(sql).all()
    # ... rest of function
```

**Step 2: Write AI prompt**

**Good prompt (specific and clear):**

```
Fix the SQL injection vulnerability in backend/app/routers/notes.py, line 71 in the unsafe_search function.

Context:
- The function currently uses an f-string to insert user input (q) directly into a SQL query
- This allows SQL injection attacks

Requirements for the fix:
- Use SQLAlchemy ORM instead of raw SQL
- Use the select() statement with .where() clauses
- Preserve the same functionality (search notes by title OR content using LIKE pattern matching)
- Keep the same endpoint path and response format
- Maintain the ORDER BY created_at DESC and LIMIT 50

Show me the complete fixed function.
```

**Bad prompt (too vague):**

```
Fix the SQL injection bug
```

**Why the good prompt is better:**
- Specifies exact file and line
- Explains the current problem
- Lists specific requirements
- Clarifies what to preserve
- Asks for complete code (easier to review)

**Step 3: Review AI's suggested fix**

AI might suggest:

```python
@router.get("/safe-search", response_model=list[NoteRead])
def safe_search(q: str, db: Session = Depends(get_db)):
    # Using SQLAlchemy ORM prevents SQL injection
    stmt = select(Note).where(
        (Note.title.contains(q)) | (Note.content.contains(q))
    ).order_by(desc(Note.created_at)).limit(50)

    rows = db.execute(stmt).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]
```

**Checklist before applying:**
- [ ] Does it use ORM instead of raw SQL? ✅
- [ ] Is user input (`q`) properly parameterized? ✅ (`.contains()` does this automatically)
- [ ] Does it preserve functionality? ✅ (still searches title and content)
- [ ] Is the response format the same? ✅ (returns `list[NoteRead]`)

**Step 4: Apply the fix**

```bash
# Open file in editor
code backend/app/routers/notes.py

# Replace the unsafe_search function with safe_search
# OR rename unsafe_search to safe_search and update the implementation
```

**Note:** You can either:
- **Option A:** Replace `unsafe_search` entirely (rename to `safe_search` or keep same name)
- **Option B:** Keep `unsafe_search` as a "bad example" and add `safe_search` as new endpoint

For the assignment, **Option A (replace)** is cleaner.

**Step 5: Verify with Semgrep**

```bash
# Re-run Semgrep on just this file
semgrep ci backend/app/routers/notes.py

# Expected output:
# ✅ No findings (or reduced findings if you only fixed one issue)
```

**If Semgrep still flags it:**
- Double-check you saved the file
- Verify you're using SQLAlchemy ORM, not `text()`
- Make sure there's no f-string with SQL

**Step 6: Test functionality**

```bash
# Run the app
make run

# In another terminal, test the endpoint
curl "http://localhost:8000/notes/safe-search?q=test"

# Or use browser: http://localhost:8000/notes/safe-search?q=meeting
```

**Expected:** Same results as before, but now secure!

**Also run automated tests:**

```bash
pytest backend/tests/test_notes.py -k search -v
```

**If tests fail:** You might need to update test file paths if you renamed the endpoint.

**Step 7: Document the fix**

In your `writeup.md`:

```markdown
### Fix #1: SQL Injection in Note Search

**File:** `backend/app/routers/notes.py:71`

**Semgrep Rule:** `python.lang.security.audit.sqli.string-format-sql`

**Severity:** HIGH

**Vulnerability Description:**
The `unsafe_search` function used an f-string to directly insert user input (`q`) into a SQL query:
```python
sql = text(f"SELECT * FROM notes WHERE title LIKE '%{q}%'")
```

This allows SQL injection. An attacker could input:
```
'; DROP TABLE notes; --
```

And the SQL would become:
```sql
SELECT * FROM notes WHERE title LIKE '%'; DROP TABLE notes; --%'
```

This would delete the entire notes table.

**Fix Applied:**

Replaced raw SQL with SQLAlchemy ORM:

```python
# Before (VULNERABLE)
sql = text(f"SELECT * FROM notes WHERE title LIKE '%{q}%'")
rows = db.execute(sql).all()

# After (SECURE)
stmt = select(Note).where(Note.title.contains(q))
rows = db.execute(stmt).scalars().all()
```

**Why This Mitigates the Issue:**

SQLAlchemy's `.contains()` method uses parameterized queries under the hood. Instead of inserting user input directly into the SQL string, it passes `q` as a parameter:

```sql
-- What SQLAlchemy actually executes:
SELECT * FROM notes WHERE title LIKE ?
-- Parameter: %test%
```

The database treats `q` as DATA, not CODE, so injection is impossible.

**AI Tool Used:** Claude Code

**Verification:**
- ✅ Semgrep re-scan shows no SQL injection findings
- ✅ Tests pass: `pytest backend/tests/test_notes.py -k search`
- ✅ Manual test successful: `curl "http://localhost:8000/notes/safe-search?q=test"`

**Evidence:**

```bash
# Before fix
$ semgrep ci backend/app/routers/notes.py
Found 1 finding: SQL injection (HIGH)

# After fix
$ semgrep ci backend/app/routers/notes.py
✅ No findings
```
```

---

### Example Fix #2: XSS in Frontend

**Issue:** `frontend/app.js:14` - XSS via `innerHTML`

**Step 1: Read the vulnerable code**

```javascript
// frontend/app.js:14
async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const notes = await fetchJSON('/notes/');
  for (const n of notes) {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    list.appendChild(li);
  }
}
```

**Step 2: Write AI prompt**

```
Fix the XSS vulnerability in frontend/app.js, line 14 in the loadNotes function.

Context:
- The function currently uses innerHTML to display note titles and content
- User-created notes can contain malicious HTML/JavaScript
- If a note title is "<script>alert('XSS')</script>", the script will execute

Requirements for the fix:
- Prevent execution of HTML/JavaScript in note data
- Keep the bold formatting for note titles (<strong> tag)
- Use safe DOM manipulation methods (textContent, createElement, etc.)
- Preserve the same visual appearance

Show me the complete fixed function.
```

**Step 3: Review AI's fix**

```javascript
async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const notes = await fetchJSON('/notes/');
  for (const n of notes) {
    const li = document.createElement('li');

    // Safe: Create elements, use textContent instead of innerHTML
    const titleElement = document.createElement('strong');
    titleElement.textContent = n.title;  // textContent escapes HTML

    li.appendChild(titleElement);
    li.appendChild(document.createTextNode(': '));
    li.appendChild(document.createTextNode(n.content));

    list.appendChild(li);
  }
}
```

**Checklist:**
- [ ] No more `innerHTML` with user data? ✅
- [ ] Uses `textContent` instead? ✅ (automatically escapes HTML)
- [ ] Bold formatting preserved? ✅ (`<strong>` element still created)
- [ ] Visual appearance same? ✅

**Step 4: Apply, verify, test, document** (same process as Fix #1)

```bash
# Verify
semgrep ci frontend/app.js
# ✅ No XSS findings

# Test manually
make run
# Create a note with title: <img src=x onerror="alert('XSS')">
# Before fix: Alert pops up ❌
# After fix: Displays literally "<img src=x onerror="alert('XSS')">" ✅
```

---

### Example Fix #3: Vulnerable Dependency

**Issue:** `requirements.txt:5` - `requests` has CVE-2018-18074

**This is the easiest fix!**

**Step 1: Understand the vulnerability**

```bash
# Check the current version
grep requests requirements.txt
# Output: requests==2.19.1

# Research the CVE
# Google: "CVE-2018-18074"
# Result: Credential leak in redirect handling
```

**Step 2: Fix it**

```bash
# Edit requirements.txt
# Change: requests==2.19.1
# To:     requests==2.31.0

# Or use AI prompt:
```

**AI Prompt:**

```
Update requirements.txt to fix vulnerable dependencies.

Current vulnerable packages:
- requests==2.19.1 (CVE-2018-18074) → upgrade to >=2.31.0
- PyYAML==5.1 (CVE-2020-1747) → upgrade to >=6.0.1
- Jinja2==2.10.1 (CVE-2019-10906) → upgrade to >=3.1.3

Requirements:
- Use latest stable versions
- Maintain compatibility with FastAPI
- Keep other dependencies (fastapi, uvicorn, sqlalchemy, pydantic)

Show me the updated requirements.txt.
```

**Step 3: Apply and test**

```bash
# Update requirements.txt (manually or with AI's suggestion)

# Install updated dependencies
pip install -r requirements.txt --upgrade

# Verify no vulnerable dependencies remain
semgrep ci --supply-chain

# Run tests to ensure nothing broke
make test

# If tests fail, check library changelogs for breaking changes
```

**Step 4: Document**

```markdown
### Fix #3: Vulnerable Dependencies

**File:** `requirements.txt`

**Semgrep Rules:**
- `sca.python.requests.requests-CVE-2018-18074`
- `sca.python.pyyaml.pyyaml-CVE-2020-1747`
- `sca.python.jinja2.jinja2-CVE-2019-10906`

**Severity:** CRITICAL (PyYAML), HIGH (requests, Jinja2)

**Vulnerability Description:**
The application used very outdated dependencies with known security vulnerabilities:

1. **requests 2.19.1 (CVE-2018-18074)**
   - Credential leak when redirecting between hosts
   - Severity: HIGH

2. **PyYAML 5.1 (CVE-2020-1747)**
   - Arbitrary code execution via unsafe YAML loading
   - Severity: CRITICAL

3. **Jinja2 2.10.1 (CVE-2019-10906)**
   - Sandbox escape via format string
   - Severity: HIGH

**Fix Applied:**

Updated `requirements.txt`:

```diff
- requests==2.19.1
+ requests==2.31.0

- PyYAML==5.1
+ PyYAML==6.0.1

- Jinja2==2.10.1
+ Jinja2==3.1.3
```

**Why This Mitigates the Issues:**

The updated versions include patches for all known CVEs. Upgrading dependencies is the ONLY way to fix supply chain vulnerabilities.

**Verification:**
- ✅ `semgrep ci --supply-chain` shows no vulnerable dependencies
- ✅ All tests pass: `make test`
- ✅ Application runs successfully: `make run`

**Advisory Links:**
- requests: https://github.com/psf/requests/security/advisories
- PyYAML: https://nvd.nist.gov/vuln/detail/CVE-2020-1747
- Jinja2: https://nvd.nist.gov/vuln/detail/CVE-2019-10906
```

---

## Part 4: Final Verification (30 minutes)

After fixing all your chosen issues, run a complete verification:

### Step 1: Full Semgrep Re-scan

```bash
semgrep ci --subdir week6 > semgrep_output_after.txt 2>&1
```

**Compare before and after:**

```bash
# Before (should have ~23 findings)
grep "Summary:" semgrep_output.txt

# After (should have fewer findings)
grep "Summary:" semgrep_output_after.txt
```

**Expected:** Your 3+ fixed issues should be gone.

### Step 2: Run All Tests

```bash
# Backend tests
pytest backend/tests/ -v

# Expected: All tests pass
```

**If tests fail:**
- Read the error message carefully
- Check if you broke existing functionality
- Use AI to help debug: "Tests are failing with error X after I fixed Y. How do I fix this while maintaining security?"

### Step 3: Manual Testing

```bash
# Start the app
make run

# Test each fix:
# 1. If you fixed SQL injection: Try searching notes
# 2. If you fixed XSS: Create a note with HTML in title, verify it doesn't execute
# 3. If you fixed dependencies: Verify app still runs

# Everything should work normally!
```

### Step 4: Clean Up

```bash
# Format code
make format

# Run linter
make lint

# Final test run
make test
```

---

## Part 5: Writing Your Writeup (45 minutes)

Your writeup should follow the template in `writeup.md`. Here's the structure:

### Section 1: Findings Overview (5 minutes)

```markdown
## Findings Overview

I ran Semgrep against the week6 application and found:
- **Total findings:** 23
- **SAST (Code):** 8 findings
- **Secrets:** 3 findings
- **SCA (Dependencies):** 12 findings

### Severity Breakdown
- CRITICAL: 4
- HIGH: 12
- MEDIUM: 7

### Categories Summary

**SAST findings included:**
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Weak cryptographic hashing (MD5)
- Overly permissive CORS configuration

**Secrets findings:**
- Hardcoded database password

**SCA findings:**
- 12 outdated dependencies with known CVEs
- Most critical: PyYAML (arbitrary code execution)

### False Positives / Suppressed Findings

[Optional: If you chose NOT to fix something, explain why]

Example:
- **Rule: insecure-hash-function-md5 (line 98):**
  - Status: Accepted risk
  - Rationale: MD5 is only used for non-security cache key generation, not for passwords or authentication. Performance is prioritized over cryptographic strength for this use case.
  - Would fix in production: Yes, by switching to SHA-256
```

### Section 2: Detailed Fixes (30 minutes)

**For EACH fix (3+ required):**

```markdown
### Fix #1: [Vulnerability Type]

**File:** `path/to/file.py:line`

**Semgrep Rule:** `rule.id.here`

**Severity:** HIGH/CRITICAL/MEDIUM

**Risk Description:**
[2-3 sentences explaining what the vulnerability is and why it's dangerous]

**Before (Vulnerable Code):**
```python
# Show the vulnerable code
```

**After (Fixed Code):**
```python
# Show your fix
```

**Why This Fix Works:**
[2-3 sentences explaining how your fix mitigates the vulnerability]

**AI Tool Used:** [Claude Code / Warp / Cursor / etc.]

**Verification:**
- Semgrep output before: [paste relevant Semgrep output]
- Semgrep output after: ✅ No findings
- Tests: ✅ All passing
```

### Section 3: Lessons Learned (10 minutes)

```markdown
## Lessons Learned

1. **Static analysis finds hidden issues**
   - I was surprised to find 23 vulnerabilities in a small app
   - Many of these I would never have caught in code review

2. **Dependencies are risky**
   - Using old versions of libraries is just as dangerous as writing bad code
   - Need to regularly update dependencies

3. **AI helps with fixes, but verification is critical**
   - AI provided good starting points for fixes
   - I still needed to understand WHY the fix works
   - Testing is essential - can't blindly trust AI

[Add your own insights!]
```

---

## Troubleshooting Guide

### Issue: Semgrep not finding any issues

**Possible causes:**
1. Running from wrong directory
2. Scanning wrong files
3. Semgrep version issue

**Solutions:**
```bash
# Verify you're in repo root
pwd
# Should end with: /modern-software-dev-assignments

# Run with explicit path
semgrep ci --subdir week6

# Check Semgrep version
semgrep --version
# Should be 1.x.x or higher
```

### Issue: Too many findings (overwhelming)

**Solution:** Start with HIGH and CRITICAL only

```bash
semgrep ci --subdir week6 --severity HIGH --severity CRITICAL
```

### Issue: AI's fix breaks tests

**Solution:**
1. Read the test error carefully
2. Understand what the test expects
3. Ask AI: "The test expects X but my fix returns Y. How do I fix this while maintaining security?"

### Issue: Can't reproduce vulnerability

**Solution:**
- Some vulnerabilities are theoretical (hard to exploit in simple app)
- Focus on understanding WHY it's a vulnerability
- Document what COULD happen if exploited

---

## Time Management

**Total estimated time: 3-4 hours**

**Suggested schedule:**

| Time | Activity | Duration |
|------|----------|----------|
| 0:00 - 0:30 | Install Semgrep, run first scan | 30 min |
| 0:30 - 1:15 | Triage findings, research vulnerabilities | 45 min |
| 1:15 - 2:45 | Fix 3+ issues with AI (30 min each) | 90 min |
| 2:45 - 3:15 | Verify all fixes, run tests | 30 min |
| 3:15 - 4:00 | Write writeup | 45 min |

**Tips:**
- Take breaks between fixes
- Don't try to fix everything (focus on 3-5 good fixes)
- Ask for help if stuck for >15 minutes

---

## Success Criteria

Before submitting, verify:

- [ ] Semgrep is installed and running
- [ ] You ran `semgrep ci --subdir week6` successfully
- [ ] You fixed at least 3 security issues
- [ ] At least one fix is HIGH or CRITICAL severity
- [ ] Re-running Semgrep confirms fixes (issues are gone)
- [ ] All tests pass (`make test`)
- [ ] App still runs (`make run`)
- [ ] Writeup includes:
  - [ ] Findings overview with categories and counts
  - [ ] 3+ detailed fixes with before/after code
  - [ ] Explanation of WHY each fix works
  - [ ] Evidence (Semgrep output, test results)
- [ ] Code is committed to git
- [ ] Repository is pushed to GitHub

---

## Getting Help

**Stuck on understanding a vulnerability?**
- Re-read the lecture section on that vulnerability
- Search: "OWASP [vulnerability name]"
- Ask in office hours with specific questions

**Stuck on a fix?**
- Check if Semgrep provides autofix: `semgrep ci --autofix`
- Try different AI prompts
- Compare your code to the lecture examples

**Stuck on AI giving bad fixes?**
- Be more specific in your prompt
- Provide more context about the codebase
- Review the fix carefully - AI isn't always right!

**Good question format:**
> "I'm trying to fix [vulnerability type] in [file:line]. Semgrep flagged [issue]. I tried [what you tried] but [what went wrong]. How can I fix this while maintaining [specific requirement]?"

---

## Bonus Challenges (Optional)

If you finish early and want to go further:

1. **Fix all CRITICAL findings** (not just 3)
2. **Set up Semgrep CI** in GitHub Actions
3. **Research and document specific CVEs** for dependency vulnerabilities
4. **Create a security checklist** for future projects
5. **Write tests** that verify vulnerabilities are fixed (e.g., test that SQL injection is blocked)

---

## Final Checklist

Before you submit:

- [ ] All required fixes are complete
- [ ] Tests pass
- [ ] App runs without errors
- [ ] Writeup is thorough and well-formatted
- [ ] Code is clean (formatted, linted)
- [ ] Everything is committed and pushed
- [ ] You understand every fix you made (don't just copy AI output)

**You're ready to submit! 🎉**

Good luck, and remember: **security is not a one-time thing—it's a continuous practice.** The skills you're learning this week will serve you throughout your career.
