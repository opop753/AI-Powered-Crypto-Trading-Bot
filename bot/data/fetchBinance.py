import os
import logging
import httpx
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)

async def fetch_binance_data(symbol='BTC-USD', interval='1h'):
    # Commenting out the Binance fetch part
    # url = "https://api.binance.com/api/v3/klines"  # Correct API endpoint for historical data
    # params = {
    #     'symbol': symbol,
    #     'interval': interval,
    #     'limit': 1000  # Adjust limit as needed
    # }
    
    return await fetch_binance_candlestick_data(symbol, interval)  # Fetch and return candlestick data

async def fetch_binance_candlestick_data(symbol='BTC-USD', interval='1h', start_time=None, end_time=None):
    url = "https://api.binance.com/api/v3/klines"  # Correct API endpoint for candlestick data
    params = {
        'symbol': symbol,
        'interval': interval
    }
    if start_time:
        params['startTime'] = start_time
    if end_time:
        params['endTime'] = end_time

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)  # Fetch candlestick data from Binance
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()  # Parse the JSON response
            df = pd.DataFrame(data)  # Convert to DataFrame
            return df
    except Exception as e:
        logging.error(f"Error fetching candlestick data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
