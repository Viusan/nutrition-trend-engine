# Nutrition Trend Engine

A pipeline that parses real nutrition-tracking exports (from [Lifesum](https://lifesum.com)), stores them in a structured database, computes real week-over-week trends and goal-adherence stats, and uses a language model **only** to phrase the already-computed findings into a short, readable summary.

This is not a GPT wrapper. The model never sees raw logs and never does any math and every number in the final output is calculated by this project's own code before the model ever runs.

## What it does

Given one or more weekly PDF exports from Lifesum, this project (so far i have only created for two weeks):

1. Parses the PDF's nutrition tables (daily summaries and individual meal entries) into structured data
2. Loads that data into a local SQLite database
3. Computes real statistics from the data:
   - Week-over-week percent change in calories, protein, and carbs
   - Percent over/under a set of personal nutrition targets, for the most recent week
   - A day-by-day breakdown of which days the calorie target was hit or missed
4. Sends those computed numbers (not the raw data) to Claude, with explicit instructions not to recalculate anything or invent patterns beyond what's given, and gets back a short natural-language summary

Example output, generated from real data:

> You consumed 12% fewer calories this week compared to last week, with protein intake down 8% and carbs dropping notably by 23%. Against your targets, you're running 12% high on calories and 14% high on protein overall, though carbs came in 45% below your goal. Looking at daily consistency, you went over your calorie target on four days (Monday, Wednesday, Thursday, and Saturday) while staying under on two days (Tuesday and Friday), with Sunday also coming in over. While the week-over-week reduction shows some pullback in intake, your targets suggest there's room to bring calories and carbs more in line with your plan.

## Why it's structured this way

Most AI + tracking data projects dump raw logs into a prompt and ask a language model to find patterns and do the math itself. That is unreliable since LLMs are not dependable at precise arithmetic over long lists of numbers, and means none of the actual analyssis is something you buit.

This project does so that the analysis happens enitry in python and sql code, using the database as the source. The language model's only job is turning correct facts into natural language, the same numbers would appear in the output no matter which model did the phrasing (dont even need a model to see the data/numbers). 

## Architecture

```
converter.py          -> parses Lifesum PDF exports into nutrition.db (SQLite)
data_analysis.py       -> queries nutrition.db, computes all stats, builds the insight prompt
insight_generator.py   -> takes computed facts, builds the LLM prompt, calls the Claude API
```

`converter.py` and `data_analysis.py` are independent and they are connected only through the shared `nutrition.db` file, not by importing each other. `data_analysis.py` is the entry point that ties the whole pipeline together, computing every stat before handing the finished numbers to `insight_generator.py`.

### Database schema

- `food_log` — one row per individual logged food item (date, meal type, title, and full nutrient breakdown)
- `daily_summary_log` — one row per day, with total nutrients for that day

Running `converter.py` wipes and rebuilds the database from scratch each time, from whatever PDFs are in the input folder, the PDFs are the source of truth, the database is a derived, disposable cache.

## Setup

1. Install dependencies:
   ```
   pip install pdfplumber anthropic python-dotenv
   ```
2. Get an API key and add a small amount of usage credit (here i used claude's API).
3. Create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```
4. Set your own nutrition targets at the top of `data_analysis.py` (`CALORIE_TARGET`, `PROTEIN_TARGET`, `CARBS_TARGET`). These are personal and not pulled from Lifesum, since lifesums own target data wasn't reliable in testing.
5. Export weekly tracking data from Lifesum as PDF and place the file(s) in the PDF input folder.

## Usage

```
python converter.py       # parses all PDFs in the input folder into nutrition.db
python data_analysis.py   # computes stats and prints a generated insight
```

## Limitations

This is a personal tool, not a general-purpose product:

- Requires at least two weeks of logged data before week-over-week comparisons are meaningful
- Nutrition targets are hardcoded constants, edited by hand when goals change
- Built and tested against Lifesum's specific PDF export format, a different export layout would need adjustments to the table-parsing logic
- No automated tests or error handling for edge cases yet (e.g. only one week of data)

## Possible next steps

- An ingredient-based meal suggestion feature
- A `goals` table instead of hardcoded constants, if targets need to vary over time
- Basic tests and error handling around the analysis step