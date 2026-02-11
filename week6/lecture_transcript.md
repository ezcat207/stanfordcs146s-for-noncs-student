# Week 6 Lecture: Security Scanning with Semgrep

**CS146S - Modern Software Development**
**Topic:** Finding and Fixing Security Vulnerabilities with Static Analysis
**Target Audience:** 18-year-olds with no CS background

---

## Opening: Why Security Matters

Imagine you built a beautiful house with a fancy front door, top-of-the-line locks, and a security camera. You feel safe. But what if you accidentally left a basement window unlocked? Or what if the contractor used weak materials that anyone could break through?

**That's exactly what happens with software.**

You might have great features and a nice user interface, but if your code has security vulnerabilities—like SQL injection, weak encryption, or outdated dependencies—attackers can exploit those weaknesses. The scary part? You might not even know they're there.

**Today's question:** How do we find security issues in our code *before* attackers do?

**Answer:** We use automated security scanners, and today we're learning about **Semgrep**, one of the most powerful open-source tools for finding security bugs.

---

## Part 1: What is Static Analysis?

### The Car Inspection Analogy

Think about getting your car inspected:

**Option 1: Wait until it breaks down**
- You're driving on the highway
- Your brakes fail
- Now you have a dangerous emergency

**Option 2: Regular inspections**
- Mechanic checks your car while it's parked
- Finds worn brake pads BEFORE they fail
- You fix it safely, on your schedule

**Static analysis is like Option 2 for code.**

### Static vs. Dynamic Analysis

**Dynamic analysis:** Running your code and testing it
- Like test-driving a car to see if it works
- Example: Writing tests, manual testing, running the app
- **Problem:** You might miss bugs you didn't think to test for

**Static analysis:** Examining your code WITHOUT running it
- Like a mechanic inspecting a car without turning it on
- Example: Semgrep scanning your code for patterns that look dangerous
- **Benefit:** Finds issues you didn't know to look for

### What Semgrep Does

**Semgrep is a static analysis tool that:**
1. **Scans your code** (Python, JavaScript, Java, Go, and 30+ languages)
2. **Looks for dangerous patterns** (SQL injection, weak crypto, XSS, etc.)
3. **Reports findings** with file names, line numbers, and severity
4. **Suggests fixes** (sometimes automatically)

Think of Semgrep as a **security-focused spell-checker** for code. Just like spell-check finds "teh" and suggests "the," Semgrep finds "using MD5 for passwords" and suggests "use bcrypt instead."

---

## Part 2: Types of Security Issues Semgrep Finds

Semgrep organizes findings into three main categories. Let's understand each one.

### Category 1: SAST (Static Application Security Testing)

**What it is:** Code-level security vulnerabilities
**Think of it as:** Structural flaws in how you built your house

**Example vulnerabilities:**

#### 1. SQL Injection

**What it looks like (DANGEROUS ❌):**

```python
# backend/app/routers/notes.py
@router.get("/unsafe-search")
def unsafe_search(q: str, db: Session = Depends(get_db)):
    sql = text(
        f"""
        SELECT * FROM notes
        WHERE title LIKE '%{q}%'
        """
    )
    rows = db.execute(sql).all()
    return rows
```

**What's wrong?**

Imagine you search for: `'; DROP TABLE notes; --`

The SQL becomes:
```sql
SELECT * FROM notes
WHERE title LIKE '%'; DROP TABLE notes; --%'
```

**Result:** Your entire notes table gets deleted! 💥

**Why this happens:** You're putting user input (`q`) directly into SQL without sanitizing it.

**The safe way (GOOD ✅):**

```python
@router.get("/safe-search")
def safe_search(q: str, db: Session = Depends(get_db)):
    # Use SQLAlchemy ORM - automatically prevents SQL injection
    stmt = select(Note).where(Note.title.contains(q))
    rows = db.execute(stmt).scalars().all()
    return rows
```

**How Semgrep finds this:**
```
Semgrep rule: python.lang.security.audit.sqli.string-format-sql
```

#### 2. Cross-Site Scripting (XSS)

**What it looks like (DANGEROUS ❌):**

```javascript
// frontend/app.js
async function loadNotes() {
  const notes = await fetchJSON('/notes/');
  for (const n of notes) {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    //         ^^^^^^^^^ DANGER! Unsanitized user data
    list.appendChild(li);
  }
}
```

**What's wrong?**

If someone creates a note with title:
```html
<img src=x onerror="alert('You got hacked!')">
```

When the page loads, that JavaScript executes in every viewer's browser!

**Analogy:** It's like letting anyone write on your website's walls with permanent marker. Attackers can write malicious code.

**The safe way (GOOD ✅):**

```javascript
async function loadNotes() {
  const notes = await fetchJSON('/notes/');
  for (const n of notes) {
    const li = document.createElement('li');
    li.textContent = `${n.title}: ${n.content}`;
    //  ^^^^^^^^^^^ Safe! Treats everything as plain text
    list.appendChild(li);
  }
}
```

**How Semgrep finds this:**
```
Semgrep rule: javascript.browser.security.insecure-document-method
```

#### 3. Weak Cryptography

**What it looks like (DANGEROUS ❌):**

```python
# backend/app/routers/notes.py
@router.get("/debug/hash-md5")
def debug_hash_md5(q: str):
    import hashlib
    return {"algo": "md5", "hex": hashlib.md5(q.encode()).hexdigest()}
```

**What's wrong?**

MD5 is like using a "lock" made of cardboard. It **looks** like security, but it's been broken for 20+ years.

**Attackers can:**
- Generate "collisions" (two different inputs that produce the same hash)
- Reverse MD5 hashes using rainbow tables
- Break it in seconds with modern computers

**When NOT to use MD5:**
- ❌ Passwords
- ❌ Security tokens
- ❌ Digital signatures
- ❌ Anything security-critical

**When MD5 is OK:**
- ✅ Non-security checksums (detecting corrupted files)
- ✅ Generating cache keys (where security doesn't matter)

**The safe way (GOOD ✅):**

```python
@router.post("/hash-password")
def hash_password(password: str):
    import bcrypt
    # bcrypt is designed for passwords - slow and secure
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return {"hashed": hashed.decode()}
```

**How Semgrep finds this:**
```
Semgrep rule: python.lang.security.audit.insecure-hash-function
```

#### 4. Overly Permissive CORS

**What it looks like (DANGEROUS ❌):**

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ❌ Allows ANY website to make requests
    allow_credentials=True,  # ❌ Even worse - includes cookies/auth
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**What's wrong?**

**CORS = Cross-Origin Resource Sharing**

Imagine your bank has a rule: "Anyone from anywhere can access your account."

That's what `allow_origins=["*"]` does. It says:
- evil-hacker-site.com can make requests to your API ✅
- malicious-phishing.com can access your data ✅
- Any website in the world can use your backend ✅

**Even worse:** `allow_credentials=True` means they can include cookies and authentication tokens!

**The attack:**
1. User logs into your app (gets auth cookie)
2. User visits evil-site.com (in another tab)
3. Evil site makes requests to YOUR API
4. Because CORS allows it, YOUR API accepts the requests
5. Auth cookies are included (because credentials are allowed)
6. Evil site steals/modifies user's data

**The safe way (GOOD ✅):**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],  # Only YOUR domains
    allow_credentials=True,  # OK now because origins are restricted
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods
    allow_headers=["Content-Type", "Authorization"],  # Specific headers
)
```

**How Semgrep finds this:**
```
Semgrep rule: python.fastapi.security.fastapi-cors-allow-all
```

---

### Category 2: Secrets Detection

**What it is:** Hardcoded passwords, API keys, tokens in code
**Think of it as:** Leaving your house key under the doormat

**Example vulnerabilities:**

#### Hardcoded API Keys

**What it looks like (DANGEROUS ❌):**

```python
# backend/app/services/external.py
OPENAI_API_KEY = "sk-proj-AbCdEf123456789"  # ❌ NEVER do this!

def call_openai_api(prompt: str):
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    response = requests.post("https://api.openai.com/v1/chat", headers=headers)
    return response.json()
```

**What's wrong?**

When you push this to GitHub:
1. The key is public (even in "private" repos, many people can see it)
2. Bots scan GitHub for patterns like `sk-proj-` constantly
3. Within minutes, attackers steal your key
4. They use YOUR API key to rack up thousands of dollars in charges
5. You get a surprise $10,000 bill

**This happens ALL THE TIME.** GitHub reports finding 1+ million secrets per year.

**The safe way (GOOD ✅):**

```python
# backend/app/services/external.py
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ✅ Read from environment

def call_openai_api(prompt: str):
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set!")
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    response = requests.post("https://api.openai.com/v1/chat", headers=headers)
    return response.json()
```

Then create a `.env` file (which is `.gitignore`d):

```bash
# .env (never committed to git)
OPENAI_API_KEY=sk-proj-AbCdEf123456789
```

**How Semgrep finds this:**
```
Semgrep rule: generic.secrets.security.detected-openai-api-key
```

#### Other Common Secrets

Semgrep looks for:
- AWS keys (`AKIA...`)
- Database passwords
- Private keys (`-----BEGIN PRIVATE KEY-----`)
- JWT secrets
- OAuth tokens
- Stripe API keys
- GitHub personal access tokens

**Rule of thumb:** If it would be bad for someone else to have it, it's a secret. Don't commit it.

---

### Category 3: SCA (Software Composition Analysis)

**What it is:** Vulnerable dependencies (npm packages, pip packages)
**Think of it as:** Using building materials with known defects

#### Vulnerable Dependencies

**What it looks like:**

```txt
# requirements.txt
requests==2.19.1   # Released in 2018!
PyYAML==5.1        # Has known security vulnerabilities
Jinja2==2.10.1     # CVE-2019-10906 (RCE vulnerability)
```

**What's wrong?**

Libraries have bugs. When security researchers find them, they're assigned **CVE numbers** (Common Vulnerabilities and Exposures).

For example:
- **PyYAML 5.1** has CVE-2020-1747 (arbitrary code execution)
- **Jinja2 2.10.1** has CVE-2019-10906 (sandbox escape)
- **requests 2.19.1** has CVE-2018-18074 (credential leak)

**Attackers scan for vulnerable versions.** If your `requirements.txt` says you use PyYAML 5.1, they know exactly which exploit to use.

**The safe way (GOOD ✅):**

```txt
# requirements.txt (updated versions)
requests==2.31.0   # Latest stable
PyYAML==6.0.1      # Fixes all known CVEs
Jinja2==3.1.3      # Secure version
```

**How to check:**
```bash
# Semgrep can scan dependencies
semgrep ci --supply-chain

# Or use pip-audit
pip install pip-audit
pip-audit
```

**How Semgrep finds this:**
```
Semgrep rule: Supply chain vulnerabilities via OSV database
```

---

## Part 3: How Semgrep Works Under the Hood

### Pattern Matching with AST (Abstract Syntax Tree)

**Simple analogy:**

Imagine you're looking for dangerous patterns in a book. Two approaches:

**Approach 1: Text search (grep)**
- Search for the exact string "SQL injection"
- **Problem:** Attackers can rewrite code to avoid the pattern

**Approach 2: Understand the structure (Semgrep)**
- Parse the sentence structure
- Understand "This is a SQL query" and "This contains user input"
- Flag when they're combined

**Semgrep uses Approach 2.** It understands code structure, not just text.

### Example: Finding SQL Injection

**Bad code:**

```python
sql = f"SELECT * FROM users WHERE id = {user_id}"
```

**Semgrep rule (simplified):**

```yaml
rules:
  - id: sql-injection
    pattern: text(f"... {$VAR} ...")
    message: "Detected SQL injection vulnerability"
    severity: ERROR
```

**What this rule says:**
1. Look for `text(...)` function (creates SQL)
2. Look for f-strings with variables (`{$VAR}`)
3. If both are true → flag it

**Semgrep finds variations:**

```python
# All of these get caught:
sql = text(f"SELECT * FROM users WHERE id = {user_id}")
sql = text(f"SELECT * FROM {table_name} WHERE active = true")
query = text(f"DELETE FROM notes WHERE title = '{title}'")
```

**But this is OK:**

```python
# Parameterized query - safe!
stmt = select(User).where(User.id == user_id)
```

---

## Part 4: Using Semgrep - Live Demo

Let me show you how to use Semgrep in practice.

### Installation

**Option 1: Using pip (Python)**

```bash
pip install semgrep
```

**Option 2: Using Homebrew (Mac)**

```bash
brew install semgrep
```

**Option 3: Using the Semgrep Cloud Platform**
- Go to semgrep.dev
- Sign up (free for open source)
- Connect your GitHub repo
- Scans run automatically on every PR

**For this class, we'll use the CLI.**

---

### Running Your First Scan

Let's scan the week6 starter app.

**Command:**

```bash
cd week6
semgrep ci
```

**What happens:**

```
Scanning 15 files with 1000+ rules...

┌────────────────────────────────────────────────────────┐
│ Semgrep CI Scan Results                                  │
└────────────────────────────────────────────────────────┘

━━━ 8 CODE FINDINGS ━━━

backend/app/routers/notes.py
  python.lang.security.audit.sqli.string-format-sql
    SQL injection: f-string used in sql.text()

    69│ def unsafe_search(q: str, db: Session = Depends(get_db)):
    70│     sql = text(
    71│         f"""
    72│         SELECT * FROM notes
    73│         WHERE title LIKE '%{q}%'
    74│         """
    75│     )

    ⚠️  Severity: HIGH
    🔧  Autofix: Use parameterized queries

backend/app/routers/notes.py
  python.lang.security.audit.insecure-hash-function.insecure-hash-function-md5
    Insecure hash function (MD5) used

    98│ return {"algo": "md5", "hex": hashlib.md5(q.encode()).hexdigest()}

    ⚠️  Severity: MEDIUM
    🔧  Autofix: Use hashlib.sha256() or bcrypt for passwords

backend/app/main.py
  python.fastapi.security.fastapi-cors-allow-all.fastapi-cors-allow-all
    CORS allows any origin with credentials

    22│ app.add_middleware(
    23│     CORSMiddleware,
    24│     allow_origins=["*"],
    25│     allow_credentials=True,

    ⚠️  Severity: HIGH
    🔧  Autofix: Restrict origins to specific domains

frontend/app.js
  javascript.browser.security.insecure-document-method.insecure-document-method
    XSS: innerHTML used with unsanitized user input

    14│ li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;

    ⚠️  Severity: HIGH
    🔧  Autofix: Use textContent instead of innerHTML

━━━ 3 SECRETS FINDINGS ━━━

backend/app/config.py
  generic.secrets.security.detected-generic-secret.detected-generic-secret
    Possible hardcoded secret

    5│ DB_PASSWORD = "super_secret_123"

    ⚠️  Severity: CRITICAL
    🔧  Autofix: Use environment variables

━━━ 12 DEPENDENCY FINDINGS ━━━

requirements.txt
  sca.python.requests.requests-CVE-2018-18074
    requests 2.19.1 is vulnerable to CVE-2018-18074

    Vulnerability: Credential leak in redirect
    Fix: Upgrade to requests>=2.20.0

    ⚠️  Severity: HIGH

requirements.txt
  sca.python.pyyaml.pyyaml-CVE-2020-1747
    PyYAML 5.1 is vulnerable to CVE-2020-1747

    Vulnerability: Arbitrary code execution
    Fix: Upgrade to PyYAML>=5.4

    ⚠️  Severity: CRITICAL

... (10 more dependency issues)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 23 total findings
  - 8 code issues (SAST)
  - 3 secrets
  - 12 vulnerable dependencies (SCA)

Severity breakdown:
  - CRITICAL: 4
  - HIGH: 12
  - MEDIUM: 7

🔧 14 findings have autofixes available
```

**Wow! 23 security issues in a small app.**

This is why scanning is critical. These are bugs you can't easily find by manual code review.

---

### Understanding Semgrep Output

Let's break down what Semgrep tells you:

**1. File and line number**
```
backend/app/routers/notes.py:71
```
Exact location of the problem

**2. Rule ID**
```
python.lang.security.audit.sqli.string-format-sql
```
- Language: `python`
- Category: `security`
- Type: `audit` (security review)
- Specific issue: `sqli.string-format-sql`

**3. Severity**
- **CRITICAL:** Fix immediately (can lead to complete compromise)
- **HIGH:** Fix soon (significant security risk)
- **MEDIUM:** Fix eventually (potential security issue)
- **LOW:** Consider fixing (best practice violation)

**4. Autofix (when available)**
```
🔧  Autofix: Use parameterized queries
```

Some rules can automatically fix the issue:

```bash
semgrep ci --autofix
```

---

## Part 5: Triaging Findings - What to Fix?

You ran Semgrep and found 23 issues. **Do you fix all of them?**

**Short answer:** It depends.

### The Triage Process

**Think of it like a hospital emergency room:**
- **Critical patients:** Treat immediately (life-threatening)
- **High priority:** Treat soon (serious but stable)
- **Medium priority:** Schedule treatment
- **Low priority:** Monitor, treat when convenient

**Same with security findings:**

#### Step 1: Verify the Finding

**Not all findings are real vulnerabilities.** Sometimes Semgrep flags code that *looks* dangerous but isn't.

**Example of a false positive:**

```python
# This looks like SQL injection, but it's safe
ALLOWED_COLUMNS = ["id", "title", "created_at"]

def sort_notes(sort_by: str):
    if sort_by not in ALLOWED_COLUMNS:
        raise ValueError("Invalid sort column")

    # Safe because we validated sort_by against allowlist
    sql = text(f"SELECT * FROM notes ORDER BY {sort_by}")
    return db.execute(sql)
```

**Semgrep might flag this** because it sees f-string in SQL. But YOU know it's safe because `sort_by` is validated.

**What to do:**
1. Add a comment explaining why it's safe
2. Use `# nosemgrep` to suppress the finding
3. Or refactor to make it obviously safe

```python
# Option 1: Suppress with explanation
# nosemgrep: python.lang.security.audit.sqli.string-format-sql
# Safe: sort_by is validated against ALLOWED_COLUMNS allowlist
sql = text(f"SELECT * FROM notes ORDER BY {sort_by}")

# Option 2: Refactor to be obviously safe
column = getattr(Note, sort_by)  # Uses ORM, clearly safe
stmt = select(Note).order_by(column)
```

#### Step 2: Prioritize by Impact

**Questions to ask:**

1. **Can an attacker exploit this remotely?**
   - SQL injection: YES → High priority
   - Hardcoded secret in internal script: NO → Lower priority

2. **What's the worst-case scenario?**
   - SQL injection: Database deleted, all data stolen → CRITICAL
   - Weak hash on cache keys: Minor info leak → MEDIUM

3. **Is this code in production?**
   - Live website: High priority
   - Development-only debug endpoint: Lower priority

4. **How easy is it to exploit?**
   - XSS: Very easy (just create a note with HTML) → HIGH
   - Complex timing attack: Difficult → MEDIUM

#### Step 3: Fix or Accept Risk

**Three options:**

**Option 1: Fix it**
- Write the code fix
- Re-run Semgrep to confirm
- Commit the fix

**Option 2: Suppress it (false positive)**
- Add `# nosemgrep` comment
- Document why it's safe

**Option 3: Accept the risk (temporarily)**
- Create a ticket to fix later
- Document the decision
- Set a deadline

**Never:** Ignore findings without documenting why.

---

## Part 6: Fixing Vulnerabilities with AI

For this assignment, you'll use AI tools (like Claude Code, Warp, or Cursor) to help fix issues.

### Example: Fixing SQL Injection

**Semgrep finding:**

```
backend/app/routers/notes.py:71
python.lang.security.audit.sqli.string-format-sql
SQL injection: f-string used in sql.text()
```

### Using Claude Code to Fix It

**Prompt to Claude Code:**

```
Fix the SQL injection vulnerability in backend/app/routers/notes.py line 71.

Requirements:
- Use SQLAlchemy ORM (no raw SQL)
- Preserve the same functionality (search by title or content)
- Use the LIKE operator for pattern matching
- Keep the same response format
```

**Claude Code's response:**

```python
# Before (VULNERABLE ❌)
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
    results = []
    for r in rows:
        results.append(NoteRead(
            id=r.id,
            title=r.title,
            content=r.content,
            created_at=r.created_at,
            updated_at=r.updated_at,
        ))
    return results

# After (SAFE ✅)
@router.get("/search", response_model=list[NoteRead])
def search_notes(q: str, db: Session = Depends(get_db)):
    # SQLAlchemy ORM prevents SQL injection by using parameterized queries
    stmt = select(Note).where(
        (Note.title.contains(q)) | (Note.content.contains(q))
    ).order_by(desc(Note.created_at)).limit(50)

    rows = db.execute(stmt).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]
```

**What changed:**
1. ❌ Removed `text(f"...")` → ✅ Uses `select(Note)`
2. ❌ Removed f-string with user input → ✅ Uses `.contains(q)` (automatically parameterized)
3. ❌ Removed manual object construction → ✅ Uses `model_validate()` (cleaner)

**Verify the fix:**

```bash
# Re-run Semgrep
semgrep ci backend/app/routers/notes.py

# Output:
✅ No findings in backend/app/routers/notes.py (SQL injection fixed)

# Test the endpoint
pytest backend/tests/test_notes.py -k search -v

# Output:
test_search_notes_by_title PASSED
test_search_notes_by_content PASSED
test_search_notes_sql_injection_attempt PASSED
```

---

### Example: Fixing XSS

**Semgrep finding:**

```
frontend/app.js:14
javascript.browser.security.insecure-document-method
XSS: innerHTML used with unsanitized user input
```

**Prompt to AI:**

```
Fix the XSS vulnerability in frontend/app.js line 14.

Requirements:
- Prevent execution of HTML/JavaScript in note titles and content
- Keep the bold formatting for note titles
- Use safe DOM methods
```

**AI's response:**

```javascript
// Before (VULNERABLE ❌)
async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const notes = await fetchJSON('/notes/');
  for (const n of notes) {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    //  ^^^^^^^^^ XSS vulnerability - user content can include <script>
    list.appendChild(li);
  }
}

// After (SAFE ✅)
async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const notes = await fetchJSON('/notes/');
  for (const n of notes) {
    const li = document.createElement('li');

    // Create elements safely using DOM methods
    const title = document.createElement('strong');
    title.textContent = n.title;  // textContent escapes HTML automatically

    li.appendChild(title);
    li.appendChild(document.createTextNode(': '));
    li.appendChild(document.createTextNode(n.content));

    list.appendChild(li);
  }
}
```

**What changed:**
1. ❌ Removed `innerHTML` → ✅ Uses `textContent` and `createTextNode()`
2. These methods treat everything as plain text, so HTML/JS can't execute

**Verify the fix:**

```bash
semgrep ci frontend/app.js

# Output:
✅ No findings in frontend/app.js (XSS fixed)
```

**Manual test:**

```javascript
// Before fix: This would execute JavaScript
// Create note with title: <img src=x onerror="alert('XSS')">
// Result: Alert pops up ❌

// After fix: Same note title
// Result: Displays literally "<img src=x onerror="alert('XSS')">" ✅
```

---

### Example: Fixing Vulnerable Dependencies

**Semgrep finding:**

```
requirements.txt:5
sca.python.requests.requests-CVE-2018-18074
requests 2.19.1 is vulnerable to CVE-2018-18074
Fix: Upgrade to requests>=2.31.0
```

**This is the easiest fix!**

```bash
# Before
# requirements.txt
requests==2.19.1
PyYAML==5.1
Jinja2==2.10.1

# After
# requirements.txt
requests==2.31.0   # Latest stable, fixes CVE-2018-18074
PyYAML==6.0.1      # Fixes CVE-2020-1747 and others
Jinja2==3.1.3      # Fixes CVE-2019-10906

# Update your environment
pip install -r requirements.txt --upgrade

# Verify no more vulnerabilities
semgrep ci --supply-chain
```

**Important:** After upgrading dependencies, ALWAYS run your tests:

```bash
make test

# Make sure nothing broke!
# If tests fail, check breaking changes in the library changelog
```

---

## Part 7: Best Practices for Security Scanning

### 1. Scan Early, Scan Often

**Don't wait until the end of the project.**

**Bad workflow:**
```
Write code for 3 weeks → Run Semgrep → Find 100 issues → Spend 2 weeks fixing
```

**Good workflow:**
```
Write code → Run Semgrep → Fix 3 issues → Write more code → Run Semgrep → Fix 2 issues...
```

**Ideal:** Run Semgrep on every commit (CI/CD integration)

```yaml
# .github/workflows/semgrep.yml
name: Semgrep Security Scan

on: [push, pull_request]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: semgrep/semgrep-action@v1
        with:
          config: auto
```

### 2. Focus on High-Severity First

**Triage priority:**
1. CRITICAL (fix today)
2. HIGH (fix this week)
3. MEDIUM (fix this month)
4. LOW (fix eventually or suppress)

### 3. Don't Trust Autofix Blindly

**Semgrep's autofix is helpful but not perfect.**

**Always:**
1. Read the autofixed code
2. Understand what changed
3. Run tests to verify it still works
4. Manually test the fixed functionality

**Example where autofix might break things:**

```python
# Before
sql = text(f"SELECT * FROM {table_name}")

# Autofix might suggest
stmt = select(table_name)  # ❌ This doesn't work! table_name is a string, not a Table object

# Correct fix
table_obj = Base.metadata.tables[table_name]
stmt = select(table_obj)
```

### 4. Document Your Decisions

**When you suppress a finding:**

```python
# nosemgrep: python.lang.security.audit.sqli.string-format-sql
# SAFE: sort_by is validated against ALLOWED_COLUMNS allowlist
# Reviewed by: Alex Chen, 2025-01-28
sql = text(f"SELECT * FROM notes ORDER BY {sort_by}")
```

**When you accept a risk:**

```markdown
# Known Issues

## Medium: MD5 used for cache keys (backend/app/cache.py:42)
- Status: Accepted risk
- Rationale: MD5 is sufficient for non-security cache keys (performance optimization)
- Review date: 2025-02-01
- Next review: 2025-08-01
```

### 5. Keep Dependencies Updated

**Set a schedule:**
- Check for dependency updates monthly
- Update immediately if CVE is announced
- Test thoroughly after updates

**Tools to help:**
```bash
# Check for outdated packages
pip list --outdated

# Or use automated tools
pip install pip-audit
pip-audit

# GitHub Dependabot (free)
# Automatically creates PRs when dependencies have security updates
```

### 6. Educate Your Team

**Security is everyone's responsibility.**

**Team practices:**
- Weekly security review meetings
- Share interesting vulnerabilities in team chat
- Pair program on security fixes (learn from each other)
- Celebrate when team members find/fix security issues

---

## Part 8: Common Pitfalls and How to Avoid Them

### Pitfall 1: "I'll Fix It Later"

**Problem:** Security issues accumulate, become overwhelming

**Solution:**
- Fix CRITICAL/HIGH immediately
- Create tickets for MEDIUM (with deadlines)
- Suppress or document LOW

### Pitfall 2: Suppressing Real Issues

**Problem:**
```python
# nosemgrep  # ❌ No explanation!
sql = text(f"SELECT * FROM users WHERE id = {user_id}")
```

**Solution:**
```python
# TODO: Fix SQL injection vulnerability
# Ticket: SEC-123
# Target: 2025-02-15
# nosemgrep: python.lang.security.audit.sqli.string-format-sql
sql = text(f"SELECT * FROM users WHERE id = {user_id}")
```

Better yet: Just fix it!

### Pitfall 3: Only Scanning Main Branch

**Problem:** Vulnerabilities get merged before anyone notices

**Solution:** Scan on every PR

```bash
# In your PR checks
semgrep ci --baseline-ref=main

# Fails PR if new vulnerabilities are introduced
```

### Pitfall 4: Ignoring False Positives

**Problem:** Team learns to ignore Semgrep output

**Solution:** Tune your rules

```yaml
# .semgrepignore
# Ignore test files for certain rules
tests/

# Ignore specific files
legacy/old-code.py
```

### Pitfall 5: Not Testing After Fixes

**Problem:** "Fixed" the security issue but broke the feature

**Solution:** ALWAYS run tests

```bash
# After every fix
pytest

# Better yet, have CI run tests automatically
```

---

## Part 9: Beyond Semgrep - Defense in Depth

**Semgrep is powerful, but it's ONE tool in your security toolbox.**

### Other Security Practices

**1. Input Validation**
```python
from pydantic import BaseModel, validator

class NoteCreate(BaseModel):
    title: str
    content: str

    @validator('title')
    def title_must_be_reasonable(cls, v):
        if len(v) > 200:
            raise ValueError('Title too long (max 200 chars)')
        return v
```

**2. Authentication & Authorization**
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

def require_auth(token: str = Depends(security)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
```

**3. Rate Limiting**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/notes")
@limiter.limit("100/minute")  # Max 100 requests per minute
def list_notes():
    pass
```

**4. Security Headers**
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])
app.add_middleware(HTTPSRedirectMiddleware)
```

**5. Penetration Testing**
- Hire security experts to attack your app
- Find vulnerabilities that static analysis misses

**6. Bug Bounty Programs**
- Offer rewards to hackers who find bugs
- Companies like Facebook, Google do this

---

## Summary: The Week 6 Workflow

**Your assignment workflow:**

```
1. Run Semgrep scan
   ↓
2. Understand the findings
   - Read Semgrep output
   - Research unfamiliar vulnerabilities
   - Verify findings (check for false positives)
   ↓
3. Triage and prioritize
   - CRITICAL → fix immediately
   - HIGH → fix in this assignment
   - MEDIUM/LOW → document decision
   ↓
4. Fix 3+ issues using AI
   - Use Claude Code, Warp, Cursor, etc.
   - Write clear prompts explaining the issue
   - Review AI's suggested fix
   - Verify it makes sense
   ↓
5. Verify fixes
   - Re-run Semgrep (ensure issue is gone)
   - Run tests (ensure functionality works)
   - Manual test (actually try the feature)
   ↓
6. Document your work
   - Before/after code diffs
   - Explanation of the vulnerability
   - Why your fix works
   - Evidence (Semgrep output, test results)
```

---

## Key Takeaways

**1. Security scanning finds issues you can't see**
- 23 vulnerabilities in a small app
- SQL injection, XSS, weak crypto, secrets, outdated deps
- Without Semgrep, you'd never find most of these

**2. Three types of findings**
- **SAST:** Code-level vulnerabilities (SQL injection, XSS)
- **Secrets:** Hardcoded passwords/API keys
- **SCA:** Vulnerable dependencies

**3. Not all findings are equal**
- Triage: CRITICAL > HIGH > MEDIUM > LOW
- Some are false positives → suppress with explanation
- Focus on remote, high-impact, easy-to-exploit issues first

**4. AI helps fix issues faster**
- Clear prompts + context = good fixes
- Always verify AI's work
- Run tests after every fix

**5. Make security a habit**
- Scan on every commit (CI/CD)
- Fix issues incrementally (don't accumulate debt)
- Keep dependencies updated
- Document decisions

**6. Defense in depth**
- Semgrep is one layer
- Also need: input validation, auth, rate limiting, security headers, testing

---

## For Your Assignment

**Required:**
1. ✅ Run `semgrep ci` on week6 app
2. ✅ Pick 3+ issues to fix (at least one HIGH severity)
3. ✅ Use AI to help with fixes
4. ✅ Verify fixes with Semgrep + tests
5. ✅ Document:
   - Before/after code
   - Explanation of vulnerability
   - Why your fix works
   - Evidence (Semgrep output before and after)

**Bonus:**
- Fix all CRITICAL findings
- Set up Semgrep CI in GitHub Actions
- Research CVEs for dependencies and document them

**Remember:** The goal isn't just fixing 3 bugs. It's learning to:
- Recognize security vulnerabilities
- Understand why they're dangerous
- Use tools to find them systematically
- Apply fixes correctly
- Verify your work

Security is a skill you'll use your entire career. **Let's get started!** 🔐
