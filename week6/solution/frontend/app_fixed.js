/**
 * Fixed version of app.js with XSS vulnerability remediated
 *
 * Fix #2: Cross-Site Scripting (XSS)
 * - Replaced innerHTML with safe DOM methods
 * - Uses textContent to automatically escape HTML special characters
 */

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// FIX #2: XSS Prevention - safe DOM manipulation
async function loadNotes(params = {}) {
  const list = document.getElementById('notes');
  list.innerHTML = '';  // This is safe - no user data involved
  const query = new URLSearchParams(params);
  const notes = await fetchJSON('/notes/?' + query.toString());

  for (const n of notes) {
    const li = document.createElement('li');

    /**
     * SECURE: Using DOM methods instead of innerHTML with user data
     *
     * Before (VULNERABLE):
     *   li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
     *   // If n.title = "<script>alert('XSS')</script>", the script executes!
     *
     * After (SECURE):
     *   Uses textContent which automatically escapes HTML
     *   If n.title = "<script>alert('XSS')</script>", it displays as literal text
     */

    // Create strong element for title (preserves bold formatting)
    const titleElement = document.createElement('strong');
    titleElement.textContent = n.title;  // textContent escapes HTML automatically

    // Create text nodes for separator and content
    const separator = document.createTextNode(': ');
    const contentNode = document.createTextNode(n.content);

    // Append all nodes to list item
    li.appendChild(titleElement);
    li.appendChild(separator);
    li.appendChild(contentNode);

    list.appendChild(li);
  }
}

async function loadActions(params = {}) {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const items = await fetchJSON('/action-items/?' + query.toString());
  for (const a of items) {
    const li = document.createElement('li');
    // SAFE: textContent is used here (was already safe in original)
    li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions(params);
      };
      li.appendChild(btn);
    } else {
      const btn = document.createElement('button');
      btn.textContent = 'Reopen';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ completed: false }),
        });
        loadActions(params);
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('note-search-btn').addEventListener('click', async () => {
    const q = document.getElementById('note-search').value;
    loadNotes({ q });
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  document.getElementById('filter-completed').addEventListener('change', (e) => {
    const checked = e.target.checked;
    loadActions({ completed: checked });
  });

  loadNotes();
  loadActions();
});
