"""
Week 2 - Day 3: System Prompts — Giving Claude a Role
======================================================
Goal: Learn how system prompts change Claude's personality and perspective.
      Same headline, 3 different roles, 3 different analyses.
"""

import anthropic
import json

client = anthropic.Anthropic()

headline = "Singapore's office REIT vacancy rates hit 12%, highest since 2020 amid remote work shift"

# --- Define 3 roles ---
roles = [
    "You are a conservative risk analyst at a Singapore bank. You focus on downside risks and always warn about potential losses.",
    "You are an aggressive hedge fund trader. You look for opportunities others miss and focus on how to profit from any situation.",
    "You are a financial journalist writing for The Straits Times. You explain news clearly for everyday Singaporean readers.",
]

role_names = ["Risk Analyst", "Hedge Fund Trader", "Journalist"]


# --- Function to analyze with a given role ---
# TODO: Create a function called analyze_as(role, headline) that:
#   1. Calls client.messages.create() with:
#      - model="claude-sonnet-5"
#      - max_tokens=1024
#      - system=role          <-- THIS IS NEW! Sets Claude's persona
#      - messages=[{"role": "user", "content": f"Analyze this headline: {headline}"}]
#   2. Returns the text response
def analyze_as(role, headline):
    message = client.messages.create(
        model = "claude-sonnet-5",
        max_tokens = 1024,
        system = role,
        messages = [
            {"role":"user", "content": f"Analyze this headline: {headline}"}
        ]
    )
    return next(block.text for block in message.content if block.type == "text")

results = []
for role, name in zip(roles, role_names):
    analysis = analyze_as(role, headline)
    print("=" * 60)
    print(f"ROLE: {name}")
    print("=" * 60)
    print(analysis)
    print()
    results.append({"role": name, "analysis": analysis})

with open("role_analysis.json", "w") as f:
    json.dump(results, f, indent=2)
print("Save to role_analysis.json")
