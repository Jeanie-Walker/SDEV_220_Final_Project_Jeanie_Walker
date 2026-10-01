import sqlite3

conn = sqlite3.connect("next_shift.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON")

cur.execute("""
    CREATE TABLE IF NOT EXISTS nurses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        credential TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL,
        adls TEXT NOT NULL,
        continence TEXT NOT NULL,
        diet TEXT NOT NULL,
        code_status TEXT NOT NULL,
        allergies TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS shifts (
        id INTEGER PRIMARY KEY,
        nurse_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        day TEXT NOT NULL,
        shift_type TEXT NOT NULL,
        FOREIGN KEY (nurse_id) REFERENCES nurses(id),
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY,
        shift_id INTEGER NOT NULL UNIQUE,
        created_at TEXT NOT NULL,
        FOREIGN KEY (shift_id) REFERENCES shifts(id)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS report_items (
        id INTEGER PRIMARY KEY,
        report_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        urgency INTEGER NOT NULL,
        FOREIGN KEY (report_id) REFERENCES reports(id)
    )
""")


conn.commit()
conn.close()