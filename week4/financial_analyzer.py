"""
Week 4 - Saturday Project: Financial Document Analyzer
=======================================================
Goal: Combine everything from Week 4 into one interactive tool.
      - Day 1: File loading
      - Day 2: Prompt chaining (3-step pipeline)
      - Day 3: Batch processing
      - Day 4: Error handling, retry, validation, sys.argv
      - Day 5: Report generation (markdown + HTML + browser)

Usage:
      python3 financial_analyzer.py              → interactive menu
      python3 financial_analyzer.py data/file.txt → analyze one file
"""

import anthropic
import json
import os
import sys
import time
import webbrowser
from datetime import datetime

client = anthropic.Anthropic()


def get_text(message):
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "NO_RESPONSE"


# ============================================================
# PART 1: Reusable functions (from Days 1-4)
# ============================================================
# TODO: Copy these functions from your previous exercises.
#       These are all functions you've already written!
#
# 1a) load_documents(folder_path) — from Day 1
#     Returns a list of {"filename", "content", "lines"} dicts
#
#   def load_documents(folder_path):
#       documents = []
#       files = os.listdir(folder_path)
#       txt_files = [f for f in files if f.endswith(".txt")]
#       for filename in txt_files:
#           full_path = os.path.join(folder_path, filename)
#           with open(full_path, "r") as f:
#               content = f.read()
#           documents.append({
#               "filename": filename,
#               "content": content,
#               "lines": len(content.splitlines())
#           })
#       return documents

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

#
#
# 1b) validate_document(doc) — from Day 4
#     Returns (True, "OK") or (False, "reason")
#
#   def validate_document(doc):
#       if not doc["content"].strip():
#           return False, "File is empty"
#       if len(doc["content"]) > 10000:
#           return False, f"File too large ({len(doc['content'])} chars, max 10000)"
#       return True, "OK"
#

def validate_document(doc):
    if not doc["content"].strip():
        return False, "File is empty"
    if len(doc["content"]) > 10000:
        return False, f"File too large ({len(doc['content'])} chars, max 10000)"
    return True, "OK"


#
# 1c) call_with_retry(func, max_retries=3) — from Day 4
#     Retries API calls up to 3 times
#
#   def call_with_retry(func, max_retries=3):
#       for attempt in range(max_retries):
#           try:
#               return func()
#           except anthropic.APIError as e:
#               print(f"    Retry {attempt + 1}/{max_retries}: {e}")
#               time.sleep(2)
#       return None

def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except anthropic.APIError as e:
            print(f"    Retry {attempt + 1}/{max_retries}: {e}")
            time.sleep(2)
    return None

#
#
# 1d) The 3 pipeline functions — from Day 2
#     extract_metrics(text), analyze_metrics(text), summarize_analysis(text)
#     Each returns the full message object (not just text)
#
#   def extract_metrics(document_text):
#       message = client.messages.create(
#           model="claude-sonnet-5",
#           max_tokens=1024,
#           messages=[{"role": "user", "content": f"""Extract all key financial metrics from this document.
#   Return ONLY valid JSON with this structure:
#   {{"document_type": "...", "subject": "...",
#     "metrics": [
#       {{"name": "...", "value": "...", "prior_period": "...", "change": "..."}},
#       ...
#     ]
#   }}
#   Document: {document_text}"""}]
#       )
#       return message

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

#
#   def analyze_metrics(metrics_json):
#       message = client.messages.create(
#           model="claude-sonnet-5",
#           max_tokens=1024,
#           messages=[{"role": "user", "content": f"""Given these extracted financial metrics, provide an analysis.
#   Identify:
#   1. Top 3 strengths (with specific numbers)
#   2. Top 3 concerns (with specific numbers)
#   3. One key trend to watch
#   Be specific and reference the actual numbers.
#   Metrics: {metrics_json}"""}]
#       )
#       return message

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
    return message

#
#   def summarize_analysis(analysis_text):
#       message = client.messages.create(
#           model="claude-sonnet-5",
#           max_tokens=512,
#           messages=[{"role": "user", "content": f"""Based on this financial analysis, write a 3-sentence
#   executive summary suitable for a senior portfolio manager.
#   Be concise, specific, and include key numbers.
#   Analysis: {analysis_text}"""}]
#       )
#       return message

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
    return message

#
#
# 1e) analyze_document_safe(doc) — from Day 4
#     Runs the full pipeline with retry + error handling
#     Returns a result dict with all fields + cost tracking
#
#   def analyze_document_safe(doc):
#       total_input_tokens = 0
#       total_output_tokens = 0
#
#       msg1 = call_with_retry(lambda: extract_metrics(doc["content"]))
#       if msg1 is None:
#           return {"filename": doc["filename"], "error": "Extract failed after retries",
#                   "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cost": 0}
#       step1_text = get_text(msg1)
#       total_input_tokens += msg1.usage.input_tokens
#       total_output_tokens += msg1.usage.output_tokens
#
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
# PART 2: Build generate_report() — NEW function
# ============================================================
# TODO: Create a function that takes results + skipped lists
#       and returns a markdown report string. (From Day 5, but as a function)
#
#   def generate_report(results, skipped):
#       now = datetime.now().strftime("%Y-%m-%d %H:%M")
#       total_tokens = sum(r.get("total_tokens", 0) for r in results)
#       total_cost = sum(r.get("cost", 0) for r in results)
#       errors = len([r for r in results if "error" in r])
#
#       report = f"""# Financial Document Analysis Report
#   Generated: {now}
#
#   ## Overview
#   - **Documents analyzed:** {len(results)}
#   - **Documents skipped:** {len(skipped)}
#   - **Errors:** {errors}
#   - **Total tokens used:** {total_tokens:,}
#   - **Total cost:** ${total_cost:.4f}
#
#   ---
#
#   """
#
#       for r in results:
#           if "error" in r:
#               report += f"""## {r['filename']} — ERROR
#   **Error:** {r['error']}
#
#   ---
#
#   """
#           else:
#               report += f"""## {r['filename']}
#   **Tokens:** {r['total_tokens']:,} | **Cost:** ${r['cost']:.4f}
#
#   ### Executive Summary
#   {r['summary']}
#
#   ### Analysis
#   {r['analysis']}
#
#   ### Extracted Metrics
#   {r['extract']}
#
#   ---
#
#   """
#
#       if skipped:
#           report += "## Skipped Documents\n\n"
#           for s in skipped:
#               report += f"- **{s['filename']}**: {s['reason']}\n"
#           report += "\n"
#
#       return report
#
# What's different from Day 5:
#   - Wrapped in a function (reusable!)
#   - Handles error results (shows "ERROR" instead of crashing)
#   - Uses r.get("total_tokens", 0) instead of r["total_tokens"]
#     .get() returns 0 if the key doesn't exist (safe for error results)
#   - Summary shown FIRST (most important info at the top)

def generate_report(results, skipped):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_tokens = sum(r.get("total_tokens", 0) for r in results)
    total_cost = sum(r.get("cost", 0) for r in results)
    errors = len([r for r in results if "error" in r])

    report = f"""# Financial Document Analysis Report
Generated: {now}

## Overview
- **Documents analyzed:** {len(results)}
- **Documents skipped:** {len(skipped)}
- **Errors:** {errors}
- **Total tokens used:** {total_tokens:,}
- **Total cost:** ${total_cost:.4f}

---

"""

    for r in results:
        if "error" in r:
            report += f"""## {r['filename']} — ERROR
**Error:** {r['error']}

---

"""
        else:
            report += f"""## {r['filename']}
**Tokens:** {r['total_tokens']:,} | **Cost:** ${r['cost']:.4f}

### Executive Summary
{r['summary']}

### Analysis
{r['analysis']}

### Extracted Metrics
{r['extract']}

---

"""

    if skipped:
        report += "## Skipped Documents\n\n"
        for s in skipped:
            report += f"- **{s['filename']}**: {s['reason']}\n"
        report += "\n"

    return report



# ============================================================
# PART 3: Build save_html_report() — NEW function
# ============================================================
# TODO: Create a function that converts the markdown report to HTML
#       and saves it. Returns the filename.
#
#   def save_html_report(report):
#       html = """<html>
#   <head>
#       <title>Financial Analysis Report</title>
#       <style>
#           body { font-family: -apple-system, Arial, sans-serif;
#                  max-width: 800px; margin: 40px auto; padding: 0 20px;
#                  line-height: 1.6; color: #333; }
#           h1 { color: #1a6b4a; border-bottom: 2px solid #1a6b4a; padding-bottom: 10px; }
#           h2 { color: #2c5282; margin-top: 30px; }
#           h3 { color: #555; }
#           hr { border: none; border-top: 1px solid #ddd; margin: 30px 0; }
#       </style>
#   </head>
#   <body>
#   """
#
#       for line in report.split("\n"):
#           if line.startswith("# "):
#               html += f"<h1>{line[2:]}</h1>\n"
#           elif line.startswith("## "):
#               html += f"<h2>{line[3:]}</h2>\n"
#           elif line.startswith("### "):
#               html += f"<h3>{line[4:]}</h3>\n"
#           elif line.startswith("- "):
#               html += f"<li>{line[2:]}</li>\n"
#           elif line.startswith("---"):
#               html += "<hr>\n"
#           elif line.strip() == "":
#               html += "<br>\n"
#           else:
#               html += f"<p>{line}</p>\n"
#
#       html += "</body></html>"
#
#       filename = "analysis_report.html"
#       with open(filename, "w") as f:
#           f.write(html)
#       return filename
#
# Note: This is NOT an f-string (no f before """), so { } are just
#       normal CSS braces — no need for {{ }}.
#       We only needed {{ }} in Day 5 because the whole thing was an f-string.

def save_html_report(report):
    html = """<html>
<head>
    <title>Financial Analysis Report</title>
    <style>
        body { font-family: -apple-system, Arial, sans-serif;
                max-width: 800px; margin: 40px auto; padding: 0 20px;
                line-height: 1.6; color: #333; }
        h1 { color: #1a6b4a; border-bottom: 2px solid #1a6b4a; padding-bottom: 10px; }
        h2 { color: #2c5282; margin-top: 30px; }
        h3 { color: #555; }
        hr { border: none; border-top: 1px solid #ddd; margin: 30px 0; }
    </style>
</head>
<body>
"""

    for line in report.split("\n"):
        if line.startswith("# "):
            html += f"<h1>{line[2:]}</h1>\n"
        elif line.startswith("## "):
            html += f"<h2>{line[3:]}</h2>\n"
        elif line.startswith("### "):
            html += f"<h3>{line[4:]}</h3>\n"
        elif line.startswith("- "):
            html += f"<li>{line[2:]}</li>\n"
        elif line.startswith("---"):
            html += "<hr>\n"
        elif line.strip() == "":
            html += "<br>\n"
        else:
            html += f"<p>{line}</p>\n"

    html += "</body></html>"

    filename = "analysis_report.html"
    with open(filename, "w") as f:
        f.write(html)
    return filename



# ============================================================
# PART 4: Build the interactive menu — NEW
# ============================================================
# TODO: Create the main program with a menu system.
#
#   def show_menu(docs):
#       print("\n" + "=" * 50)
#       print("  FINANCIAL DOCUMENT ANALYZER")
#       print("=" * 50)
#       print(f"\n  {len(docs)} documents loaded:\n")
#       for i, doc in enumerate(docs, 1):
#           print(f"  {i}. {doc['filename']} ({doc['lines']} lines)")
#       print(f"\n  A. Analyze ALL documents")
#       print(f"  Q. Quit")
#       print()
#       return input("  Choose (1-{}/A/Q): ".format(len(docs))).strip()
#
# New concept — input():
#   We used this in Week 3's research assistant.
#   input("prompt") shows a prompt and waits for the user to type something.
#   .strip() removes extra spaces/newlines.


def show_menu(docs):
    print("\n" + "=" * 50)
    print("  FINANCIAL DOCUMENT ANALYZER")
    print("=" * 50)
    print(f"\n  {len(docs)} documents loaded:\n")
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc['filename']} ({doc['lines']} lines)")
    print(f"\n  A. Analyze ALL documents")
    print(f"  Q. Quit")
    print()
    return input("  Choose (1-{}/A/Q): ".format(len(docs))).strip()


# ============================================================
# PART 5: Main script — tie everything together
# ============================================================
# TODO: Build the main logic that handles both command-line and interactive mode.
#
#   # --- Command-line mode ---
#   if len(sys.argv) > 1:
#       target_file = sys.argv[1]
#       if not os.path.exists(target_file):
#           print(f"Error: file '{target_file}' not found")
#           sys.exit(1)
#       with open(target_file, "r") as f:
#           content = f.read()
#       doc = {"filename": os.path.basename(target_file), "content": content,
#              "lines": len(content.splitlines())}
#
#       valid, reason = validate_document(doc)
#       if not valid:
#           print(f"Error: {reason}")
#           sys.exit(1)
#
#       print(f"\nAnalyzing {doc['filename']}...")
#       result = analyze_document_safe(doc)
#
#       if "error" in result:
#           print(f"Error: {result['error']}")
#       else:
#           print(f"Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")
#           print(f"\nSummary: {result['summary']}")
#
#       report = generate_report([result], [])
#       html_file = save_html_report(report)
#       webbrowser.open(html_file)
#       print(f"\nReport saved to {html_file}")
#       sys.exit(0)
#
#   # --- Interactive mode ---
#   docs = load_documents("data")
#   if not docs:
#       print("No .txt files found in data/ folder")
#       sys.exit(1)
#
#   while True:
#       choice = show_menu(docs)
#
#       if choice.upper() == "Q":
#           print("Goodbye!")
#           break
#
#       elif choice.upper() == "A":
#           # Analyze all documents
#           results = []
#           skipped = []
#           print(f"\nProcessing {len(docs)} documents...\n")
#
#           for i, doc in enumerate(docs, 1):
#               valid, reason = validate_document(doc)
#               if not valid:
#                   print(f"  [{i}/{len(docs)}] SKIP: {doc['filename']} — {reason}")
#                   skipped.append({"filename": doc["filename"], "reason": reason})
#                   continue
#               print(f"  [{i}/{len(docs)}] Processing: {doc['filename']}...")
#               result = analyze_document_safe(doc)
#               if "error" in result:
#                   print(f"           ERROR: {result['error']}")
#               else:
#                   print(f"           Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")
#               results.append(result)
#
#           report = generate_report(results, skipped)
#           html_file = save_html_report(report)
#           webbrowser.open(html_file)
#           print(f"\nReport saved to {html_file}")
#
#       elif choice.isdigit() and 1 <= int(choice) <= len(docs):
#           # Analyze one document
#           doc = docs[int(choice) - 1]
#           valid, reason = validate_document(doc)
#           if not valid:
#               print(f"\nSkipped: {reason}")
#               continue
#
#           print(f"\nAnalyzing {doc['filename']}...")
#           result = analyze_document_safe(doc)
#
#           if "error" in result:
#               print(f"Error: {result['error']}")
#           else:
#               print(f"Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")
#               print(f"\nSummary: {result['summary']}")
#
#           report = generate_report([result], [])
#           html_file = save_html_report(report)
#           webbrowser.open(html_file)
#           print(f"\nReport saved to {html_file}")
#
#       else:
#           print("Invalid choice. Try again.")
#
# New concepts:
#   choice.upper()     — converts "a" to "A", "q" to "Q"
#   choice.isdigit()   — True if "1", "2", "3"; False if "A", "hello"
#   int(choice) - 1    — converts "1" to index 0 (lists start at 0)
#   continue           — skip rest of loop, go back to menu
#   sys.exit(0)        — exit program successfully (0 = no error)


if len(sys.argv) > 1:
    target_file = sys.argv[1]
    if not os.path.exists(target_file):
        print(f"Error: file '{target_file}' not found")
        sys.exit(1)
    with open(target_file, "r") as f:
        content = f.read()
    doc = {"filename": os.path.basename(target_file), "content": content,
            "lines": len(content.splitlines())}

    valid, reason = validate_document(doc)
    if not valid:
        print(f"Error: {reason}")
        sys.exit(1)

    print(f"\nAnalyzing {doc['filename']}...")
    result = analyze_document_safe(doc)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")
        print(f"\nSummary: {result['summary']}")

    report = generate_report([result], [])
    html_file = save_html_report(report)
    webbrowser.open(html_file)
    print(f"\nReport saved to {html_file}")
    sys.exit(0)

# --- Interactive mode ---
docs = load_documents("data")
if not docs:
    print("No .txt files found in data/ folder")
    sys.exit(1)

while True:
    choice = show_menu(docs)

    if choice.upper() == "Q":
        print("Goodbye!")
        break

    elif choice.upper() == "A":
        # Analyze all documents
        results = []
        skipped = []
        print(f"\nProcessing {len(docs)} documents...\n")

        for i, doc in enumerate(docs, 1):
            valid, reason = validate_document(doc)
            if not valid:
                print(f"  [{i}/{len(docs)}] SKIP: {doc['filename']} — {reason}")
                skipped.append({"filename": doc["filename"], "reason": reason})
                continue
            print(f"  [{i}/{len(docs)}] Processing: {doc['filename']}...")
            result = analyze_document_safe(doc)
            if "error" in result:
                print(f"           ERROR: {result['error']}")
            else:
                print(f"           Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")
            results.append(result)

        report = generate_report(results, skipped)
        html_file = save_html_report(report)
        webbrowser.open(html_file)
        print(f"\nReport saved to {html_file}")

    elif choice.isdigit() and 1 <= int(choice) <= len(docs):
        # Analyze one document
        doc = docs[int(choice) - 1]
        valid, reason = validate_document(doc)
        if not valid:
            print(f"\nSkipped: {reason}")
            continue

        print(f"\nAnalyzing {doc['filename']}...")
        result = analyze_document_safe(doc)

        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Done! ({result['total_tokens']} tokens, ${result['cost']:.4f})")
            print(f"\nSummary: {result['summary']}")

        report = generate_report([result], [])
        html_file = save_html_report(report)
        webbrowser.open(html_file)
        print(f"\nReport saved to {html_file}")

    else:
        print("Invalid choice. Try again.")