from fastapi import FastAPI
from app import app  # Import the FastAPI app from app.py using relative import

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the app on port 800
