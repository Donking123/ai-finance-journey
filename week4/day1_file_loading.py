"""
Week 4 - Day 1: Read and Parse Real Financial Data from Files
==============================================================
Goal: Load .txt files from a folder into Python.
      Build a reusable load_documents() function.
"""

import os


# ============================================================
# PART 1: Read a single file
# ============================================================
# TODO: Open and read "data/dbs_q1_2025.txt"
#   - Use: with open("data/dbs_q1_2025.txt", "r") as f:
#              content = f.read()
#   - Print the filename, character count, and line count:
#       print(f"File: dbs_q1_2025.txt")
#       print(f"Characters: {len(content)}")
#       print(f"Lines: {len(content.splitlines())}")
#       print()
#
# Explanation:
#   with open(path, "r") as f:   — opens the file for reading ("r")
#   f.read()                      — reads the entire file as one string
#   content.splitlines()          — splits the string into a list of lines
#   len()                         — counts items (characters in a string, items in a list)

with open("data/dbs_q1_2025.txt", "r") as f:
    content = f.read()

print(f"File: dbs_q1_2025.txt")
print(f"Characters: {len(content)}")
print(f"Lines: {len(content.splitlines())}")
# ============================================================
# PART 2: Read all 3 files
# ============================================================
# TODO: Do the same for all 3 files. You can copy-paste the pattern
#   from Part 1 for each file, or use a list:
#
#   filenames = ["dbs_q1_2025.txt", "news_headlines.txt", "analyst_note.txt"]
#   for filename in filenames:
#       with open(f"data/{filename}", "r") as f:
#           content = f.read()
#       print(f"File: {filename}")
#       print(f"Characters: {len(content)}")
#       print(f"Lines: {len(content.splitlines())}")
#       print()

filenames = ["dbs_q1_2025.txt", "news_headlines.txt", "analyst_note.txt"]
for filename in filenames:
    with open(f"data/{filename}", "r") as f:
        content = f.read()
    print(f"File: {filename}")
    print(f"Characters: {len(content)}")
    print(f"Lines: {len(content.splitlines())}")
    print()

# ============================================================
# PART 3: Build load_documents() function
# ============================================================
# TODO: Create a function called load_documents(folder_path)
#   - Uses os.listdir(folder_path) to get all files in the folder
#   - Filters for only .txt files using: f.endswith(".txt")
#   - Reads each file
#   - Returns a list of dictionaries, one per file:
#       [
#           {"filename": "dbs_q1_2025.txt", "content": "...", "lines": 12},
#           {"filename": "news_headlines.txt", "content": "...", "lines": 10},
#           ...
#       ]
#
# def load_documents(folder_path):
#     documents = []
#     files = os.listdir(folder_path)
#     txt_files = [f for f in files if f.endswith(".txt")]
#
#     for filename in txt_files:
#         full_path = os.path.join(folder_path, filename)
#         with open(full_path, "r") as f:
#             content = f.read()
#         documents.append({
#             "filename": filename,
#             "content": content,
#             "lines": len(content.splitlines())
#         })
#
#     return documents
#
# New concepts:
#   os.listdir("data")           — returns ["dbs_q1_2025.txt", "news_headlines.txt", ...]
#   f.endswith(".txt")           — True if filename ends with ".txt"
#   os.path.join("data", "x.txt") — builds "data/x.txt" (works on any OS)
#   [f for f in files if ...]    — list comprehension (filter a list in one line)

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
# PART 4: Test load_documents()
# ============================================================
# TODO: Call load_documents("data") and print results
#
#   docs = load_documents("data")
#   print(f"Loaded {len(docs)} documents:\n")
#   for doc in docs:
#       print(f"  {doc['filename']} — {doc['lines']} lines, {len(doc['content'])} chars")

docs = load_documents("data")
print(f"Loaded  {len(docs)} documents:\n")
for doc in docs:
    print(f"  {doc['filename']} — {doc['lines']} lines, {len(doc['content'])} chars")
