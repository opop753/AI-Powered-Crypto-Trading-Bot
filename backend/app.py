from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import traceback
from backend.models.model import Model
#from database import SessionLocal  # Import the session
import requests  # For CoinGecko API calls
import os
import sys
from typing import Dict, Any

# Add the directory containing your modules to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing function - adjust the import path as needed
try:
    from data.fetchBinance import fetch_binance_data
except ImportError:
    # Fallback function if import fails
    def fetch_binance_data() -> Dict[str, str]:
        return {"error": "Binance data module not found"}

app = FastAPI(title="Crypto Trading API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="/opt/lampp/htdocs/bot/frontend/dist"), name="static")
@app.get('/api/binance-data')
async def get_binance_data():
    try:
        data = await fetch_binance_data()
        return data
    except Exception as e:
        print(f"Error in /api/binance-data: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/coingecko')
async def get_coingecko_data(vs_currency: str = 'usd', days: int = 30):
    try:
        days = min(days, 30)  # Limit to a maximum of 30 days
        
        # Log the request parameters
        print(f"Requesting CoinGecko data with parameters: vs_currency={vs_currency}, days={days}")
        
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {
            'vs_currency': vs_currency,
            'days': days
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Log the response from CoinGecko
        data = response.json()
        print(f"Received response from CoinGecko: {data}")
        
        return data
    except Exception as e:
        print(f"Error in /api/coingecko: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get('/health')
def health_check():
    return {"status": "healthy"}

@app.get('/api/price-data/models')
def get_price_data_models():
    try:
        # Return a list of available model types
        available_models = [
            {"name": "lstm", "enabled": True},
            {"name": "Random Forest", "enabled": True},
            {"name": "XGBoost", "enabled": True},
            {"name": "rnn_lstm", "enabled": True},
        ]
        return {"models": available_models}  # Return models as a list of dictionaries
    except Exception as e:
        print(f"Error fetching models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# The following block is not needed when using uvicorn
# if __name__ == '__main__':
#     print("Starting unified API server on port 5001...")  # Changed port to 5001
#     app.run(debug=True, host='0.0.0.0', port=5001)  # Changed port to 5001
