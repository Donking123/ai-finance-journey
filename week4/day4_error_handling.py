"""
Week 4 - Day 4: Error Handling & Robustness for Production Pipelines
=====================================================================
Goal: Make the batch processor production-ready with error handling,
      retry logic, input validation, and command-line arguments.
"""

import anthropic
import json
import os
import sys
import time

client = anthropic.Anthropic()

def get_text(message):
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "NO_RESPONSE"


# --- Reuse from previous days ---
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
# PART 1: Build call_with_retry()
# ============================================================
# TODO: Create a function that retries a failed API call up to 3 times.
#
#   def call_with_retry(func, max_retries=3):
#       for attempt in range(max_retries):
#           try:
#               return func()
#           except anthropic.APIError as e:
#               print(f"    Retry {attempt + 1}/{max_retries}: {e}")
#               time.sleep(2)
#       return None
#
# How it works:
#   - func is a function to call (passed without parentheses)
#   - try: attempts to call func()
#   - except: if it fails with an API error, wait 2 seconds and retry
#   - After 3 failures, give up and return None
#
# Usage:
#   result = call_with_retry(lambda: extract_metrics(doc["content"]))
#
# New concept — lambda:
#   lambda is a mini function with no name. These two are the same:
#     lambda: extract_metrics(doc["content"])
#     def do_it(): return extract_metrics(doc["content"])

def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except anthropic.APIError as e:
            print(f"    Retry {attempt + 1}/{max_retries}: {e}")
            time.sleep(2)
    return None


# ============================================================
# PART 2: Build validate_document()
# ============================================================
# TODO: Create a function that checks if a document is valid before processing.
#
#   def validate_document(doc):
#       if not doc["content"].strip():
#           return False, "File is empty"
#       if len(doc["content"]) > 10000:
#           return False, f"File too large ({len(doc['content'])} chars, max 10000)"
#       return True, "OK"
#
# This returns TWO values (a tuple):
#   valid, reason = validate_document(doc)
#   if not valid:
#       print(f"Skipping {doc['filename']}: {reason}")

def validate_document(doc):
    if not doc["content"].strip():
        return False, "File is empty"
    if len(doc["content"]) > 10000:
        return False, f"File too large ({len(doc['content'])} chars, max 10000)"
    return True, "OK"



# ============================================================
# PART 3: Build analyze_document_safe() — pipeline with error handling
# ============================================================
# TODO: Create a function that runs the full pipeline with retries
#   and error handling. If any step fails, save partial results.
#
#   def analyze_document_safe(doc):
#       total_input_tokens = 0
#       total_output_tokens = 0
#       step1_text = None
#       step2_text = None
#       step3_text = None
#
#       # Step 1: Extract (with retry)
#       msg1 = call_with_retry(lambda: extract_metrics(doc["content"]))
#       if msg1 is None:
#           return {"filename": doc["filename"], "error": "Extract failed after retries",
#                   "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cost": 0}
#       step1_text = get_text(msg1)
#       total_input_tokens += msg1.usage.input_tokens
#       total_output_tokens += msg1.usage.output_tokens
#
#       # Step 2: Analyze (with retry)
#       msg2 = call_with_retry(lambda: analyze_metrics(step1_text))
#       if msg2 is None:
#           return {"filename": doc["filename"], "error": "Analyze failed after retries",
#                   "extract": step1_text,
#                   "input_tokens": total_input_tokens, "output_tokens": total_output_tokens,
#                   "total_tokens": total_input_tokens + total_output_tokens,
#                   "cost": (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000)}
#       step2_text = get_text(msg2)
#       total_input_tokens += msg2.usage.input_tokens
#       total_output_tokens += msg2.usage.output_tokens
#
#       # Step 3: Summarize (with retry)
#       msg3 = call_with_retry(lambda: summarize_analysis(step2_text))
#       if msg3 is None:
#           return {"filename": doc["filename"], "error": "Summarize failed after retries",
#                   "extract": step1_text, "analysis": step2_text,
#                   "input_tokens": total_input_tokens, "output_tokens": total_output_tokens,
#                   "total_tokens": total_input_tokens + total_output_tokens,
#                   "cost": (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000)}
#       step3_text = get_text(msg3)
#       total_input_tokens += msg3.usage.input_tokens
#       total_output_tokens += msg3.usage.output_tokens
#
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

def analyze_document_safe(doc):
    total_input_tokens = 0
    total_output_tokens = 0
    step1_text = None
    step2_text = None
    step3_text = None

    # Step 1: Extract (with retry)

    msg1 = call_with_retry(lambda: extract_metrics(doc["content"]))
    if msg1 is None:
        return {"filename": doc["filename"], "error": "Extract failed after retries",
                "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cost": 0}

    step1_text = get_text(msg1)
    total_input_tokens += msg1.usage.input_tokens
    total_output_tokens += msg1.usage.output_tokens

    # Step 2: Analyze (with retry)
    msg2 = call_with_retry(lambda: analyze_metrics(step1_text))
    if msg2 is None:
        return {"filename": doc["filename"], "error": "Analyze failed after retries",
                "extract": step1_text,
                "input_tokens": total_input_tokens, "output_tokens": total_output_tokens,
                "total_tokens": total_input_tokens + total_output_tokens,
                "cost": (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000)}
    step2_text = get_text(msg2)
    total_input_tokens += msg2.usage.input_tokens
    total_output_tokens += msg2.usage.output_tokens
    
    # Step 3: Summarize (with retry)
    msg3 = call_with_retry(lambda: summarize_analysis(step2_text))
    if msg3 is None:
        return {"filename": doc["filename"], "error": "Summarize failed after retries",
                "extract": step1_text, "analysis": step2_text,
                "input_tokens": total_input_tokens, "output_tokens": total_output_tokens,
                "total_tokens": total_input_tokens + total_output_tokens,
                "cost": (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000)}
    step3_text = get_text(msg3)
    total_input_tokens += msg3.usage.input_tokens
    total_output_tokens += msg3.usage.output_tokens

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
# PART 4: Main script with sys.argv support
# ============================================================
# TODO: Build the main script that either processes one file or all files.
#
#   # Check for command-line argument
#   if len(sys.argv) > 1:
#       # Process a single file: python3 day4.py data/dbs_q1_2025.txt
#       target_file = sys.argv[1]
#       if not os.path.exists(target_file):
#           print(f"Error: file '{target_file}' not found")
#           sys.exit(1)
#       with open(target_file, "r") as f:
#           content = f.read()
#       doc = {"filename": os.path.basename(target_file), "content": content,
#              "lines": len(content.splitlines())}
#       docs = [doc]
#   else:
#       # Process all files in data/
#       docs = load_documents("data")
#
#   # Run batch processing with validation
#   results = []
#   skipped = []
#
#   print(f"Processing {len(docs)} document(s)...\n")
#
#   for i, doc in enumerate(docs, 1):
#       # Validate first
#       valid, reason = validate_document(doc)
#       if not valid:
#           print(f"[{i}/{len(docs)}] SKIP: {doc['filename']} — {reason}")
#           skipped.append({"filename": doc["filename"], "reason": reason})
#           continue
#
#       print(f"[{i}/{len(docs)}] Processing: {doc['filename']}...")
#       result = analyze_document_safe(doc)
#
#       if "error" in result:
#           print(f"         ERROR: {result['error']}")
#       else:
#           print(f"         Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")
#
#       results.append(result)
#
#   # Print summary
#   print(f"\n{'=' * 70}")
#   print("BATCH PROCESSING COMPLETE")
#   print(f"{'=' * 70}")
#   print(f"  Processed: {len(results)}")
#   print(f"  Skipped:   {len(skipped)}")
#   print(f"  Errors:    {len([r for r in results if 'error' in r])}")
#
#   grand_total_tokens = sum(r.get("total_tokens", 0) for r in results)
#   grand_total_cost = sum(r.get("cost", 0) for r in results)
#   print(f"  Tokens:    {grand_total_tokens:,}")
#   print(f"  Cost:      ${grand_total_cost:.4f}")
#
#   # Save results (even partial ones)
#   with open("batch_results_safe.json", "w") as f:
#       json.dump({"results": results, "skipped": skipped}, f, indent=2)
#   print(f"\nResults saved to batch_results_safe.json")


# Check for command-line argument
if len(sys.argv) > 1:
    # Process a single file: python3 day4.py data/dbs_q1_2025.txt
    target_file = sys.argv[1]
    if not os.path.exists(target_file):
        print(f"Error: file '{target_file}' not found")
        sys.exit(1)
    with open(target_file, "r") as f:
        content = f.read()
    doc = {"filename": os.path.basename(target_file), "content": content,
            "lines": len(content.splitlines())}
    docs = [doc]
else:
    # Process all files in data/
    docs = load_documents("data")

#Run batch processing with validation
results = []
skipped = []

print(f"Processing {len(docs)} document(s)...\n")

for i, doc in enumerate(docs, 1):
    # Validate first
    valid, reason = validate_document(doc)
    if not valid:
        print(f"[{i}/{len(docs)}] SKIP: {doc['filename']} — {reason}")
        skipped.append({"filename": doc["filename"], "reason": reason})
        continue

    print(f"[{i}/{len(docs)}] Processing: {doc['filename']}...")
    result = analyze_document_safe(doc)

    if "error" in result:
        print(f"         ERROR: {result['error']}")
    else:
        print(f"         Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")

    results.append(result)


# Print summary
print(f"\n{'=' * 70}")
print("BATCH PROCESSING COMPLETE")
print(f"{'=' * 70}")
print(f"  Processed: {len(results)}")
print(f"  Skipped:   {len(skipped)}")
print(f"  Errors:    {len([r for r in results if 'error' in r])}")

grand_total_tokens = sum(r.get("total_tokens", 0) for r in results)
grand_total_cost = sum(r.get("cost", 0) for r in results)
print(f"  Tokens:    {grand_total_tokens:,}")
print(f"  Cost:      ${grand_total_cost:.4f}")


# Save results (even partial ones)
with open("batch_results_safe.json", "w") as f:
    json.dump({"results": results, "skipped": skipped}, f, indent=2)
print(f"\nResults saved to batch_results_safe.json")