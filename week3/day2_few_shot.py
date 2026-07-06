"""
Week 3 - Day 2: Few-Shot Prompting — Teach Claude by Showing Examples
=======================================================================
Goal: See how giving Claude examples before asking improves consistency.
      Zero-shot (no examples) vs few-shot (with examples).
"""

import anthropic
import json

client = anthropic.Anthropic()

# --- Headlines to classify ---
headlines = [
    "DBS slashes 500 jobs after completing Laksa Bank acquisition to cut costs",
    "Singtel shares plunge 10% after reporting worst quarterly loss in a decade",
    "MAS warns Singapore banks to brace for rising loan defaults amid global slowdown",
    "CapitaLand sells $2B property portfolio as REIT index hits 52-week low",
    "Tesla stock surges 15% after Elon Musk announces surprise $10B share buyback",
]


# --- Zero-shot: just ask, no examples ---
# TODO: Create a function zero_shot(headline) that asks Claude to classify
# the headline into one of these categories:
#   earnings, M&A, regulatory, macro, market_movement
# Just ask — don't give any examples.
# Return the response text.

def get_text(message):
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "NO_RESPONSE"

def zero_shot(headline):
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=50,
        messages=[
            {"role": "user", "content": f"""Classify this financial headline into one of these categories: earnings, M&A, regulatory, macro, market_movement

Return ONLY the category name, nothing else.

Headline: {headline}"""}
        ]
    )
    return get_text(message)

# --- Few-shot: give examples first, then ask ---
# TODO: Create a function few_shot(headline) that gives Claude 5 examples
# before asking it to classify the new headline.
#
# The examples to include in your prompt:
#   "Apple reports Q3 revenue of $81.4 billion, up 8% year-over-year"
#   → earnings
#
#   "Microsoft completes $69 billion acquisition of Activision Blizzard"
#   → M&A
#
#   "SEC announces new rules for crypto exchange registration"
#   → regulatory
#
#   "China GDP growth slows to 4.9%, below economist forecasts"
#   → macro
#
#   "S&P 500 falls 3% as tech selloff intensifies"
#   → market_movement
#
# Then ask Claude to classify the new headline.
# Tell Claude to return ONLY the category, nothing else.
# Return the response text.

def few_shot(headline):
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=50,
        messages=[
            {"role": "user", "content": f"""Classify financial headlines into one of these categories: earnings, M&A, regulatory, macro, market_movement

Examples:
Headline: "Apple reports Q3 revenue of $81.4 billion, up 8% year-over-year"
Category: earnings

Headline: "Microsoft completes $69 billion acquisition of Activision Blizzard"
Category: M&A

Headline: "SEC announces new rules for crypto exchange registration"
Category: regulatory

Headline: "China GDP growth slows to 4.9%, below economist forecasts"
Category: macro

Headline: "S&P 500 falls 3% as tech selloff intensifies"
Category: market_movement

Now classify this headline. Return ONLY the category name, nothing else.
Headline: "{headline}"
Category:"""}
        ]
    )
    return get_text(message)



# --- Run both on all headlines and compare ---
# TODO: Loop through headlines
# For each one, run zero_shot() and few_shot()
# Print both results side by side
# Observe: few-shot should be more consistent and accurate



# --- Save results ---
# TODO: Save results to "classification_results.json"
results = []
print(f"{'HEADLINE':<55} {'ZERO-SHOT':<20} {'FEW-SHOT':<20}")
print("-" * 95)

for headline in headlines:
    zs = zero_shot(headline)
    fs = few_shot(headline)
    print(f"{headline[:53]:<55} {zs:<20} {fs:<20}")
    results.append({
        "headline": headline,
        "zero_shot": zs,
        "few_shot": fs,
    })

with open("classification_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved to classification_results.json")