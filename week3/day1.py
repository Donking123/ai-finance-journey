"""
Week 3 - Day 1: Temperature — Controlling Creativity vs Consistency
====================================================================
Goal: See how temperature changes Claude's output.
      Low = consistent and predictable. High = varied and creative.
"""

import anthropic

client = anthropic.Anthropic()

headline = "Grab Holdings announces $500M share buyback program amid investor pressure"

prompt = f"""Analyze this financial headline in 2 sentences.
Headline: {headline}"""


# --- Low temperature: 3 runs at temperature=0.0 ---
# TODO: Loop 3 times, each time calling Claude with temperature=0.0
# Print each result and observe: they should be nearly identical
#
# Pattern:
#   message = client.messages.create(
#       model="claude-sonnet-4-6",
#       max_tokens=256,
#       temperature=0.0,       <-- NEW PARAMETER
#       messages=[{"role": "user", "content": prompt}]
#   )

print("=" * 60)
print("LOW TEMPERATURE (0.0) — 3 runs:")
print("=" * 60)

for i in range(3):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    )
    reply = next(block.text for block in message.content if block.type == "text")
    print(f"\nRun {i+1}:")
    print(reply)

# --- High temperature: 3 runs at temperature=1.0 ---
print("\n" + "=" * 60)
print("HIGH TEMPERATURE (1.0) — 3 runs:")
print("=" * 60)

for i in range(3):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        temperature=1.0,
        messages=[{"role": "user", "content": prompt}]
    )
    reply = next(block.text for block in message.content if block.type == "text")
    print(f"\nRun {i+1}:")
    print(reply)
