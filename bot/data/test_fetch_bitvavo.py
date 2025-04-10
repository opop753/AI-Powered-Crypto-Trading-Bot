import os
import requests
import pandas as pd

BITVAVO_API_KEY = os.getenv('BITVAVO_API_KEY')
BITVAVO_API_SECRET = os.getenv('BITVAVO_API_SECRET')

def fetch_bitvavo_data(symbol='BTC-EUR'):
    url = "https://api.bitvavo.com/v2/markets/" + symbol + "/candles"
    params = {
        'interval': '1h',
        'limit': 100
    }
    headers = {
        'Content-Type': 'application/json',
        'X-BITVAVO-APIKEY': BITVAVO_API_KEY,
        'X-BITVAVO-APISECRET': BITVAVO_API_SECRET
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print(f"Fetched data: {response.json()}")
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")

fetch_bitvavo_data()
