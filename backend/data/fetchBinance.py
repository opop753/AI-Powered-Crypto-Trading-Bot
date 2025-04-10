import httpx
import time

async def fetch_binance_data():
    """
    Fetch Binance data.

    Returns:
        dict: A dictionary containing Binance data.
    """
    # Example parameters for fetching data
    symbol = 'BTC-USD'
    interval = '1h'
    limit = 100
    end = int(time.time() * 1000)  # Current time in milliseconds
    start = end - (24 * 60 * 60 * 1000)  # 24 hours ago in milliseconds

    return await fetch_binance_candlestick_data(symbol, interval, limit, start, end)

async def fetch_binance_candlestick_data(symbol: str, interval: str, limit: int, start: int, end: int):
    """
    Fetch candlestick data from Binance API.

    Args:
        symbol (str): The trading pair symbol (e.g., 'BTC-USD').
        interval (str): The interval for the candlestick data (e.g., '1h').
        limit (int): The number of data points to fetch.
        start (int): The start time in milliseconds.
        end (int): The end time in milliseconds.

    Returns:
        list: A list of candlestick data.
    """
    url = f'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit,
        'startTime': start,
        'endTime': end
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
