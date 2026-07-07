"""
Week 4 - Day 3: Batch Processing — Analyze Multiple Documents Automatically
=============================================================================
Goal: Run the Day 2 pipeline on ALL documents in the data/ folder.
      Track tokens and cost across the entire batch.
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


# --- Reuse pipeline functions from Day 2 ---
def extract_metrics(document_text):
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"""Extract all key financial metrics from this document.
Return ONLY valid JSON with this structure:
{{"document_type": "...", "subject": "...",
  "metrics": [
    {{"name": "...", "value": "...", "prior_period": "...", "change": "..."}},
    ...
  ]
}}
Document: {document_text}"""}]
    )
    return message

def analyze_metrics(metrics_json):
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"""Given these extracted financial metrics, provide an analysis.
Identify:
1. Top 3 strengths (with specific numbers)
2. Top 3 concerns (with specific numbers)
3. One key trend to watch
Be specific and reference the actual numbers.
Metrics: {metrics_json}"""}]
    )
    return message

def summarize_analysis(analysis_text):
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=512,
        messages=[{"role": "user", "content": f"""Based on this financial analysis, write a 3-sentence
executive summary suitable for a senior portfolio manager.
Be concise, specific, and include key numbers.
Analysis: {analysis_text}"""}]
    )
    return message


# ============================================================
# PART 1: Build analyze_document() — runs the full pipeline on one doc
# ============================================================
# TODO: Create a function called analyze_document(doc)
#   - Takes a document dict ({"filename": ..., "content": ..., "lines": ...})
#   - Runs all 3 pipeline steps
#   - Tracks tokens and cost across all 3 steps
#   - Returns a result dictionary
#
#   def analyze_document(doc):
#       total_input_tokens = 0
#       total_output_tokens = 0
#
#       # Step 1: Extract
#       msg1 = extract_metrics(doc["content"])
#       step1_text = get_text(msg1)
#       total_input_tokens += msg1.usage.input_tokens
#       total_output_tokens += msg1.usage.output_tokens
#
#       # Step 2: Analyze
#       msg2 = analyze_metrics(step1_text)
#       step2_text = get_text(msg2)
#       total_input_tokens += msg2.usage.input_tokens
#       total_output_tokens += msg2.usage.output_tokens
#
#       # Step 3: Summarize
#       msg3 = summarize_analysis(step2_text)
#       step3_text = get_text(msg3)
#       total_input_tokens += msg3.usage.input_tokens
#       total_output_tokens += msg3.usage.output_tokens
#
#       # Calculate cost (claude-sonnet-5: $3/M input, $15/M output)
#       cost = (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000)
#
#       return {
#           "filename": doc["filename"],
#           "extract": step1_text,
#           "analysis": step2_text,
#           "summary": step3_text,
#           "input_tokens": total_input_tokens,
#           "output_tokens": total_output_tokens,
#           "total_tokens": total_input_tokens + total_output_tokens,
#           "cost": cost
#       }
#
# Notice: The pipeline functions now return the full message object
# (not just text) so we can access both .usage and the text.

def analyze_document(doc):
    total_input_tokens = 0
    total_output_tokens = 0

    # Step 1: Extract
    msg1 = extract_metrics(doc["content"])
    step1_text = get_text(msg1)
    total_input_tokens += msg1.usage.input_tokens
    total_output_tokens += msg1.usage.output_tokens


    # Step 2: Analyze
    msg2 = analyze_metrics(step1_text)
    step2_text = get_text(msg2)
    total_input_tokens += msg2.usage.input_tokens
    total_output_tokens += msg2.usage.output_tokens

    # Step 3: Summarize
    msg3 = summarize_analysis(step2_text)
    step3_text = get_text(msg3)
    total_input_tokens += msg3.usage.input_tokens
    total_output_tokens += msg3.usage.output_tokens

    # Calculate cost (claude-sonnet-5: $3/M input, $15/M output)
    cost = (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000)

    return {
        "filename": doc["filename"],
        "extract": step1_text,
        "analysis": step2_text,
        "summary": step3_text,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "cost": cost
    }


# ============================================================
# PART 2: Batch process all documents
# ============================================================
# TODO: Load all documents and run the pipeline on each one.
#
#   docs = load_documents("data")
#   results = []
#
#   print(f"Processing {len(docs)} documents...\n")
#
#   for i, doc in enumerate(docs, 1):
#       print(f"[{i}/{len(docs)}] Processing: {doc['filename']}...")
#       result = analyze_document(doc)
#       results.append(result)
#       print(f"         Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")
#
# New concept — enumerate(docs, 1):
#   Gives you both the index (starting from 1) and the item.
#   enumerate(["a","b","c"], 1) → (1,"a"), (2,"b"), (3,"c")

docs = load_documents("data")
results = []

print(f"Processing {len(docs)} documents...\n")

for i, doc in enumerate(docs, 1):
    print(f"[{i}/{len(docs)}] Processing: {doc['filename']}...")
    result = analyze_document(doc)
    results.append(result)
    print(f"         Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")


# ============================================================
# PART 3: Print summary table
# ============================================================
# TODO: Print a table showing results for all documents.
#
#   print(f"\n{'=' * 70}")
#   print("BATCH PROCESSING COMPLETE")
#   print(f"{'=' * 70}")
#   print(f"{'File':<30} | {'Tokens':>10} | {'Cost':>10} | Status")
#   print(f"{'-' * 70}")
#
#   grand_total_tokens = 0
#   grand_total_cost = 0
#
#   for r in results:
#       print(f"{r['filename']:<30} | {r['total_tokens']:>10,} | ${r['cost']:>9.4f} | Done")
#       grand_total_tokens += r['total_tokens']
#       grand_total_cost += r['cost']
#
#   print(f"{'-' * 70}")
#   print(f"{'TOTAL':<30} | {grand_total_tokens:>10,} | ${grand_total_cost:>9.4f} |")
#
# New concepts:
#   f"{text:<30}"   — left-align in 30 characters
#   f"{num:>10,}"   — right-align in 10 characters, with comma separators
#   f"${cost:>9.4f}" — right-align, 4 decimal places

print(f"\n{'=' * 70}")
print("BATCH PROCESSING COMPLETE")
print(f"{'=' * 70}")
print(f"{'File':<30} | {'Tokens':>10} | {'Cost':>10} | Status")
print(f"{'-' * 70}")

grand_total_tokens = 0
grand_total_cost = 0

for r in results:
    print(f"{r['filename']:<30} | {r['total_tokens']:>10,} | ${r['cost']:>9.4f} | Done")
    grand_total_tokens += r['total_tokens']
    grand_total_cost += r['cost']

print(f"{'-' * 70}")
print(f"{'TOTAL':<30} | {grand_total_tokens:>10,} | ${grand_total_cost:>9.4f} |")




# ============================================================
# PART 4: Save all results
# ============================================================
# TODO: Save all results to "batch_results.json"
#
#   with open("batch_results.json", "w") as f:
#       json.dump(results, f, indent=2)
#   print(f"\nResults saved to batch_results.json")

with open("batch_results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to batch_results.json")