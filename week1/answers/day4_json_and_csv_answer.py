import json
import csv

stocks = [
    {"name": "DBS", "price": 35.50, "shares": 100, "sector": "finance"},
    {"name": "Singtel", "price": 2.80, "shares": 500, "sector": "telecom"},
    {"name": "CapitaLand", "price": 3.45, "shares": 200, "sector": "realestate"},
    {"name": "OCBC", "price": 13.20, "shares": 150, "sector": "finance"},
    {"name": "Keppel", "price": 7.10, "shares": 300, "sector": "industrial"},
]

# Save to JSON
with open("portfolio.json", "w") as f:
    json.dump(stocks, f, indent=2)

# Read back from JSON
with open("portfolio.json", "r") as f:
    loaded_json = json.load(f)

print("From JSON:")
for stock in loaded_json:
    print(f"  {stock['name']}: ${stock['price'] * stock['shares']:.2f}")

# Save to CSV
with open("portfolio.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "price", "shares", "sector"])
    writer.writeheader()
    writer.writerows(stocks)

# Read back from CSV
with open("portfolio.csv", "r") as f:
    reader = csv.DictReader(f)
    loaded_csv = list(reader)

print("\nFrom CSV:")
for stock in loaded_csv:
    print(f"  {stock['name']}: ${float(stock['price']) * int(stock['shares']):.2f}")

# Confirm they match
print(f"\nJSON count: {len(loaded_json)}, CSV count: {len(loaded_csv)}")
print("Data matches!" if len(loaded_json) == len(loaded_csv) else "Mismatch!")
