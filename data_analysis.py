import sqlite3

from datetime import datetime

CALORIE_TARGET = 1900
PROTEIN_TARGET = 140
CARBS_TARGET = 300

conn = sqlite3.connect("nutrition.db")
cursor = conn.cursor()

#this will automate grouping by week so we dont need to hardcode each week
#strftime my date from the column and rewrites into a pattern i give (her %Y being year and %W being week; so outcome would be 2026-33 for example as year and week number)
#we save it as a variable week then we sort average as we would but replacing the hardcoded statement with our variable
cursor.execute("SELECT strftime('%Y-%W', date) AS week, FLOOR(AVG(calories)), FLOOR(AVG(protein)), FLOOR(AVG(carbs)) FROM daily_summary_log GROUP BY week ORDER BY week")

#gets most recent query executed through cursor
rows = cursor.fetchall()

def percentage_change(new, old):
    return round(((new-old)/old)*100)

calorie_development = percentage_change(rows[-1][1], rows[-2][1])
protein_development = percentage_change(rows[-1][2], rows[-2][2])
carbs_development = percentage_change(rows[-1][3], rows[-2][3])

calorie_target_latest_week = percentage_change(rows[-1][1], CALORIE_TARGET)
protein_target_latest_week = percentage_change(rows[-1][2], PROTEIN_TARGET)
carbs_target_latest_week = percentage_change(rows[-1][3], CARBS_TARGET)

print(f"Calorie change: {calorie_development}%\nProtein change: {protein_development}%\nCarbs change: {carbs_development}%")
print(f"Missed/Hit Calorie Target: {calorie_target_latest_week}%")
print(f"Missed/Hit Protein Target: {protein_target_latest_week}%")
print(f"Missed/Hit Carbs Target: {carbs_target_latest_week}%")

cursor.execute("SELECT date, calories, protein, carbs FROM daily_summary_log WHERE strftime('%Y-%W', date) = ? ORDER BY strftime('%Y-%W', date)", (rows[-1][0],))

daily_data = cursor.fetchall()

daily_dict = {}

for row in daily_data:
    parsed_date = datetime.strptime(row[0], "%Y-%m-%d")
    day_name = parsed_date.strftime("%A")
    if row[1] > CALORIE_TARGET:
        daily_dict[day_name] = 1
    else:
        daily_dict[day_name] = 0

print(daily_dict)