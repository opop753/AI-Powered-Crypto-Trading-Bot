#!/bin/bash

# Function to display user-friendly messages
function display_message {
    echo "$1"
}

# Check if NetworkManager is active
if ! systemctl is-active --quiet NetworkManager; then
    display_message "NetworkManager is not active. Please check your network settings."
    exit 1
fi

# Restart Backend
display_message "Starting Backend..."
cd ./backend
pkill -f api.py
PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload > backend_startup.log 2>&1 &

# Check if Backend is running
if pgrep -f "api.py" > /dev/null; then
    display_message "Backend is running."
else
    display_message "Backend failed to start."
    exit 1
fi

# Restart API
display_message "Starting API..."
curl -f http://localhost:3000/health || { display_message "API is not responding."; exit 1; }

# Restart Frontend
display_message "Starting Frontend..."
cd ../trading-bot-frontend
fuser -k 3001/tcp # Kill any process using port 3001
pkill -f "npm start" # Stop any existing frontend process

# Check if port 3001 is occupied
if lsof -i:3001; then
    display_message "Port 3001 is occupied. Please enter a different port:"
    read PORT
else
    PORT=3001
fi

# Start frontend and log errors to console
PORT=$PORT npm start || { display_message "Frontend failed to start."; exit 1; }
sleep 5 # Wait for the frontend to start

# Check if Frontend is running
if pgrep -f "npm start" > /dev/null; then
    display_message "Frontend is running."
else
    display_message "Frontend failed to start."
    exit 1
fi

# Open the project pages in Google Chrome
if ! pgrep -f "google-chrome" > /dev/null; then
    google-chrome &
fi
google-chrome http://localhost:3000 http://localhost:3001 http://localhost:3001/health &

# Close Google Chrome after services are restarted
pkill -f "google-chrome"

display_message "All services restarted successfully."
