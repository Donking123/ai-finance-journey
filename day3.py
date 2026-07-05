stocks = [
    {"name": "DBS", "price": 35.50, "shares": 100, "sector": "finance"},
    {"name": "Singtel", "price": 2.80, "shares": 500, "sector": "telecom"},
    {"name": "CapitaLand", "price": 3.45, "shares": 200, "sector": "realestate"},
    {"name": "OCBC", "price": 13.20, "shares": 150, "sector": "finance"},
    {"name": "Keppel", "price": 7.10, "shares": 300, "sector": "industrial"},
]

def calculate_portfolio_value(stocks):
    total = 0
    for stock in stocks:
        total += stock["price"] * stock["shares"]
    return total

def find_top_stock(stocks):
    return max(stocks, key=lambda s: s["price"] * s["shares"])

def group_by_sector(stocks):
    sector_totals = {}
    for stock in stocks:
        value = stock["price"] * stock["shares"]
        if stock["sector"] in sector_totals:
            sector_totals[stock["sector"]] += value
        else:
            sector_totals[stock["sector"]] = value
    return sector_totals

total = calculate_portfolio_value(stocks)
top = find_top_stock(stocks)
sectors = group_by_sector(stocks)

report = f"Portfolio Value: ${total:.2f}\n"
report += f"Top Stock: {top['name']} (${top['price'] * top['shares']:.2f})\n"
report += "\nSector Totals:\n"
for sector, value in sectors.items():
    report += f" {sector}: ${value:.2f}\n"

with open("portfolio_report.txt", "w") as f:
    f.write(report)

with open("portfolio_report.txt", "r") as f:
    print(f.read())