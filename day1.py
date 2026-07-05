# Stock information
name = "DBS"
price = 35.50
shares = 100
sector = "finance"

# Calculate total value
total_value = price * shares

print(f"You own {shares} of {name} worth ${total_value:.2f}")

if total_value > 10000:
    print("Large position")
else:
    print("Small position")