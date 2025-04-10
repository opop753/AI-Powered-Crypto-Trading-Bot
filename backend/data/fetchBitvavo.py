import httpx
import pandas as pd

async def fetch_bitvavo_candlestick_data(symbol: str, interval: str, start_time: float, end_time: float, limit: int = 100):
    """
    Fetch historical candlestick data from the Bitvavo API.

    Args:
        symbol (str): The market symbol (e.g., 'BTC-EUR').
        interval (str): The time interval for the candlestick data (e.g., '1h').
        start_time (float): The start time for the data fetch.
        end_time (float): The end time for the data fetch.

    Returns:
        pd.DataFrame: A DataFrame containing the fetched candlestick data.
    """
    url = f"https://api.bitvavo.com/v2/candlestick/{symbol}/{interval}?start={start_time}&end={end_time}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    return df
