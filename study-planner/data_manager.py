import sqlite3

DB_NAME = "study_planner.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create Subjects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    # Create Topics table with reviewer column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            notes TEXT,
            reviewer TEXT,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    ''')
    # Add reviewer column if it doesn't exist (for upgrades)
    try:
        cursor.execute("ALTER TABLE topics ADD COLUMN reviewer TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def save_reviewer(topic_id, reviewer):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE topics SET reviewer = ? WHERE id = ?", (reviewer, topic_id))
    conn.commit()
    conn.close()

def get_reviewer(topic_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT reviewer FROM topics WHERE id = ?", (topic_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] else None

def get_subjects():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM subjects")
    subjects = cursor.fetchall()
    conn.close()
    return subjects

def add_subject(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_topics(subject_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, notes FROM topics WHERE subject_id = ?", (subject_id,))
    topics = cursor.fetchall()
    conn.close()
    return topics

def add_topic(subject_id, name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO topics (subject_id, name, notes) VALUES (?, ?, '')", (subject_id, name))
    conn.commit()
    conn.close()

def update_topic_notes(topic_id, notes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE topics SET notes = ? WHERE id = ?", (notes, topic_id))
    conn.commit()
    conn.close()
