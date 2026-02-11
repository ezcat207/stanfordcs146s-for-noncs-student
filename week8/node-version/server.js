const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Database Setup
const db = new sqlite3.Database(':memory:'); // Using memory for simplicity, or './journal.db'
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)");
});

// Routes
app.get('/api/entries', (req, res) => {
    db.all("SELECT * FROM entries", [], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

app.post('/api/entries', (req, res) => {
    const { title, content } = req.body;
    if (!title || !content) return res.status(400).json({ error: "Title and content required" });

    const stmt = db.prepare("INSERT INTO entries (title, content) VALUES (?, ?)");
    stmt.run(title, content, function (err) {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ id: this.lastID, title, content });
    });
    stmt.finalize();
});

app.delete('/api/entries/:id', (req, res) => {
    const { id } = req.params;
    db.run("DELETE FROM entries WHERE id = ?", id, function (err) {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ message: "Deleted", changes: this.changes });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
