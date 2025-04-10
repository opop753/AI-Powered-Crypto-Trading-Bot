# fetch historical data from bitvavo and return a dataframe
from dotenv import load_dotenv
import os
import httpx
import pandas as pd

load_dotenv()  # Load environment variables from .env file

BITVAVO_API_KEY = os.getenv('BITVAVO_API_KEY')
BITVAVO_API_SECRET = os.getenv('BITVAVO_API_SECRET')

if BITVAVO_API_KEY is None or BITVAVO_API_SECRET is None:
    raise ValueError("API key and secret must be set in environment variables.")

async def fetch_bitvavo_data(symbol='BTC-EUR', interval='1h', start_time=None, end_time=None, retries=3):
    url = "https://api.newapi.com/v1/historical-data"  # Replace with the new API endpoint

    params = {
        'market': symbol,
        'interval': interval
    }
    if start_time:
        params['start'] = int(pd.to_datetime(start_time).timestamp() * 1000)
    if end_time:
        params['end'] = int(pd.to_datetime(end_time).timestamp() * 1000)

    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                response = await client.get(url, params=params)  # Fetch historical data from the new API
                response.raise_for_status()  # Raise an error for bad responses
                data = response.json()  # Parse the JSON response
                df = pd.DataFrame(data)  # Convert to DataFrame
                return df
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    raise  # Re-raise the exception if all attempts fail

async def fetch_bitvavo_candlestick_data(market: str, interval: str, limit: int, start: int = None, end: int = None):
    url = "https://api.bitvavo.com/v2/ticker/24h"  # Endpoint for fetching ticker data
    headers = {
        'Content-Type': 'application/json',
        'X-BITVAVO-APIKEY': BITVAVO_API_KEY,
        'X-BITVAVO-APISECRET': BITVAVO_API_SECRET
    }
    
    params = { 
        'market': market  # Only market parameter is needed for ticker data
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)  # Fetch candlestick data
        if response.status_code == 200:
            return response.json()  # Return the fetched data
        else:
            print(f"Error fetching candlestick data: {response.status_code} - {response.text}")
            return []  # Return an empty list on error
