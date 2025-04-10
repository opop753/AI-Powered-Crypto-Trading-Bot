import time, os, sys, logging
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from backend.api.historicaldata import router  # Import the router from historicaldata.py
import httpx  # Importing httpx for making HTTP requests
from datetime import datetime, timedelta
from backend.models.model import Model
from sqlalchemy.orm import Session, relationship
from backend.database import SessionLocal
#from bot.data.fetchYahooFinance import fetch_yfinance_data
from bot.data.fetchBitvavo import fetch_bitvavo_candlestick_data
from bot.data.fetchBinance import fetch_binance_data, fetch_binance_candlestick_data
from bot.data.fetchBitvavoWithBacktesting import fetch_bitvavo_data
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from bot.models.models import Model
from bot.models.rnn_lstm import RNNLSTM
from bot.models.xgboost import XGBoost
from bot.models.lstm import LSTM
from bot.models.random_forest import RandomForest
from bot.models.fetchall import fetchall
from fastapi.security import OAuth2PasswordBearer
from authlib.integrations.starlette_client import OAuth
import uuid

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="/opt/lampp/htdocs/frontend"), name="static")

class User(BaseModel):
    username: str
    password: str
    email: str
    provider: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)  # Include the router for API endpoints

@app.get("/") 
async def root():
    return FileResponse("/opt/lampp/htdocs/frontend/index.html")

@app.get("/welcome")
async def welcome():
    return FileResponse("/opt/lampp/htdocs/frontend/index.html")

@app.get("/dashboard")
async def dashboard():
    return FileResponse("/opt/lampp/htdocs/frontend/dashboard.html")

@app.get("/logout")
async def logout(response: Response):
    # Clear cookies/session data
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_token")
    response.delete_cookie(key="user_id")
    return response

@app.get("/logout-page")
async def logout_page():
    return FileResponse("/opt/lampp/htdocs/frontend/logout.html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/models")
async def get_models(db: Session = Depends(get_db)):
    models = db.query(Model).all()
    return [model.to_dict() for model in models]

def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

@app.post("/api/register")
async def register(user: User, db: Session = Depends(get_db)):  # Corrected line
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password=hashed_password, email=user.email, provider=user.provider)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully!"}

@app.post("/api/login")
async def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and pwd_context.verify(user.password, db_user.password):
        return {"message": "Login successful!"}
    raise HTTPException(status_code=400, detail="Invalid credentials")


@app.get("/api/binance/candlestick")
async def get_binance_candlestick_data(market: str, interval: str, start_time: float, end_time: float):
    response = await fetch_binance_candlestick_data(market, interval, start_time, end_time)
    return JSONResponse(content=response)

@app.get("/api/fetch/binance")
async def fetch_binance(market: str, interval: str, start_time: float, end_time: float):
    logging.info(f"Fetching Binance data for market: {market}, interval: {interval}, start_time: {start_time}, end_time: {end_time}")
    response = await fetch_binance_data(market, interval, start_time, end_time)
    return JSONResponse(content=response)

@app.post("/api/train_cnn")
async def train_cnn(training_data: dict, db: Session = Depends(get_db)):
    """
    Train the CNN model with the provided training data.
    """
    X_train = training_data.get("X_train")
    y_train = training_data.get("y_train")
    
    if X_train is None or y_train is None:
        raise HTTPException(status_code=400, detail="Training data is required.")
    
    model = train_CNN(X_train, y_train)  # Call the train_CNN function
    return {"message": "Model trained successfully!"}

@app.post("/api/train_lstm")
async def train_lstm(training_data: dict):
    """
    Train the LSTM model with the provided training data.
    """
    X_train = training_data.get("X_train")
    y_train = training_data.get("y_train")
    
    if X_train is None or y_train is None:
        raise HTTPException(status_code=400, detail="Training data is required.")
    
    # Initialize and train the LSTM model
    model = LSTM()
    model.train(X_train, y_train)
    return {"message": "LSTM model trained successfully!"}

@app.post("/api/train_rnn_lstm")
async def train_rnn_lstm(training_data: dict):
    """
    Train the RNN-LSTM model with the provided training data.
    """
    X_train = training_data.get("X_train")
    y_train = training_data.get("y_train")
    
    if X_train is None or y_train is None:
        raise HTTPException(status_code=400, detail="Training data is required.")
    
    # Initialize and train the RNN-LSTM model
    model = RNNLSTM()
    model.train(X_train, y_train)
    return {"message": "RNN-LSTM model trained successfully!"}

@app.post("/api/train_xgboost")
async def train_xgboost(training_data: dict):
    """
    Train the XGBoost model with the provided training data.
    """
    X_train = training_data.get("X_train")
    y_train = training_data.get("y_train")
    
    if X_train is None or y_train is None:
        raise HTTPException(status_code=400, detail="Training data is required.")
    
    # Initialize and train the XGBoost model
    model = XGBoost()
    model.train(X_train, y_train)
    return {"message": "XGBoost model trained successfully!"}

@app.post("/api/train_random_forest")
async def train_random_forest(training_data: dict):
    """
    Train the Random Forest model with the provided training data.
    """
    X_train = training_data.get("X_train")
    y_train = training_data.get("y_train")
    
    if X_train is None or y_train is None:
        raise HTTPException(status_code=400, detail="Training data is required.")
    
    # Initialize and train the Random Forest model
    model = RandomForest()
    model.train(X_train, y_train)
    return {"message": "Random Forest model trained successfully!"}

@app.get("/api/predict/{model_name}")
async def predict(model_name: str, market: str):
    """
    Make a prediction using the specified model for the given market.
    """
    try:
        # In a real application, you would load the latest data for the market
        # For demonstration purposes, we'll return a simulated prediction
        
        import random
        prediction = random.randint(0, 1)  # 0 = down, 1 = up
        confidence = random.uniform(0.6, 0.95)  # Random confidence between 60% and 95%
        
        # In production, you would use the actual trained model
        # For example:
        # if model_name == "lstm":
        #     model = LSTM()
        #     model.load()
        #     prediction, confidence = model.predict(latest_data)
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "model": model_name,
            "market": market,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Initialize OAuth
oauth = OAuth()

# Configure Google OAuth
oauth.register(
    name='google',
    client_id='123456789012-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com',  # Replace with your actual client ID
    client_secret='GOCSPX-abcdefghijklmnopqrstuvwxyz',  # Replace with your actual client secret
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth/google/callback',
    client_kwargs={'scope': 'email profile'},
)

# Configure Facebook OAuth
oauth.register(
    name='facebook',
    client_id='1234567890123456',  # Replace with your actual Facebook App ID
    client_secret='1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p',  # Replace with your actual Facebook App Secret
    authorize_url='https://www.facebook.com/v12.0/dialog/oauth',
    authorize_params=None,
    access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth/facebook/callback',
    client_kwargs={'scope': 'email'},
)

# Google OAuth routes
@app.get('/auth/google')
async def google_login(request: Request):
    redirect_uri = 'http://localhost:8000/auth/google/callback'
    return await oauth.google.authorize_redirect(request, redirect_uri)

async def create_or_login_user(email: str, provider: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Create new user
        user = User(
            username=email.split('@')[0],
            email=email,
            password=pwd_context.hash(str(uuid.uuid4())),  # Random password
            provider=provider
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@app.get('/auth/google/callback')
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    email = user_info['email']
    user = await create_or_login_user(email, 'google', db)
    return RedirectResponse(url='/welcome')

# Facebook OAuth routes
@app.get('/auth/facebook')
async def facebook_login(request: Request):
    redirect_uri = 'http://localhost:8000/auth/facebook/callback'
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

@app.get('/auth/facebook/callback')
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.facebook.authorize_access_token(request)
    user_info = await oauth.facebook.get('me?fields=email')
    email = user_info.json()['email']
    user = await create_or_login_user(email, 'facebook', db)
    return RedirectResponse(url='/welcome')
