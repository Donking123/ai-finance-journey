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
#       model="claude-sonnet-5",
#       max_tokens=256,
#       temperature=0.0,       <-- NEW PARAMETER
#       messages=[{"role": "user", "content": prompt}]
#   )



# --- High temperature: 3 runs at temperature=1.0 ---
# TODO: Loop 3 times, each time calling Claude with temperature=1.0
# Print each result and observe: they should be noticeably different



# --- Compare ---
# TODO: Print a summary of what you observed
# Which was more consistent? Which was more interesting?
