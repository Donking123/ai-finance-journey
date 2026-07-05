import anthropic
import json

client = anthropic.Anthropic()

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

for i, headline in enumerate(headlines):
    try:
        message = client.messages.create(
            model = "claude-sonnet-5",
            max_tokens = 1024,
            system = system_prompt,
            messages = [
                {"role": "user", "content": f"""Analyze this financial headline. Return ONLY valid JSON, no other text.
Use this exact structure:
{{
  "sentiment": "positive or negative or neutral",
  "confidence": 0.0 to 1.0,
  "sector": "finance or tech or property or energy or telecom or macro",
  "region": "Singapore or US or Global or Asia",
  "key_entities": ["list", "of", "entities"],
  "market_impact": "one sentence",
  "action": "buy_signal or sell_signal or hold or monitor"
}}
                 
Headline: {headline}"""}
            ]
        )

        reply = next(block.text for block in message.content if block.type == "text")
        clean_json = reply.strip().removeprefix("```json").removesuffix("```").strip()
        data = json.loads(clean_json)
        data["headline"] = headline

        total_input_tokens += message.usage.input_tokens
        total_output_tokens += message.usage.output_tokens

        results.append(data)
        print(f"[{i+1}/{len(headlines)}] {data['sentiment'].upper():8s} | {headline[:60]}...")
        
    except anthropic.APIError as e:
        print(f"[{i+1}/{len(headlines)}] ERROR: {e}")
    except json.JSONDecodeError:
        print(f"[{i+1}/{len(headlines)}] JSON PARSE ERROR on: {headline[:40]}...")

# --- Generate summary report ---
positive_count = sum(1 for r in results if r["sentiment"] == "positive")
negative_count = sum(1 for r in results if r["sentiment"] == "negative")
neutral_count = sum(1 for r in results if r["sentiment"] == "neutral")

# TODO: Group by sector
sectors = {}
for r in results:
    sector = r["sector"]
    if sector not in sectors:
        sectors[sector] = []
    sectors[sector].append(r["headline"])

# Group by region
regions = {}
for r in results:
    region = r["region"]
    if region not in regions:
        regions[region] = []
    regions[region].append(r["headline"])

buy_signals = [r for r in results if r["action"] == "buy_signal"]
sell_signals = [r for r in results if r["action"] == "sell_signal"]

print("\n" + "=" * 60)
print("FINANCIAL NEWS ANALYSIS REPORT")
print("=" * 60)

print(f"\nSENTIMENT SUMMARY:")
print(f"  Positive: {positive_count}")
print(f"  Negative: {negative_count}")
print(f"  Neutral:  {neutral_count}")

print(f"\nBY SECTOR:")
for sector, items in sectors.items():
    print(f"\n  {sector.upper()}:")
    for item in items:
        print(f"    - {item}")

print(f"\nBY REGION:")
for region, items in regions.items():
    print(f"\n  {region.upper()}:")
    for item in items:
        print(f"    - {item}")

print(f"\nSIGNALS:")
for s in buy_signals:
    print(f"  BUY:  {s['headline']}")
for s in sell_signals:
    print(f"  SELL: {s['headline']}")
if not buy_signals and not sell_signals:
    print("  No strong signals detected.")

input_cost = total_input_tokens * (3.00 / 1_000_000)
output_cost = total_output_tokens * (15.00 / 1_000_000)
total_cost = input_cost + output_cost

print(f"\nCOST:")
print(f"  Headlines: {len(results)}/{len(headlines)}")
print(f"  Tokens: {total_input_tokens} in / {total_output_tokens} out")
print(f"  Estimated cost: ${total_cost:.6f}")

with open("news_report.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved to news_report.json")


