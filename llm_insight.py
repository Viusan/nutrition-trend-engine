import os
import anthropic
from dotenv import load_dotenv

# Search for and load the .env file
load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def generate_insight(insights):
    daily_summary_text = ""
    # build string of which days i went over/under calorie target
    for day, target in insights['daily_hits'].items():
        daily_summary_text += day + ": " + f"{'over' if target == 1 else 'under'}\n"
    
    prompt = f"""You are given real, already-computed nutrition data comparing this week to last week. Do not recalculate, re-derive, or double-check any of the numbers below — treat every value as already correct and final.

    Your only job is to turn these facts into a short, plain-language summary, written in an encouraging but honest tone. Do not surface any pattern, comparison, or observation that isn't explicitly given below (for example, do not point out which metric changed the most, comment on consistency across days, or speculate about causes like diet or training changes) — only restate what is provided, in clearer language.

    Week-over-week changes:
    - Calories: {insights['calorie_change']}% compared to last week
    - Protein: {insights['protein_change']}% compared to last week
    - Carbs: {insights['carbs_change']}% compared to last week

    Target adherence (most recent week):
    - Calories: {insights['calorie_target_pct']}% relative to target
    - Protein: {insights['protein_target_pct']}% relative to target
    - Carbs: {insights['carbs_target_pct']}% relative to target

    Latest week daily calorie target results:
    {daily_summary_text}

    Write the summary in 3-5 sentences, plain language, no bullet points or headers."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    ) 

    # only get the text response back
    print(response.content[0].text)
       

