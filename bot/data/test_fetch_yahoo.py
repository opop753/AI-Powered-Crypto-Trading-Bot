# Test script for fetch_yfinance_data
import pandas as pd
from fetchYahooFinance import fetch_yfinance_data

import time

def test_fetch():
    time.sleep(5)  # Delay before the first fetch attempt
    data = fetch_yfinance_data('BTC-USD', '1h', '2y')
    if data is not None:
        print("Data fetched successfully:")
        print(data.head())
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    test_fetch()
