# Fetch historical data from yahoo finance, returning a dataframe
import yfinance as yf

import time
import random

def fetch_yfinance_data(symbol='BTC-USD', interval='1h', period="2y"):
    retries = 5
    for attempt in range(retries):
        try:
            data = yf.download(tickers=symbol, interval=interval, period=period)
            break  # Exit the loop if the request is successful
        except Exception as e:
            if attempt < retries - 1:
                wait_time = 2 ** attempt + random.uniform(0, 1)  # Exponential backoff
                print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                print("Failed to fetch data after multiple attempts.")
                return None  # Return None or handle the error as needed
    print(data)  # Print the DataFrame to inspect its structure
    import pandas as pd
    data.columns = data.columns.get_level_values(0)
    data = data.reset_index()  # Ensure 'Date' is a normal column
    data = data.rename(columns={'Date': 'timestamp'})
    data.columns = [col.lower() for col in data.columns]
    numeric_cols = ['close', 'high', 'low', 'open', 'volume']
    data['close'] = pd.to_numeric(data['close'], errors='coerce')
    data['close'] = data['close'].astype(float)
    data['timestamp'] = data.index  # Use the index as the timestamp
    return data
