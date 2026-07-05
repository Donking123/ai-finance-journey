"""
Week 2 - Day 2: Prompt Engineering for Finance
================================================
Goal: Learn how different prompts give different results.
      Make Claude return structured JSON instead of plain text.

Exercise:
  1. Take the SAME headline
  2. Try 3 different prompts (basic, detailed, JSON)
  3. Compare the outputs — see how prompt quality controls output quality
"""

import anthropic
import json

client = anthropic.Anthropic()

headline = "OCBC Bank acquires Great Eastern for $1.4 billion, creating Southeast Asia's largest bancassurance group"

# --- Prompt 1: Vague (bad prompt) ---
# TODO: Send this headline to Claude with a vague prompt like "What do you think about this?"
# Store the response in result_1
message = client.messages.create(
    model = "claude-sonnet-5",
    max_tokens = 1024,
    messages = [
        {"role": "user", "content": f"what do you think about this? {headline}"}
    ]
)
result_1 = next(block.text for block in message.content if block.type == "text")

# --- Prompt 2: Specific (better prompt) ---
# TODO: Send the same headline with a more specific prompt asking for:
#       sentiment, key entities, market impact, and who benefits/loses
# Store the response in result_2
message = client.messages.create(
    model = "claude-sonnet-5",
    max_tokens = 1024,
    messages = [
        {"role": "user", "content": f"""Analyse this financial headline. Return exactly:
Sentiment: [positive/negative/neutral]
Key Entities: [list]
Market Impact: [one sentence]
Who Benefits: [list]
Who Loses: [list]

Headline: {headline}"""}
    ]
)
result_2 = next(block.text for block in message.content if block.type == "text")


# --- Prompt 3: JSON output (best prompt) ---
# TODO: Send the same headline but ask Claude to return valid JSON with this structure:
#       {
#         "sentiment": "positive/negative/neutral",
#         "confidence": 0.0 to 1.0,
#         "entities": ["list", "of", "entities"],
#         "market_impact": "one sentence",
#         "winners": ["who benefits"],
#         "losers": ["who loses"]
#       }
# Store the response in result_3
message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"""Analyze this financial headline. Return ONLY valid JSON, no other text.
Use this exact structure:
{{
  "sentiment": "positive or negative or neutral",
  "confidence": 0.0 to 1.0,
  "entities": ["list", "of", "entities"],
  "market_impact": "one sentence",
  "winners": ["who benefits"],
  "losers": ["who loses"]
}}

Headline: {headline}"""}
    ]
)
result_3 = next(block.text for block in message.content if block.type == "text")

# --- Print all 3 results ---
print("=" * 60)
print("PROMPT 1 - Vague:")
print("=" * 60)
print(result_1)

print("\n" + "=" * 60)
print("PROMPT 2 - Specific:")
print("=" * 60)
print(result_2)

print("\n" + "=" * 60)
print("PROMPT 3 - JSON:")
print("=" * 60)
print(result_3)

# --- Bonus: Parse the JSON response and use it ---
clean_json = result_3.strip().removeprefix("```json").removesuffix("```").strip()
data = json.loads(clean_json)
print(f"\nSentiment: {data['sentiment']} (confidence: {data['confidence']})")
