import sqlite3

conn = sqlite3.connect("next_shift.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON")

# insert into nurses
nurses = [
    ("Francis Smith", "RN"),
    ("Alex Walls", "LPN"),
    ("Pilar Flores", "RN"),
    ("Gail Robinson", "LPN"),
    ("Samantha Couch", "LPN"),
    ("Amanda Richards", "RN"),
    ("Whitni Tailor", "LPN"),
    ("Ayesha Johnson", "RN"),
]

cur.executemany(
    "INSERT INTO nurses (name, credential) VALUES (?, ?)",
    nurses,
)

# insert into patients
patients = [
    ("Linda Williams", "Total assist", "Incontinent of B&B", "Enteral feeds, NPO", "DNR", "NKA"),
    ("Sherry Banks", "Mod assist", "Incontinent of bladder", "Mech soft NAS", "Full Code", "Statins"),
    ("Bethany Carter", "Mod(toileting, bathing, mobility) min(eating)", "Continent", "Regular", "Full Code", "Penicillin")
]

cur.executemany(
    "INSERT INTO patients (name, adls, continence, diet, code_status, allergies) VALUES (?, ?, ?, ?, ?, ?)", 
    patients,
)

# insert into shifts
shifts = [
    (1, 1, "Mon", "day"),
    (1, 1, "Tue", "day"),
    (1, 1, "Wed", "day"),
    (4, 1, "Mon", "night"),
    (2, 1, "Tue", "night"),
    (2, 1, "Wed", "night"),
    (3, 2, "Mon", "day"),
    (3, 2, "Tue", "day"),
    (5, 2, "Wed", "day"),
    (5, 2, "Mon", "night"),
    (6, 2, "Tue", "night"),
    (6, 2, "Wed", "night"),
    (7, 3, "Mon", "day"),
    (7, 3, "Tue", "day"),
    (8, 3, "Wed", "day"),
    (8, 3, "Mon", "night"),
    (4, 3, "Tue", "night"),
    (4, 3, "Wed", "night"),
    (4, 1, "Sun", "night"),
    (5, 2, "Sun", "night"),
    (8, 3, "Sun", "night")
]

cur.executemany(
    "INSERT INTO shifts(nurse_id, patient_id, day, shift_type) VALUES (?, ?, ?, ?)",
    shifts,
)

# insert into reports
reports = [
    (19, "2026-10-05 06:40"),
    (20, "2026-10-05 06:45"),
    (21, "2026-10-05 06:50")
]

cur.executemany(
    "INSERT INTO reports(shift_id, created_at) VALUES (?, ?)",
    reports,
)

# insert into report items
report_items = [
    # Linda's report (report 1)
    (1, "Skin", "Redness on sacrum, repositioned q2h, monitor", 1),
    (1, "Nutrition", "Tolerated well, no residual", 3),
    (1, "Refills", "Refill needed on Keppra", 2),
    (1, "Elimination", "Large, formed", 3),
    (1, "PRN meds", "Applied Calazime to sacrum per order", 3),

    # Sherry's report (report 2)
    (2, "Incident", "Follow up fall, continues neuro checks, currently q2hrs until 1000", 1),
    (2, "New orders", "neuro checks, see order", 2),
    (2, "New orders", "Colace by mouth twice daily for constipation", 2),
    (2, "Elimination", "Small, hard", 3),

    # Bethany's report (report3)
    (3, "MD notification", "Notify MD about continued insomnia", 2),
    (3, "Respiratory", "Lungs noted with rhonchi, cleared with cough assist", 3),
    (3, "Function", "Pt noted to be irritable, refused care x2", 3),
    (3, "Other", "Pt c/o headache in the night but refused PRN pain reliever", 3),
    (3, "Elimination", "No BM this shift", 3)

]

cur.executemany(
    "INSERT INTO report_items(report_id, category, description, urgency) VALUES (?, ?, ?, ?)",
    report_items,
)

conn.commit()
conn.close()