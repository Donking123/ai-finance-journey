"""
Week 4 - Day 5: Report Generation — Turn Results into Readable Reports
========================================================================
Goal: Load batch_results_safe.json and generate a formatted Markdown
      report, then open it in the browser as HTML.
"""

import json
from datetime import datetime


# ============================================================
# PART 1: Load the batch results
# ============================================================
# TODO: Load batch_results_safe.json and print a quick overview.
#
#   with open("batch_results_safe.json", "r") as f:
#       data = json.load(f)
#
#   results = data["results"]
#   skipped = data["skipped"]
#
#   print(f"Loaded {len(results)} results, {len(skipped)} skipped")
#   for r in results:
#       print(f"  {r['filename']} — {r['total_tokens']} tokens")
#
# New concept — json.load() vs json.dump():
#   json.dump(data, file)   — writes Python → JSON file (we used this before)
#   json.load(file)         — reads JSON file → Python (the reverse!)

with open("batch_results_safe.json", "r") as f:
    data = json.load(f)

results = data["results"]
skipped = data["skipped"]

print(f"Loaded {len(results)} results, {len(skipped)} skipped")
for r in results:
     print(f"  {r['filename']} — {r['total_tokens']} tokens")

# ============================================================
# PART 2: Build the report header
# ============================================================
# TODO: Start building a markdown string with a header section.
#
#   now = datetime.now().strftime("%Y-%m-%d %H:%M")
#   total_tokens = sum(r["total_tokens"] for r in results)
#   total_cost = sum(r["cost"] for r in results)
#
#   report = f"""# Financial Document Analysis Report
#   Generated: {now}
#
#   ## Overview
#   - **Documents analyzed:** {len(results)}
#   - **Documents skipped:** {len(skipped)}
#   - **Total tokens used:** {total_tokens:,}
#   - **Total cost:** ${total_cost:.4f}
#
#   ---
#
#   """
#
#   print("Header built!")
#
# New concepts:
#   datetime.now()                    — gets current date/time
#   .strftime("%Y-%m-%d %H:%M")      — formats as "2026-07-07 14:30"
#   sum(r["cost"] for r in results)   — adds up one field across all results
#
# Note: The triple-quote string preserves line breaks.
#       Everything between """ and """ becomes part of the string.

now = datetime.now().strftime("%Y-%m-%d %H:%M")
total_tokens = sum(r["total_tokens"] for r in results)
total_cost = sum(r["cost"] for r in results)

report = f"""# Financial Document Analysis Report
Generated: {now}

## Overview
- **Documents analyzed:** {len(results)}
- **Documents skipped:** {len(skipped)}
- **Total tokens used:** {total_tokens:,}
- **Total cost:** ${total_cost:.4f}

---

"""

print("Header built!")




# ============================================================
# PART 3: Add each document's analysis to the report
# ============================================================
# TODO: Loop through results and append each document's section.
#
#   for r in results:
#       report += f"""## {r['filename']}
#   **Tokens:** {r['total_tokens']:,} | **Cost:** ${r['cost']:.4f}
#
#   ### Extracted Metrics
#   {r['extract']}
#
#   ### Analysis
#   {r['analysis']}
#
#   ### Executive Summary
#   {r['summary']}
#
#   ---
#
#   """
#
#   print(f"Added {len(results)} document sections")
#
# How += works with strings:
#   report += "new text"  is the same as  report = report + "new text"
#   It appends to the end of the existing string.

for r in results:
     report += f"""## {r['filename']}
**Tokens:** {r['total_tokens']:,} | **Cost:** ${r['cost']:.4f}

### Extracted Metrics
{r['extract']}

### Analysis
{r['analysis']}

### Executive Summary
{r['summary']}

---

"""

print(f"Added {len(results)} document sections")



# ============================================================
# PART 4: Add skipped documents (if any)
# ============================================================
# TODO: If any documents were skipped, add a section listing them.
#
#   if skipped:
#       report += "## Skipped Documents\n\n"
#       for s in skipped:
#           report += f"- **{s['filename']}**: {s['reason']}\n"
#       report += "\n"
#
#   print(f"Skipped section: {'added' if skipped else 'none needed'}")
#
# New concept — if skipped:
#   An empty list [] is "falsy" in Python.
#   A non-empty list ["something"] is "truthy".
#   So "if skipped:" means "if there are any skipped documents"

if skipped:
     report += "## Skipped Documents\n\n"
     for s in skipped:
         report += f"- **{s['filename']}**: {s['reason']}\n"
     report += "\n"

print(f"Skipped section: {'added' if skipped else 'none needed'}")



# ============================================================
# PART 5: Save as Markdown and open as HTML in browser
# ============================================================
# TODO: Save the markdown report, then create an HTML version
#   and open it in the browser.
#
#   # Save markdown
#   with open("analysis_report.md", "w") as f:
#       f.write(report)
#   print(f"Markdown saved to analysis_report.md")
#
#   # Convert to simple HTML and open in browser
#   import webbrowser
#
#   html = f"""<html>
#   <head>
#       <title>Financial Analysis Report</title>
#       <style>
#           body {{ font-family: -apple-system, Arial, sans-serif;
#                   max-width: 800px; margin: 40px auto; padding: 0 20px;
#                   line-height: 1.6; color: #333; }}
#           h1 {{ color: #1a6b4a; border-bottom: 2px solid #1a6b4a; padding-bottom: 10px; }}
#           h2 {{ color: #2c5282; margin-top: 30px; }}
#           h3 {{ color: #555; }}
#           hr {{ border: none; border-top: 1px solid #ddd; margin: 30px 0; }}
#           pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px;
#                  overflow-x: auto; font-size: 14px; }}
#           code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
#           strong {{ color: #1a1a1a; }}
#       </style>
#   </head>
#   <body>
#   """
#
#   # Convert markdown to basic HTML
#   for line in report.split("\n"):
#       if line.startswith("# "):
#           html += f"<h1>{line[2:]}</h1>\n"
#       elif line.startswith("## "):
#           html += f"<h2>{line[3:]}</h2>\n"
#       elif line.startswith("### "):
#           html += f"<h3>{line[4:]}</h3>\n"
#       elif line.startswith("- "):
#           html += f"<li>{line[2:]}</li>\n"
#       elif line.startswith("---"):
#           html += "<hr>\n"
#       elif line.strip() == "":
#           html += "<br>\n"
#       else:
#           html += f"<p>{line}</p>\n"
#
#   html += "</body></html>"
#
#   with open("analysis_report.html", "w") as f:
#       f.write(html)
#
#   webbrowser.open("analysis_report.html")
#   print("HTML report opened in browser!")
#
# New concepts:
#   webbrowser.open("file.html")   — opens a file in your default browser
#   line.startswith("# ")          — checks if a string starts with "# "
#   line[2:]                       — slice: everything from index 2 onward
#                                    "# Hello" → "Hello"
#   {{ and }} in f-strings         — literal curly braces (CSS needs them)

  # Save markdown
with open("analysis_report.md", "w") as f:
     f.write(report)
print(f"Markdown saved to analysis_report.md")

# Convert to simple HTML and open in browser
import webbrowser

html = f"""<html>
<head>
<title>Financial Analysis Report</title>
<style>
      body {{ font-family: -apple-system, Arial, sans-serif;
            max-width: 800px; margin: 40px auto; padding: 0 20px;
            line-height: 1.6; color: #333; }}
      h1 {{ color: #1a6b4a; border-bottom: 2px solid #1a6b4a; padding-bottom: 10px; }}
      h2 {{ color: #2c5282; margin-top: 30px; }}
      h3 {{ color: #555; }}
      hr {{ border: none; border-top: 1px solid #ddd; margin: 30px 0; }}
      pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px;
            overflow-x: auto; font-size: 14px; }}
      code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
      strong {{ color: #1a1a1a; }}
</style>
</head>
<body>
"""

# Convert markdown to basic HTML
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

with open("analysis_report.html", "w") as f:
    f.write(html)

webbrowser.open("analysis_report.html")
print("HTML report opened in browser!")
