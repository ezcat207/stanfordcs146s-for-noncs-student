# Week 8 Bridge: From Lecture to Assignment

**Target Audience:** 18-year-old student who understands the concept of AI Generators but needs to build 3 apps.
**Goal:** Demystify the "Multi-Stack" assignment and explain exactly how to execute it.

---

## 1. The Challenge: One Idea, Three Execution Paths

"So, the lecture said: *'Syntax is cheap.'*
The assignment says: *'Prove it.'*

Your job is to build the exact same app three times.
Let's say your idea is a 'Developer Journal' (CRUD notes app).
You need to build:
1.  **The AI Version**: Using Bolt.new.
2.  **The Python Version**: Using Flask or Django (Non-JS requirement).
3.  **The JS Version**: Using Node/Express or MERN.

You aren't just coding; you are comparing *workflows*."

---

## 2. Path 1: Bolt.new (The Speed Run)

**The Task:** Use the AI Generator.
**How to do it**:
1.  **Get your Credit**: Check your email for the code. Go to bolt.new settings and apply it.
2.  **The Prompt**: Don't just say "Make a notes app".
    - *Say:* "Create a Developer Journal app. It should have a SQLite database. Users can create entries with a title, body, and tags. The UI should be dark mode."
3.  **The Export**: Bolt runs in the browser. To submit it, you need the code.
    - Click the "Download" or "Export" button in Bolt.
    - Unzip it into `week8/bolt-version/`.
4.  **The Reflection**: In `writeup.md`, note how fast it was. Did it make mistakes? Did you have to fix the prompt?

---

## 3. Path 2: The Non-JS Stack (Python/Flask)

**The Task:** Build the backend without JavaScript.
**Why?**: To show you aren't just a React script-kiddie.
**How to do it**:
1.  **Setup**:
    ```bash
    mkdir week8/python-version
    cd week8/python-version
    python3 -m venv venv
    source venv/bin/activate
    pip install flask sqlalchemy
    ```
2.  **The Code**:
    - Create `app.py`.
    - Use Flask to serve HTML templates (`render_template`).
    - Use SQLAlchemy for the database.
    - **No React**. Use simple HTML/CSS forms.
3.  **The Lesson**: Notice how different it feels to render HTML on the server vs. the client.

---

## 4. Path 3: The JS Stack (Node/Express)

**The Task:** The "Traditional" Modern Stack.
**How to do it**:
1.  **Setup**:
    ```bash
    mkdir week8/node-version
    npm init -y
    npm install express cors sqlite3
    ```
2.  **The Code**:
    - Build a REST API in `server.js`.
    - Build a simple `index.html` that uses `fetch()` to get data.
3.  **The Lesson**: Compare this to the Python version. Notice how much *more* code you write for the API + Frontend split compared to Flask's server-side rendering (or Bolt's instant generation).

---

## 5. The Deliverables (The Checklist)

"At the end, your `week8` folder should look like this:

- `week8/`
    - `bolt-version/` (Source code downloaded from Bolt)
    - `python-version/` (Your Flask app)
    - `node-version/` (Your Express app)
    - `writeup.md` (FILLED OUT with your reflections)

**Don't forget the READMEs!** Every folder needs a `README.md` telling the TA how to run it.
- Python: 'Run `python app.py`'
- Node: 'Run `node server.js`'
- Bolt: 'Run `npm run dev`'
"
