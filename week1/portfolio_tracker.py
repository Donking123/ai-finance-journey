import json

with open("portfolio.json", "r") as f:
    stocks = json.load(f)

# Step 2: Simulated current market prices
current_prices = {
    "DBS": 36.80,
    "Singtel": 2.65,
    "CapitaLand": 3.70,
    "OCBC": 13.50,
    "Keppel": 6.90,
}

# Step 3: Calculate everything for each stock
portfolio = []
for stock in stocks:
    name = stock["name"]
    purchase_price = stock["price"]
    current_price = current_prices[name]
    shares = stock["shares"]

    purchase_value = purchase_price * shares
    current_value = current_price * shares
    gain_loss = current_value - purchase_value
    gain_pct = (gain_loss / purchase_value) * 100

    portfolio.append({
        "name": name,
        "shares": shares,
        "purchase_price": purchase_price,
        "current_price": current_price,
        "current_value" : current_value,
        "gain_loss" : gain_loss,
        "gain_pct": gain_pct,
    })


total_value = sum(s["current_value"] for s in portfolio)

for stock in portfolio:
    stock["weight"] = (stock["current_value"] / total_value) * 100

best = max(portfolio, key=lambda s: s["gain_pct"])
worst = min(portfolio, key= lambda s: s["gain_pct"])


# Step 5: Build the report
report = "=" * 50 + "\n"
report += "       PORTFOLIO TRACKER REPORT\n"
report += "=" * 50 + "\n\n"

for stock in portfolio:
    sign = "+" if stock["gain_loss"] >= 0 else ""
    report += f"{stock['name']}\n"
    report += f"  Shares: {stock['shares']}\n"
    report += f"  Purchase: ${stock['purchase_price']:.2f} → Current: ${stock['current_price']:.2f}\n"
    report += f"  Value: ${stock['current_value']:.2f} ({stock['weight']:.1f}% of portfolio)\n"
    report += f"  Gain/Loss: {sign}${stock['gain_loss']:.2f} ({sign}{stock['gain_pct']:.1f}%)\n\n"

report += "-" * 50 + "\n"
report += f"Total Portfolio Value: ${total_value:.2f}\n"
report += f"Best Performer:  {best['name']} (+{best['gain_pct']:.1f}%)\n"
report += f"Worst Performer: {worst['name']} ({worst['gain_pct']:.1f}%)\n"

print(report)

# Step 6: Save to file
with open("tracker_report.txt", "w") as f:
    f.write(report)

print("Report saved to tracker_report.txt")