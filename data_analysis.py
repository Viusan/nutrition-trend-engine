import sqlite3

conn = sqlite3.connect("nutrition.db")
cursor = conn.cursor()

#this will automate grouping by week so we dont need to hardcode each week
#strftime my date from the column and rewrites into a pattern i give (her %Y being year and %W being week; so outcome would be 2026-33 for example as year and week number)
#we save it as a variable week then we sort average as we would but replacing the hardcoded statement with our variable
cursor.execute("SELECT strftime('%Y-%W', date) AS week, AVG(calories) FROM daily_summary_log GROUP BY week")
rows = cursor.fetchall()

for row in rows:
    print(row)