import sqlite3
import csv

# Connect to SQLite
conn = sqlite3.connect("counselling.db")
cursor = conn.cursor()

# Drop table if exists (for fresh run)
cursor.execute("DROP TABLE IF EXISTS counselling")

# Create table
cursor.execute("""
CREATE TABLE counselling (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sr_no INTEGER,
    round TEXT,
    institute TEXT,
    program TEXT,
    group_name TEXT,
    category TEXT,
    max_gate_score INTEGER,
    min_gate_score INTEGER
)
""")

# Read CSV
with open("data.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        cursor.execute("""
        INSERT INTO counselling (
            sr_no, round, institute, program, group_name,
            category, max_gate_score, min_gate_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["Sr.No"],
            row["Round ▲▼"],
            row["Institute ▲▼"],
            row["PG Program ▲▼"],
            row["Group ▲▼"],
            row["Category ▲▼"],
            row["Max GATE Score ▲▼"],
            row["Min GATE Score ▲▼"]
        ))

conn.commit()
conn.close()

print("Database created successfully.")
