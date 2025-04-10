from backend.data.fetchBitvavo import fetch_bitvavo_candlestick_data

async def fetch_bitvavo_data(symbol: str, start_time: float, end_time: float):
    """
    Fetch historical data for backtesting from the Bitvavo API.

    Args:
        symbol (str): The market symbol (e.g., 'BTC-EUR').
        start_time (float): The start time for the data fetch.
        end_time (float): The end time for the data fetch.

    Returns:
        list: A list of historical data for backtesting.
    """
    # Fetch candlestick data
    data = await fetch_bitvavo_candlestick_data(symbol, '1h', start_time, end_time)
    # Implement backtesting logic here (if needed)
    return data
