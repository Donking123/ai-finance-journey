# Stock information
name = "DBS"
price = 35.50
shares = 100
sector = "finance"

# Calculate total value
total_value = price * shares

# Print summary
print(f"You own {shares} shares of {name} worth ${total_value:.2f}")

# Check position size
if total_value > 10000:
    print("Large position")
else:
    print("Small position")
