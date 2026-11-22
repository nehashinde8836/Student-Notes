"""
Local Windows runner — serves both the frontend and the Flask API
on http://localhost:5000  (no Nginx needed on Windows)
"""
import os, sys
from datetime import datetime

FRONTEND = os.path.join(os.path.dirname(__file__), "app", "frontend", "index.html")
DB_PATH  = os.environ.get("NOTES_DB", "notes.db")
VERSION  = os.environ.get("APP_VERSION", "1.0")

from flask import Flask, send_file, jsonify, request, g
import sqlite3, socket

app = Flask(__name__)

# ── DB ──────────────────────────────────────────────────────────
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "subject TEXT NOT NULL,"
            "content TEXT NOT NULL,"
            "pinned INTEGER NOT NULL DEFAULT 0,"
            "color TEXT NOT NULL DEFAULT 'default',"
            "created_at TEXT NOT NULL DEFAULT (datetime('now')),"
            "updated_at TEXT NOT NULL DEFAULT (datetime('now')))"
        )
        g.db.commit()
        for col, defval in [
            ("color","'default'"),
            ("created_at","(datetime('now'))"),
            ("updated_at","(datetime('now'))")
        ]:
            try:
                g.db.execute(f"ALTER TABLE notes ADD COLUMN {col} TEXT NOT NULL DEFAULT {defval}")
                g.db.commit()
            except Exception:
                pass
    return g.db

@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db: db.close()

def row_to_dict(row):
    return {"id":row["id"],"subject":row["subject"],"content":row["content"],
            "pinned":bool(row["pinned"]),"color":row["color"],
            "created_at":row["created_at"],"updated_at":row["updated_at"]}

# ── Frontend ────────────────────────────────────────────────────
@app.get("/")
def index():
    return send_file(FRONTEND)

# ── API ─────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return jsonify(status="ok", service="student-notes")

@app.get("/api/info")
def info():
    db = get_db()
    total   = db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    pinned  = db.execute("SELECT COUNT(*) FROM notes WHERE pinned=1").fetchone()[0]
    subjects= db.execute("SELECT COUNT(DISTINCT subject) FROM notes").fetchone()[0]
    return jsonify(app="Student Notes", version=VERSION, host=socket.gethostname(),
                   stats={"total":total,"pinned":pinned,"subjects":subjects})

@app.get("/api/notes")
def list_notes():
    subject = request.args.get("subject","").strip()
    search  = request.args.get("search","").strip()
    query   = "SELECT * FROM notes WHERE 1=1"
    params  = []
    if subject:
        query += " AND subject = ?"; params.append(subject)
    if search:
        query += " AND (subject LIKE ? OR content LIKE ?)"; params += [f"%{search}%",f"%{search}%"]
    query += " ORDER BY pinned DESC, updated_at DESC"
    return jsonify([row_to_dict(r) for r in get_db().execute(query, params).fetchall()])

@app.get("/api/subjects")
def list_subjects():
    rows = get_db().execute(
        "SELECT subject, COUNT(*) as count FROM notes GROUP BY subject ORDER BY subject"
    ).fetchall()
    return jsonify([{"subject":r["subject"],"count":r["count"]} for r in rows])

@app.post("/api/notes")
def create_note():
    data    = request.get_json(silent=True) or {}
    subject = str(data.get("subject","")).strip()
    content = str(data.get("content","")).strip()
    color   = str(data.get("color","default")).strip()
    pinned  = int(bool(data.get("pinned", False)))
    if not subject or not content:
        return jsonify(error="subject and content are required"), 400
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    db  = get_db()
    cur = db.execute(
        "INSERT INTO notes (subject,content,color,pinned,created_at,updated_at) VALUES (?,?,?,?,?,?)",
        (subject, content, color, pinned, now, now)
    )
    db.commit()
    row = db.execute("SELECT * FROM notes WHERE id=?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201

@app.put("/api/notes/<int:note_id>")
def update_note(note_id):
    data = request.get_json(silent=True) or {}
    db   = get_db()
    row  = db.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if row is None: return jsonify(error="not found"), 404
    subject = str(data.get("subject", row["subject"])).strip() or row["subject"]
    content = str(data.get("content", row["content"])).strip() or row["content"]
    pinned  = int(bool(data.get("pinned", row["pinned"])))
    color   = str(data.get("color", row["color"])).strip()
    now     = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    db.execute("UPDATE notes SET subject=?,content=?,pinned=?,color=?,updated_at=? WHERE id=?",
               (subject,content,pinned,color,now,note_id))
    db.commit()
    row = db.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    return jsonify(row_to_dict(row))

@app.delete("/api/notes/<int:note_id>")
def delete_note(note_id):
    db  = get_db()
    cur = db.execute("DELETE FROM notes WHERE id=?", (note_id,))
    db.commit()
    if cur.rowcount == 0: return jsonify(error="not found"), 404
    return "", 204

if __name__ == "__main__":
    print("\n========================================")
    print("  Student Notes - running locally")
    print("  Open http://localhost:5000 in browser")
    print("========================================\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
