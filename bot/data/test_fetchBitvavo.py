# Test script for fetch_bitvavo_data function
from fetchBitvavo import fetch_bitvavo_data

# Test the function with a valid market symbol
result = fetch_bitvavo_data(symbol='BTC-EUR')
print(result)

# Additional test cases for different market symbols
symbols = ['ETH-EUR', 'LTC-EUR', 'XRP-EUR']
for symbol in symbols:
    try:
        result = fetch_bitvavo_data(symbol=symbol)
        print(f"Result for {symbol}: {result}")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
