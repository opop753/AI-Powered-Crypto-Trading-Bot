from fastapi import APIRouter, HTTPException
import httpx  # Import httpx for making HTTP requests

router = APIRouter()

@router.get("/api/price-data/bitvavo")
async def get_bitvavo_price_data(symbol: str = 'BTC-EUR'):
    """Fetch and return price data for the specified symbol from Bitvavo."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.bitvavo.com/v2/ticker/24h?market={symbol}")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()  # Parse the JSON response
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    """Fetch and return price data for the specified symbol from Bitvavo."""
    
@router.get("/api/price-data/new-api")
async def get_new_api_price_data(symbol: str = 'BTC-EUR'):
    """Fetch and return price data for the specified symbol from the new API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.newapi.com/v1/historical-data?symbol={symbol}")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()  # Parse the JSON response
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    """Fetch and return price data for the specified symbol from Bitvavo."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.bitvavo.com/v2/ticker/24h?market={symbol}")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()  # Parse the JSON response
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/portfolio")
async def get_portfolio():
    """
    Fetch and return the portfolio data from Bitvavo, Binance, and CoinGecko.
    """
    try:
        # Fetch data from Bitvavo
        bitvavo_data = await get_bitvavo_price_data()
        
        # Fetch data from Binance
        binance_response = httpx.get("https://api.binance.com/api/v3/ticker/24hr")
        binance_response.raise_for_status()
        binance_data = binance_response.json()
        
        # Fetch data from CoinGecko
        coingecko_response = httpx.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd")
        coingecko_response.raise_for_status()
        coingecko_data = coingecko_response.json()
        
        # Combine all data
        portfolio_data = {
            "bitvavo": bitvavo_data,
            "binance": binance_data,
            "coingecko": coingecko_data
        }
        
        return portfolio_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Other endpoints remain unchanged
