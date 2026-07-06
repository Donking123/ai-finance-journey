"""
Week 2 - Saturday Power Day: Financial News Analyzer
=====================================================
Goal: Combine everything from this week into one real tool.
      API calls + JSON prompts + system prompts + error handling + cost tracking
"""

import anthropic
import json

client = anthropic.Anthropic()

# --- System prompt (Day 3 skill) ---
system_prompt = "You are a senior financial analyst at a Singapore investment bank. You analyze headlines with precision and return only valid JSON."

# --- 10 headlines: mix of SG, US, and global news ---
headlines = [
    "DBS Group reports record Q2 profit of $2.9 billion, beats analyst expectations",
    "Singtel warns of potential 15% revenue decline amid fierce competition",
    "MAS holds interest rates steady, signals cautious outlook for Singapore economy",
    "Sea Limited stock surges 20% after surprise profitable quarter",
    "Grab Holdings announces $500M share buyback program amid investor pressure",
    "Tesla shares drop 8% after missing Q3 delivery targets",
    "NVIDIA hits $3 trillion market cap as AI chip demand soars",
    "China cuts interest rates to boost slowing economic growth",
    "CapitaLand Investment acquires Tokyo office tower for $800M",
    "Oil prices surge 15% as OPEC announces surprise production cuts",
]

# --- Track totals (Day 5 skill) ---
total_input_tokens = 0
total_output_tokens = 0
results = []


# --- Process each headline (Day 1 + 2 + 3 + 5 skills) ---
# TODO: Loop through headlines using enumerate
# For each headline:
#   1. Wrap in try/except (Day 5)
#   2. Call Claude with system prompt (Day 3) and JSON prompt (Day 2)
#      Ask Claude to return ONLY valid JSON with this structure:
#      {
#        "sentiment": "positive/negative/neutral",
#        "confidence": 0.0 to 1.0,
#        "sector": "finance/tech/property/energy/telecom/macro",
#        "region": "Singapore/US/Global/Asia",
#        "key_entities": ["list"],
#        "market_impact": "one sentence",
#        "action": "buy_signal/sell_signal/hold/monitor"
#      }
#   3. Parse the JSON response (clean markdown wrapper if needed)
#   4. Track tokens
#   5. Append parsed data (not raw text) to results
#   6. Print progress



# --- Generate summary report ---
# TODO: Count sentiments
# positive_count = number of results where sentiment == "positive"
# negative_count = ...
# neutral_count = ...



# TODO: Group by sector
# Create a dictionary where key = sector, value = list of headlines in that sector



# TODO: Group by region
# Same as sector grouping but by region



# TODO: Find buy/sell signals
# Filter results where action == "buy_signal" or "sell_signal"



# --- Print the report ---
# TODO: Print a formatted report with:
#   - Sentiment summary (X positive, Y negative, Z neutral)
#   - Headlines grouped by sector
#   - Headlines grouped by region
#   - Any buy/sell signals flagged
#   - Cost summary (tokens used, estimated cost)



# --- Save everything ---
# TODO: Save results to "news_report.json"
