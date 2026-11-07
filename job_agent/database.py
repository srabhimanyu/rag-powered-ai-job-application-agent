import sqlite3
import json
from .config import DB_PATH

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY, company TEXT, title TEXT, location TEXT,
            experience_min INTEGER, experience_max INTEGER, skills TEXT,
            description TEXT, source TEXT, url TEXT, posted TEXT,
            match_score REAL DEFAULT 0, llm_analysis TEXT DEFAULT '',
            status TEXT DEFAULT 'NEW', created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL,
            status TEXT NOT NULL, notes TEXT DEFAULT '',
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(job_id) REFERENCES jobs(id)
        )""")

def upsert_job(job, score=0, llm_analysis=""):
    with connect() as conn:
        conn.execute("""
        INSERT INTO jobs
        (id, company, title, location, experience_min, experience_max,
         skills, description, source, url, posted, match_score, llm_analysis)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          company=excluded.company, title=excluded.title, location=excluded.location,
          experience_min=excluded.experience_min, experience_max=excluded.experience_max,
          skills=excluded.skills, description=excluded.description, source=excluded.source,
          url=excluded.url, posted=excluded.posted, match_score=excluded.match_score,
          llm_analysis=excluded.llm_analysis
        """, (job.id, job.company, job.title, job.location, job.experience_min,
              job.experience_max, json.dumps(job.skills), job.description, job.source,
              job.url, job.posted, score, llm_analysis))

def list_jobs(min_score=0, status=None):
    query, params = "SELECT * FROM jobs WHERE match_score >= ?", [min_score]
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY match_score DESC, created_at DESC"
    with connect() as conn:
        rows = conn.execute(query, params).fetchall()
    items = []
    for row in rows:
        item = dict(row)
        item["skills"] = json.loads(item["skills"] or "[]")
        items.append(item)
    return items

def set_job_status(job_id, status):
    with connect() as conn:
        conn.execute("UPDATE jobs SET status=? WHERE id=?", (status, job_id))

def record_application(job_id, status, notes=""):
    with connect() as conn:
        conn.execute("INSERT INTO applications(job_id, status, notes) VALUES (?, ?, ?)",
                     (job_id, status, notes))
        conn.execute("UPDATE jobs SET status=? WHERE id=?", (status, job_id))

def application_history():
    with connect() as conn:
        rows = conn.execute("""
        SELECT a.id, a.job_id, j.company, j.title, a.status, a.notes, a.updated_at
        FROM applications a JOIN jobs j ON j.id=a.job_id
        ORDER BY a.updated_at DESC
        """).fetchall()
    return [dict(r) for r in rows]
