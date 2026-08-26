import pdfplumber

table_settings = {
    # raising tolerance up to 5 allows endpoints to be more flexible and treat them as connected or as the same line
    # basically if two lines are close enough, treat them as touching.
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "snap_tolerance": 5,
    "join_tolerance": 5,
}

summary_table = None 
meal_rows = [] # we group up all the meal rows into this list since we have multiple pages which splits the tables

daily_rows = [] # we want to group up the summarry part here
# we also want to keep the average and target row somewhere
average_row = None
target_row = None

with pdfplumber.open("pdf_files/Tracking data 2026-08-19 - 2026-08-25.pdf") as pdf: # open the pdf
    for page in pdf.pages: # loop through each page
        tables = page.extract_tables(table_settings) # exctract table with out table settings
        # we check our tables and want to divide the meal log and daily summary, we do this by checking how many columns since meal and daily has different amount of columns
        for t in tables:
            num_cols = len(t[0])
            if num_cols == 12:
                summary_table = t
            elif num_cols == 17:
                for row in t:
                    # we dont want to include the header or empty rows
                    if row[0] == 'Date' or row[0] == '':
                        continue
                    meal_rows.append(row)

    # we want to remove the empty rows and also split the daily summary, average, and target rows
    for row in summary_table:
        if row[0] == '':
            continue
        elif row[0] == 'Average for the period':
            average_row = row
        elif row[0] == 'User target nutrients':
            target_row = row
        else:
            daily_rows.append(row)    
                    
for rows in daily_rows:
    for i, info in enumerate(rows):
        if info[0] == 'S': # one column contains title for summary and data, which we dont need to convert
            continue
        rows[i] = float(rows[i])

for rows in meal_rows:
    for i, info in enumerate(rows):
        if any(char.isalpha() for char in info): # if any letters we skip
            continue
        elif '-' in info: # one column contains data, which we dont need to convert
            continue
        rows[i] = float(rows[i])

print(f"Summary table rows: {len(daily_rows)}")
print(f"Total meal rows collected: {len(meal_rows)}")