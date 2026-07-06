"""
Week 3 - Day 5: Prompt Library — Reusable Prompt Templates for Finance
=======================================================================
Goal: Build a dictionary of prompt templates you can reuse across projects.
      Create a run_prompt() function that looks up a template, fills in
      placeholders, sends to Claude, and returns the response.
"""

import anthropic
import json

client = anthropic.Anthropic()

def get_text(message):
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "NO_RESPONSE"


# --- Step 1: Build the prompt library ---
# TODO: Create a dictionary called prompt_library with 5 templates.
#   Each key is the template name, each value is an f-string-style template
#   (use {placeholder} for variables that get filled in later).
#
#   "sentiment_analysis":
#       "Classify the sentiment of this financial headline as BULLISH, BEARISH, or NEUTRAL.
#        Also provide a confidence score from 0-100.
#        Return ONLY JSON: {{\"sentiment\": \"...\", \"confidence\": ..., \"reasoning\": \"...\"}}
#        Headline: {headline}"
#
#   "risk_assessment":
#       "Identify the top 3 risks in this financial scenario. For each risk, rate severity
#        as HIGH, MEDIUM, or LOW and explain why.
#        Return as a numbered list.
#        Scenario: {scenario}"
#
#   "earnings_summary":
#       "Summarize these quarterly earnings into 4 key metrics:
#        1. Revenue performance (growth/decline and why)
#        2. Profitability (margins and efficiency)
#        3. Risk indicators (NPL, leverage, etc.)
#        4. Outlook (one sentence forward-looking view)
#        Keep each point to 1-2 sentences.
#        Earnings data: {earnings_data}"
#
#   "comparison":
#       "Compare these two investment options. Give pros and cons for each,
#        then a recommendation with reasoning.
#        Option A: {option_a}
#        Option B: {option_b}"
#
#   "explain_simple":
#       "Explain this financial concept in simple terms that a beginner investor
#        would understand. Use an everyday analogy. Keep it under 100 words.
#        Concept: {concept}"
prompt_library = {
    "sentiment_analysis":
    """Classify the sentiment of this financial headline as BULLISH, BEARISH, or NEUTRAL.
    Also provide a confidence score from 0-100.
    Return ONLY JSON: {{"sentiment": "...", "confidence": ..., "reasoning": "..."}}
    Headline: {headline}""",

   "risk_assessment":
    """Identify the top 3 risks in this financial scenario. For each risk, rate severity
    as HIGH, MEDIUM, or LOW and explain why.
    Return as a numbered list.
    Scenario: {scenario}""",

    "earnings_summary":
    """Summarize these quarterly earnings into 4 key metrics:
    1. Revenue performance (growth/decline and why)
    2. Profitability (margins and efficiency)
    3. Risk indicators (NPL, leverage, etc.)
    4. Outlook (one sentence forward-looking view)
    Keep each point to 1-2 sentences.
    Earnings data: {earnings_data}""",

    "comparison":
    """Compare these two investment options. Give pros and cons for each,
    then a recommendation with reasoning.
    Option A: {option_a}
    Option B: {option_b}""",

    "explain_simple":
    """Explain this financial concept in simple terms that a beginner investor
    would understand. Use an everyday analogy. Keep it under 100 words.
    Concept: {concept}""",
}


# --- Step 2: Build the run_prompt function ---
# TODO: Create a function called run_prompt(template_name, **kwargs)
#   - Look up template_name in prompt_library
#   - If not found, print an error and return None
#   - Fill in the placeholders using .format(**kwargs)
#   - Send to Claude (model="claude-sonnet-5", max_tokens=1024)
#   - Return the text using get_text()
#
# Hint: the function signature is:
#   def run_prompt(template_name, **kwargs):
#
# **kwargs means you can pass any keyword arguments, e.g.:
#   run_prompt("sentiment_analysis", headline="DBS posts record profit")
#   Inside the function, kwargs = {"headline": "DBS posts record profit"}
#   Then: prompt_library[template_name].format(**kwargs)

def run_prompt(template_name, **kwargs):
    if template_name not in prompt_library:
        print(f"Error: template '{template_name}' not found")
        return None

    prompt = prompt_library[template_name].format(**kwargs)

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return get_text(message)


# --- Step 3: Test each template ---
# TODO: Test all 5 templates with real financial data and print results.
#
# Test 1 — Sentiment Analysis:
result1 = run_prompt("sentiment_analysis",
headline="Singtel sells Optus stake for $1.2B to fund 5G expansion")
#
# Test 2 — Risk Assessment:
result2 = run_prompt("risk_assessment",
scenario="A property developer has 60% of revenue from China, debt-to-equity ratio of 1.8, and 3 projects delayed by 6 months")
#
# Test 3 — Earnings Summary:
result3 = run_prompt("earnings_summary",
earnings_data="OCBC Q1 2025: Net profit S$2.1B (+8% YoY), NIM 2.20% (stable), Fee income S$580M (+12%), NPL ratio 1.3%, CET1 15.5%, Dividend S$0.44/share")
#
# Test 4 — Comparison:
result4 = run_prompt("comparison",
option_a="Singapore T-bills yielding 3.5%, risk-free, 6-month lock-in",
option_b="Mapletree Industrial Trust REIT yielding 5.8%, price volatile, quarterly distributions")
#
# Test 5 — Explain Simple:
result5 = run_prompt("explain_simple",
concept="Net Interest Margin (NIM) for banks")
#
# Print each result with a header like:
#   print(f"\n{'=' * 60}")
#   print(f"TEMPLATE: {template_name}")
#   print('=' * 60)
#   print(result)
results_dict = {"result1": result1, "result2": result2, "result3": result3, "result4": result4, "result5": result5}
for fmt, result in results_dict.items():
    print(f"\n{'=' * 60}")
    print(f"FORMAT: {fmt.upper()}")
    print('=' * 60)
    print(result)


# --- Step 4: Save the prompt library ---
# TODO: Save the prompt_library dictionary to "prompt_library.json"
with open("prompt_library.json", "w") as f:
    json.dump({
        "templates": prompt_library,
        "results": {
            "sentiment_analysis": result1,
            "risk_assessment": result2,
            "earnings_summary": result3,
            "comparison": result4,
            "explain_simple": result5
        }
    }, f, indent=2)