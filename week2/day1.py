import anthropic
import json

client = anthropic.Anthropic()


headlines = [
    "DBS Group reports record Q2 profit of $2.9 billion, beats analyst expectations",
    "Singtel warns of potential 15% revenue decline amid fierce competition",
    "MAS holds interest rates steady, signals cautious outlook for Singapore economy"
]

results = []

for headline in headlines:
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"""Analyze this financial headline. Return exactly:
Sentiment: [positive/negative/neutral]
Entities: [list]
Summary: [one sentence]
             
Headline: {headline}"""}
        ]
    )

    analysis = message.content[0].text
    print(f"Headline: {headline}")
    print(analysis)
    print("-" * 50)

    results.append({
        "headline": headline,
        "analysis": analysis,
    })

with open("headline_analysis.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved to headline_analysis.json")
