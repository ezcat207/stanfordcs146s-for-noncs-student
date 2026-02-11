# Week 8 Assignment Review & Common Mistakes

## 1. Bolt/AI Generation Pitfalls

### Mistake: The "Vague Prompt"
**Symptom**: You get a generic landing page instead of a functional app.
**Fix**: Be an engineer, not a tourist.
- *Bad*: "Make a cool app."
- *Good*: "Create a CRUD application for 'Notes'. It needs a sidebar for navigation and a main content area. Use LocalStorage for persistence."

### Mistake: Ignoring "Hallucinations"
**Symptom**: The code looks perfect but doesn't run because it imports a library that doesn't exist.
**Fix**: Check `package.json`. If Bolt imports `super-cool-date-picker`, make sure it's actually installed. If not, delete the import or install it manually.

---

## 2. Python (Flask) Pitfalls

### Mistake: Forgetting the Virtual Environment
**Symptom**: `ModuleNotFoundError: No module named 'flask'` even though you *swore* you installed it.
**Fix**: Look at your prompt. Does it say `(venv)` or `(week8)`? If not, run `source venv/bin/activate`.

### Mistake: Template Locations
**Symptom**: `TemplateNotFound: index.html`.
**Fix**: Flask looks for HTML files in a folder named `templates/` (plural). If your file is in the root, Flask won't find it.

---

## 3. Node (Express) Pitfalls

### Mistake: The CORS Error
**Symptom**: Your frontend `fetch()` fails with a red error in the console.
**Fix**: Install `cors` (`npm install cors`) and add `app.use(cors())` to your `server.js`. Browsers don't like it when port 5500 talks to port 3000 without permission.

### Mistake: Forgetting to Restart
**Symptom**: You changed the code, saved it, but the app behaves the same.
**Fix**: Node doesn't auto-restart by default.
- *Option A*: Stop the server (`Ctrl+C`) and run `node server.js` again.
- *Option B*: Use `nodemon` (`npx nodemon server.js`).

---

## Self-Correction Checklist

Before submitting, check these 3 things:
1.  [ ] **Python**: Can I delete a note and have it disappear? (Tests CRUD).
2.  [ ] **Node**: Does the frontend actually talk to the backend, or is it faking it? (Check Network tab).
3.  [ ] **Bolt**: Did I export the *code*, not just a screenshot?
