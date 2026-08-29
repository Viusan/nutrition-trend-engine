import sqlite3

from llm_insight import generate_insight
from datetime import datetime

# what my target should be
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

# function that calculates percentage change
def percentage_change(new, old):
    return round(((new-old)/old)*100)

# weekly change
calorie_development = percentage_change(rows[-1][1], rows[-2][1])
protein_development = percentage_change(rows[-1][2], rows[-2][2])
carbs_development = percentage_change(rows[-1][3], rows[-2][3])

# how much i hit or missed my goals for the latest week
calorie_target_latest_week = percentage_change(rows[-1][1], CALORIE_TARGET)
protein_target_latest_week = percentage_change(rows[-1][2], PROTEIN_TARGET)
carbs_target_latest_week = percentage_change(rows[-1][3], CARBS_TARGET)

# this part is to check each day of the latest week if i hit my calorie goal
cursor.execute("SELECT date, calories, protein, carbs FROM daily_summary_log WHERE strftime('%Y-%W', date) = ? ORDER BY strftime('%Y-%W', date)", (rows[-1][0],))
daily_data = cursor.fetchall()
# empty dict to put my hit or miss
daily_dict = {}

# using pythons datetime module to know what day is what
for row in daily_data:
    parsed_date = datetime.strptime(row[0], "%Y-%m-%d")
    day_name = parsed_date.strftime("%A")
    # if i hit over target, i add 1 and under adds 0
    if row[1] > CALORIE_TARGET:
        daily_dict[day_name] = 1
    else:
        daily_dict[day_name] = 0

# creating a dict with the data i want to use in my prompt
insights = {
    "calorie_change": calorie_development,
    "protein_change": protein_development,
    "carbs_change": carbs_development,
    "calorie_target_pct": calorie_target_latest_week,
    "protein_target_pct": protein_target_latest_week,
    "carbs_target_pct": carbs_target_latest_week,
    "daily_hits": daily_dict,
}

# function that runs prompt calling api 
generate_insight(insights)