"""
Week 2 - Day 5: Error Handling & Cost Tracking
================================================
Goal: Make your code production-ready.
      Handle API failures gracefully and track what things cost.
"""

import anthropic
import json

client = anthropic.Anthropic()

headlines = [
    "DBS Group reports record Q2 profit of $2.9 billion, beats analyst expectations",
    "Singtel warns of potential 15% revenue decline amid fierce competition",
    "MAS holds interest rates steady, signals cautious outlook for Singapore economy",
    "Sea Limited stock surges 20% after surprise profitable quarter",
    "Grab Holdings announces $500M share buyback program amid investor pressure",
]

# --- Track totals ---
total_input_tokens = 0
total_output_tokens = 0
results = []


# --- Process each headline with error handling ---
# TODO: Loop through headlines with a for loop
# Inside the loop:
#   1. Wrap the API call in try/except
#   2. On success:
#      - Get the reply text
#      - Add message.usage.input_tokens to total_input_tokens
#      - Add message.usage.output_tokens to total_output_tokens
#      - Print the headline and analysis
#      - Append to results
#   3. On error:
#      - Catch anthropic.APIError and print a message
#      - Continue to the next headline (don't crash)
#
# Pattern:
#   try:
#       message = client.messages.create(...)
#       # success code here
#   except anthropic.APIError as e:
#       print(f"Error analyzing headline: {e}")

for i, headline in enumerate(headlines):
    try:
        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"""Analyze this headline in one sentence.
Headline: {headline}"""}
            ]
        )

        reply = next(block.text for block in message.content if block.type == "text")

        total_input_tokens += message.usage.input_tokens
        total_output_tokens += message.usage.output_tokens

        print(f"\n[{i+1}/{len(headlines)}] {headline}")
        print(f"Analysis: {reply}")
        print(f"Tokens: {message.usage.input_tokens} in / {message.usage.output_tokens} out")

        results.append({
            "headline": headline,
            "analysis": reply,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        })

    except anthropic.APIError as e:
        print(f"\n[{i+1}/{len(headlines)}] ERROR on: {headline}")
        print(f"Error: {e}")

    
input_cost = total_input_tokens * (3.00 / 1_000_000)
output_cost = total_output_tokens * (15.00 / 1_000_000)
total_cost = input_cost + output_cost

print("\n" + "=" * 50)
print("COST SUMMARY")
print("=" * 50)
print(f"Headlines processed: {len(results)}/{len(headlines)}")
print(f"Input tokens:  {total_input_tokens}")
print(f"Output tokens: {total_output_tokens}")
print(f"Estimated cost: ${total_cost:.6f}")

with open("headline_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved to headline_results.json")
