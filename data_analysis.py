import sqlite3

conn = sqlite3.connect("nutrition.db")
cursor = conn.cursor()

#this will automate grouping by week so we dont need to hardcode each week
#strftime my date from the column and rewrites into a pattern i give (her %Y being year and %W being week; so outcome would be 2026-33 for example as year and week number)
#we save it as a variable week then we sort average as we would but replacing the hardcoded statement with our variable
cursor.execute("SELECT strftime('%Y-%W', date) AS week, FLOOR(AVG(calories)), FLOOR(AVG(protein)), FLOOR(AVG(carbs)) FROM daily_summary_log GROUP BY week ORDER BY week")

#gets most recent query executed through cursor
rows = cursor.fetchall()

def percentage_change(new, old):
    return int(((new-old)/old)*100)

calorie_development = percentage_change(rows[-1][1], rows[-2][1])
protein_development = percentage_change(rows[-1][2], rows[-2][2])
carbs_development = percentage_change(rows[-1][2], rows[-2][2])

print(f"Calorie change: {calorie_development}%\nProtein change: {protein_development}%\nCarbs change: {carbs_development}%")