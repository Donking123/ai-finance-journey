"""
Week 5 - Day 1: pandas Basics — DataFrames, read_csv, Filtering
=================================================================
Goal: Load SGX stock data into a DataFrame, explore it, and filter it.

pandas is THE data tool in Python. Think of a DataFrame as a
spreadsheet/Excel table — rows and columns — but in code.
"""

import pandas as pd


# ============================================================
# PART 1: Load CSV into a DataFrame
# ============================================================
# TODO: Load the SGX stocks CSV file into a DataFrame.
#
#   df = pd.read_csv("data/sgx_stocks.csv")
#   print(df)
#
# New concept — pandas:
#   import pandas as pd     — import pandas, call it "pd" for short
#   pd.read_csv("file.csv") — reads a CSV file into a DataFrame
#   A DataFrame is a table: rows (stocks) and columns (ticker, name, etc.)
#
# When you print(df), you'll see the full table.

df = pd.read_csv("data/sgx_stocks.csv")
print(df)


# ============================================================
# PART 2: Explore the DataFrame
# ============================================================
# TODO: Use these commands to understand your data.
#
#   print(f"Shape: {df.shape}")          # (rows, columns) — e.g. (20, 7)
#   print(f"\nColumns: {list(df.columns)}")  # column names
#   print(f"\nData types:\n{df.dtypes}")     # what type each column is
#   print(f"\nFirst 5 rows:\n{df.head()}")   # first 5 rows
#   print(f"\nLast 3 rows:\n{df.tail(3)}")   # last 3 rows
#
# New concepts:
#   df.shape      — tuple of (rows, columns): (20, 7) means 20 stocks, 7 fields
#   df.columns    — list of column names
#   df.dtypes     — data type of each column (int64, float64, object=string)
#   df.head(n)    — first n rows (default 5)
#   df.tail(n)    — last n rows

print(f"Shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")


# ============================================================
# PART 3: Select columns
# ============================================================
# TODO: Select and print specific columns.
#
#   # Single column — returns a Series (one column of data)
#   names = df["name"]
#   print("Stock names:")
#   print(names)
#   print()
#
#   # Multiple columns — returns a smaller DataFrame
#   summary = df[["name", "sector", "price"]]
#   print("Name, sector, and price:")
#   print(summary)
#
# New concepts:
#   df["name"]              — one column → Series (like a list)
#   df[["name", "price"]]   — multiple columns → DataFrame (mini table)
#   Note: single [] for one column, double [[]] for multiple



# ============================================================
# PART 4: Filter rows
# ============================================================
# TODO: Filter the DataFrame to show only specific stocks.
#
#   # Filter: only banking stocks
#   banks = df[df["sector"] == "Banking"]
#   print("Banks:")
#   print(banks[["name", "price", "dividend_yield"]])
#   print()
#
#   # Filter: stocks with dividend yield above 5%
#   high_yield = df[df["dividend_yield"] > 5.0]
#   print("High yield (>5%):")
#   print(high_yield[["name", "sector", "dividend_yield"]])
#   print()
#
#   # Filter: REITs only (sector contains "REIT")
#   reits = df[df["sector"].str.contains("REIT")]
#   print("REITs:")
#   print(reits[["name", "sector", "dividend_yield"]])
#
# New concepts:
#   df[df["sector"] == "Banking"]        — filter where sector equals "Banking"
#   df[df["dividend_yield"] > 5.0]       — filter where yield is above 5
#   df["sector"].str.contains("REIT")    — filter where sector contains "REIT"
#
# How filtering works:
#   df["sector"] == "Banking" produces True/False for every row.
#   df[True/False list] keeps only the True rows.



# ============================================================
# PART 5: Sort values
# ============================================================
# TODO: Sort the DataFrame by different columns.
#
#   # Sort by market cap (largest first)
#   by_cap = df.sort_values("market_cap_m", ascending=False)
#   print("Top 5 by market cap:")
#   print(by_cap[["name", "sector", "market_cap_m"]].head())
#   print()
#
#   # Sort by dividend yield (highest first)
#   by_yield = df.sort_values("dividend_yield", ascending=False)
#   print("Top 5 by dividend yield:")
#   print(by_yield[["name", "sector", "dividend_yield"]].head())
#   print()
#
#   # Sort by PE ratio (lowest first = cheapest)
#   has_pe = df[df["pe_ratio"] > 0]
#   by_pe = has_pe.sort_values("pe_ratio")
#   print("Top 5 cheapest by PE ratio:")
#   print(by_pe[["name", "sector", "pe_ratio"]].head())
#
# New concepts:
#   df.sort_values("column")                    — sort ascending (smallest first)
#   df.sort_values("column", ascending=False)   — sort descending (largest first)
#   Chaining: df.sort_values(...).head()        — sort, then take top 5



# ============================================================
# PART 6: Combine filter + sort + select
# ============================================================
# TODO: Chain operations together to answer questions.
#
#   # Question 1: What are the top 3 highest-yielding REITs?
#   reits = df[df["sector"].str.contains("REIT")]
#   top_reits = reits.sort_values("dividend_yield", ascending=False).head(3)
#   print("Top 3 REITs by yield:")
#   print(top_reits[["name", "sector", "dividend_yield", "price"]])
#   print()
#
#   # Question 2: Which banking stock has the lowest PE ratio?
#   banks = df[df["sector"] == "Banking"]
#   cheapest_bank = banks.sort_values("pe_ratio").head(1)
#   print("Cheapest bank by PE:")
#   print(cheapest_bank[["name", "pe_ratio", "price"]])
#   print()
#
#   # Question 3: How many stocks have zero dividend?
#   no_div = df[df["dividend_yield"] == 0]
#   print(f"Stocks with no dividend: {len(no_div)}")
#   print(no_div[["name", "sector"]])
