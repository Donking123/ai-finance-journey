"""
Week 3 - Day 4: Output Formatting — Control Exactly What Claude Returns
========================================================================
Goal: Same financial data, 4 different output formats.
      Learn to control Claude's response structure through prompt instructions.
"""

import anthropic
import json

client = anthropic.Anthropic()

def get_text(message):
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "NO_RESPONSE"


# --- The financial data we'll analyze in 4 formats ---
company_data = """
Company: DBS Group Holdings (SGX: D05)
Quarter: Q1 2025
Total Income: S$5.42 billion (vs S$5.17B Q1 2024)
Net Profit: S$2.89 billion (vs S$2.96B Q1 2024)
Net Interest Margin: 2.12% (vs 2.14% Q1 2024)
Fee Income: S$1.08 billion (vs S$0.92B Q1 2024)
Cost-to-Income Ratio: 38.9% (vs 39.4% Q1 2024)
Non-Performing Loan Ratio: 1.1% (vs 1.1% Q1 2024)
Common Equity Tier 1 Ratio: 14.8%
Dividend: S$0.60 per share (vs S$0.54 Q1 2024)
"""


# --- Build the formatting function ---
# TODO: Create a function called format_analysis(data, format_type)
#   - It takes two arguments: data (the company_data string) and format_type (a string)
#   - Based on format_type, it sends a different prompt to Claude:
#
#   format_type == "paragraph":
#       "Summarize these quarterly results in one clear paragraph: {data}"
#
#   format_type == "bullets":
#       "Analyze these quarterly results as a structured bullet-point list.
#        Group into: Revenue, Profitability, Risk Metrics, Shareholder Returns.
#        Use sub-bullets for details.
#        Data: {data}"
#
#   format_type == "json":
#       "Analyze these quarterly results and return ONLY valid JSON with this structure:
#        {{\"company\": \"...\", \"quarter\": \"...\", \"highlights\": [...], \"concerns\": [...],
#          \"metrics\": {{\"revenue_growth\": \"...\", \"profit_growth\": \"...\", \"nim_change\": \"...\"}},
#          \"outlook\": \"...\"}}
#        Data: {data}"
#
#   format_type == "table":
#       "Analyze these quarterly results as a markdown table with columns:
#        | Metric | Q1 2025 | Q1 2024 | YoY Change | Assessment |
#        Include all key metrics from the data.
#        Data: {data}"
#
#   - Use model="claude-sonnet-5", max_tokens=1024
#   - Return the text using get_text()

def format_analysis(data, format_type):
    if format_type == "paragraph":
        prompt = f"Summarize these quarterly results in one clear paragraph: {data}"
    elif format_type == "bullets":
        prompt = f"""Analyze these quarterly results as a structured bullet-point list.
Group into: Revenue, Profitability, Risk Metrics, Shareholder Returns.
Use sub-bullets for details.
Data: {data}"""
    elif format_type == "json":
        prompt = f"""Analyze these quarterly results and return ONLY valid JSON with this structure:
{{"company": "...", "quarter": "...", "highlights": [...], "concerns": [...],
"metrics": {{"revenue_growth": "...", "profit_growth": "...", "nim_change": "..."}},
"outlook": "..."}}
Data: {data}"""
    elif format_type == "table":
        prompt = f"""Analyze these quarterly results as a markdown table with columns:
| Metric | Q1 2025 | Q1 2024 | YoY Change | Assessment |
Include all key metrics from the data.
Data: {data}"""

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return get_text(message)





# --- Run all 4 formats ---
# TODO: Call format_analysis() for each format type and store results:
#   paragraph_result = format_analysis(company_data, "paragraph")
#   bullets_result   = format_analysis(company_data, "bullets")
#   json_result      = format_analysis(company_data, "json")
#   table_result     = format_analysis(company_data, "table")

paragraph_result = format_analysis(company_data, "paragraph")
bullets_result   = format_analysis(company_data, "bullets")
json_result      = format_analysis(company_data, "json")
table_result     = format_analysis(company_data, "table")

results_dict = {"paragraph": paragraph_result, "bullets": bullets_result, "json": json_result, "table": table_result}
for fmt, result in results_dict.items():
    print(f"\n{'=' * 60}")
    print(f"FORMAT: {fmt.upper()}")
    print('=' * 60)
    print(result)



# --- Save results ---
# TODO: Save all 4 results to "format_comparison.json"
results = {
    "company": "DBS Group Holdings",
    "quarter": "Q1 2025",
    "formats": {
        "paragraph": paragraph_result,
        "bullets": bullets_result,
        "json": json_result,
        "table": table_result
    }
}
with open("format_comparison.json", "w") as f:
    json.dump(results, f, indent=2)
