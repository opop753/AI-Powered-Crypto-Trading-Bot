# fetch historical data from bitvavo and return a dataframe
import os

import pandas as pd

from bot import backtest

BITVAVO_API_KEY = os.getenv('BITVAVO_API_KEY')
BITVAVO_API_SECRET = os.getenv('BITVAVO_API_SECRET')

from apscheduler.schedulers.background import BackgroundScheduler  # Import BackgroundScheduler

# Create a scheduler instance
scheduler = BackgroundScheduler()

# Function to refresh data
def refresh_data():
    fetch_bitvavo_data(symbol='BTC-EUR')  # Call the function to fetch data

# Start the scheduler to run the refresh_data function every 10 minutes
scheduler.add_job(refresh_data, 'interval', minutes=10)
scheduler.start()

from python_bitvavo_api.bitvavo import Bitvavo  # Import the Bitvavo class

def fetch_bitvavo_data(symbol='BTC-EUR', interval='1h', start_time=None, end_time=None, retries=3, strategy='MovingAverageCrossover'):
    bitvavo = Bitvavo({'APIKEY': BITVAVO_API_KEY,'APISECRET': BITVAVO_API_SECRET})
    params = {'market': symbol, 'interval': interval}
    if start_time:
        params['start'] = int(pd.to_datetime(start_time).timestamp() * 1000)
    if end_time:
        params['end'] = int(pd.to_datetime(end_time).timestamp() * 1000)
    for attempt in range(retries):
        try:
            response = bitvavo.candles(symbol, interval, params)
            break  # Exit the loop if the request is successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                raise  # Re-raise the exception if all attempts fail
    data = pd.DataFrame(response, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'strategy'])
    data['close'] = pd.to_numeric(data['close'], errors='coerce')
    data['close'] = data['close'].astype(float)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    bitvavo_data = data
    # Run Backtest with error handling
    bt = backtest(data, strategy, cash=10_000, commission=0.002)

    try:
        bt = backtest(bitvavo_data, strategy, cash=10_000, commission=0.002)
        stats = bt.run()
    except Exception as e:
        print(f"Error during backtesting: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    stats = bt.run()
# Display Results
    print(stats)
    bt.plot()
    return data
