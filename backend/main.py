from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import subprocess  # Import subprocess to check network status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Correctly import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from backend.api.historicaldata import router as historicaldata_router
from datetime import datetime, timedelta
import json
from backend.database import get_db  # Import the get_db function
import httpx

app = FastAPI()

# Check if NetworkManager is active
if subprocess.call(["systemctl", "is-active", "--quiet", "NetworkManager"]) != 0:
    raise HTTPException(status_code=503, detail="NetworkManager is not active. Please check your network settings.")

# Configure CORS
app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4173", "http://localhost:5173"],  # Allow both frontend origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include the historicaldata router
app.include_router(historicaldata_router, prefix="/api")

# Model schemas
class MLModel(BaseModel):
    id: str
    name: str
    description: str
    enabled: bool
    order: int

class ModelUpdate(BaseModel):
    enabled: Optional[bool] = None
    deleted: Optional[bool] = None

class ModelReorder(BaseModel):
    modelIds: List[str]

# In-memory storage (replace with your database)
models = [
    {
        "id": "1",
        "name": "LSTM Network",
        "description": "Long Short-Term Memory neural network for sequence prediction",
        "enabled": True,
        "order": 1,
    },
    {
        "id": "2",
        "name": "CNN Model",
        "description": "Convolutional Neural Network for pattern recognition",
        "enabled": False,
        "order": 2,
    },
]

@app.get("/api/models")
async def get_models(skip: int = 0, limit: int = 10):
    model_list = [{"id": model["id"], "name": model["name"], "description": model["description"], "enabled": model["enabled"], "order": model["order"]} for model in models]
    print("Models being returned:", model_list)  # Debugging line
    return {"models": [{"id": model["id"], "name": model["name"], "description": model["description"], "enabled": model["enabled"], "order": model["order"]} for model in models]}

@app.patch("/api/models/{model_id}")
async def update_model(model_id: str, update: ModelUpdate, db: Session = Depends(get_db)):
    for model in models:
        if model["id"] == model_id:
            if update.enabled is not None:
                model["enabled"] = update.enabled
            if update.deleted:
                models.remove(model)
            return model
    raise HTTPException(status_code=404, detail="Model not found")

@app.post("/api/models/reorder")
async def reorder_models(reorder: ModelReorder):
    global models
    if len(reorder.modelIds) != len(models):
        raise HTTPException(status_code=400, detail="Invalid model ID list")
    
    new_models = []
    for idx, model_id in enumerate(reorder.modelIds):
        model = next((m for m in models if m["id"] == model_id), None)
        if not model:
            raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
        model["order"] = idx + 1
        new_models.append(model)
    
    models = new_models
    return models

@app.get("/api/price-data/binance")
async def get_price_data(market: str):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={market}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

@app.get("/api/candles/{market}")
async def get_candles(market: str):
    url = f"https://api.bitvavo.com/v2/{market}/candles"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    
@app.get("/api/price-data/yahoo")
async def get_yahoo_data():
    # Mock response for the /api/price-data/yahoo endpoint
    return {
        "data": [
            {"timestamp": "2023-01-01T00:00:00Z", "price": 29000, "volume": 450},
            {"timestamp": "2023-01-01T01:00:00Z", "price": 29500, "volume": 550},
            {"timestamp": "2023-01-01T02:00:00Z", "price": 30000, "volume": 650}
        ]
    }
