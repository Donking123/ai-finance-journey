stocks = [
    {"name": "DBS", "price": 35.50, "shares": 100, "sector": "finance"},
    {"name": "Singtel", "price": 2.80, "shares": 500, "sector": "telecom"},
    {"name": "CapitaLand", "price": 3.45, "shares": 200, "sector": "realestate"},
    {"name": "OCBC", "price": 13.20, "shares": 150, "sector": "finance"},
    {"name": "Keppel", "price": 7.10, "shares": 300, "sector": "industrial"},
]

# Print each stock's total value
for stock in stocks:
    value = stock["price"] * stock["shares"]
    print(f"{stock['name']}: ${value:.2f}")

# Find the most valuable position
top_stock = max(stocks, key=lambda s: s["price"] * s["shares"])
top_value = top_stock["price"] * top_stock["shares"]
print(f"\nMost valuable: {top_stock['name']} at ${top_value:.2f}")

# Group by sector and print totals
sector_totals = {}
for stock in stocks:
    value = stock["price"] * stock["shares"]
    if stock["sector"] in sector_totals:
        sector_totals[stock["sector"]] += value
    else:
        sector_totals[stock["sector"]] = value

print("\nSector totals:")
for sector, total in sector_totals.items():
    print(f"  {sector}: ${total:.2f}")
