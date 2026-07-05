import requests
import json

# Call the API
url = "https://api.exchangerate-api.com/v4/latest/SGD"
response = requests.get(url)
data = response.json()

# Print base info
print(f"Base currency: {data['base']}")
print(f"Last updated: {data['date']}")

# Print selected exchange rates
currencies = ["USD", "MYR", "JPY", "GBP", "EUR"]

print("\nSGD Exchange Rates:")
for currency in currencies:
    rate = data["rates"][currency]
    print(f"  1 SGD = {rate} {currency}")


# Save result to JSON
result = {
    "base": data["base"],
    "date": data["date"],
    "selected_rates": {c: data["rates"][c] for c in currencies}
}

with open("exchange_rates.json", "w") as f:
    json.dump(result, f, indent=2)

print("\nSaved to exchange_rates.json")