import sqlite3

conn = sqlite3.connect("nutrition.db")
cursor = conn.cursor()

cursor.execute("SELECT AVG(calories) FROM daily_summary_log WHERE date BETWEEN '2026-05-11' AND '2026-05-17'")
rows = cursor.fetchall()

for row in rows:
    print(row)