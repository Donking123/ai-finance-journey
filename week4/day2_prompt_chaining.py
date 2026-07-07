"""
Week 4 - Day 2: Prompt Chaining — Chain Multiple Prompts Together
==================================================================
Goal: Run a document through a 3-step pipeline where each step's
      output feeds into the next step.
      Step 1: Extract key metrics as JSON
      Step 2: Analyze strengths and concerns
      Step 3: Write an executive summary
"""

import anthropic
import json
import os

client = anthropic.Anthropic()

def get_text(message):
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "NO_RESPONSE"


# --- Reuse load_documents from Day 1 ---
def load_documents(folder_path):
    documents = []
    files = os.listdir(folder_path)
    txt_files = [f for f in files if f.endswith(".txt")]

    for filename in txt_files:
        full_path = os.path.join(folder_path, filename)
        with open(full_path, "r") as f:
            content = f.read()
        documents.append({
            "filename": filename,
            "content": content,
            "lines": len(content.splitlines())
        })

    return documents


# ============================================================
# PART 1: Load the earnings document
# ============================================================
# TODO: Use load_documents("data") to load all documents,
#   then find the earnings file (dbs_q1_2025.txt).
#
#   docs = load_documents("data")
#   earnings_doc = None
#   for doc in docs:
#       if "dbs" in doc["filename"]:
#           earnings_doc = doc
#           break
#   print(f"Loaded: {earnings_doc['filename']} ({earnings_doc['lines']} lines)\n")

docs = load_documents("data")
earnings_doc = None
for doc in docs:
    if "dbs" in doc["filename"]:
        earnings_doc = doc
        break
print(f"Loaded: {earnings_doc['filename']} ({earnings_doc['lines']} lines)\n")

# ============================================================
# PART 2: Step 1 — Extract key metrics as JSON
# ============================================================
# TODO: Send the earnings document to Claude and ask it to extract
#   key financial metrics as structured JSON.
#
#   Create a function called extract_metrics(document_text):
#       - Sends this prompt to Claude:
#           "Extract all key financial metrics from this earnings report.
#            Return ONLY valid JSON with this structure:
#            {{"company": "...", "quarter": "...",
#              "metrics": [
#                {{"name": "...", "value": "...", "prior_period": "...", "change": "..."}},
#                ...
#              ]
#            }}
#            Document: {document_text}"
#       - Use model="claude-sonnet-5", max_tokens=1024
#       - Return the text using get_text()
#
#   Call it: step1_result = extract_metrics(earnings_doc["content"])
#   Print: print("STEP 1 — EXTRACT METRICS")
#          print("=" * 60)
#          print(step1_result)
#          print()

def extract_metrics(document_text):
    message = client.messages.create(
        model = "claude-sonnet-5",
        max_tokens= 1024,
        messages=[{"role": "user", "content": f"""Extract all key financial metrics from this earnings report.
Return ONLY valid JSON with this structure:
{{"company": "...", "quarter": "...",
  "metrics": [
    {{"name": "...", "value": "...", "prior_period": "...", "change": "..."}},
    ...
  ]
}}
Document: {document_text}"""}]
    )
    return get_text(message)

step1_result = extract_metrics(earnings_doc["content"])

print("STEP 1 — EXTRACT METRICS")
print("=" * 60)
print(step1_result)
print()


# ============================================================
# PART 3: Step 2 — Analyze strengths and concerns
# ============================================================
# TODO: Feed Step 1's output into a NEW prompt that analyzes it.
#   This is the "chaining" — Step 2 uses Step 1's result.
#
#   Create a function called analyze_metrics(metrics_json):
#       - Sends this prompt to Claude:
#           "Given these extracted financial metrics, provide an analysis.
#            Identify:
#            1. Top 3 strengths (with specific numbers)
#            2. Top 3 concerns (with specific numbers)
#            3. One key trend to watch
#            Be specific and reference the actual numbers.
#            Metrics: {metrics_json}"
#       - Use model="claude-sonnet-5", max_tokens=1024
#       - Return the text using get_text()
#
#   Call it: step2_result = analyze_metrics(step1_result)
#   Print with header like Step 1.

def analyze_metrics(metrics_json):
    message = client.messages.create(
        model = "claude-sonnet-5",
        max_tokens= 1024,
        messages=[{"role": "user", "content": f"""Given these extracted financial metrics, provide an analysis.
Identify:
1. Top 3 strengths (with specific numbers)
2. Top 3 concerns (with specific numbers)
3. One key trend to watch
Be specific and reference the actual numbers.
Metrics: {metrics_json}"""
}]
    )
    return get_text(message)

step2_result = analyze_metrics(step1_result)
print("STEP 2 — ANALYZE METRICS")
print("=" * 60)
print(step2_result)
print()



# ============================================================
# PART 4: Step 3 — Executive summary
# ============================================================
# TODO: Feed Step 2's output into a final prompt for a summary.
#
#   Create a function called summarize_analysis(analysis_text):
#       - Sends this prompt to Claude:
#           "Based on this financial analysis, write a 3-sentence
#            executive summary suitable for a senior portfolio manager.
#            Be concise, specific, and include key numbers.
#            Analysis: {analysis_text}"
#       - Use model="claude-sonnet-5", max_tokens=512
#       - Return the text using get_text()
#
#   Call it: step3_result = summarize_analysis(step2_result)
#   Print with header like Steps 1 and 2.

def summarize_analysis(analysis_text):
    message = client.messages.create(
        model = "claude-sonnet-5",
        max_tokens= 1024,
        messages=[{"role": "user", "content": f"""Based on this financial analysis, write a 3-sentence
executive summary suitable for a senior portfolio manager.
Be concise, specific, and include key numbers.
Analysis: {analysis_text}"""
}]
    )
    return get_text(message)

step3_result = summarize_analysis(step2_result)
print("STEP 3 — EXECUTIVE SUMMARY")
print("=" * 60)
print(step3_result)
print()


# ============================================================
# PART 5: Save the full pipeline result
# ============================================================
# TODO: Save all 3 steps to "pipeline_result.json":
#
#   pipeline_result = {
#       "document": earnings_doc["filename"],
#       "step1_extract": step1_result,
#       "step2_analyze": step2_result,
#       "step3_summary": step3_result
#   }
#   with open("pipeline_result.json", "w") as f:
#       json.dump(pipeline_result, f, indent=2)
#   print("Pipeline result saved to pipeline_result.json")

pipeline_result = {
    "document": earnings_doc["filename"],
    "step1_extract": step1_result,
    "step2_analyze": step2_result,
    "step3_summary": step3_result
}

with open("pipeline_result.json", "w") as f:
    json.dump(pipeline_result, f, indent=2)
print("Pipeline result saved to pipeline_result.json")
