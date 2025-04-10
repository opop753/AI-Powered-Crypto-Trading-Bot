#!/bin/bash

PORT=8000

# Function to kill processes using the port
cleanup_port() {
    echo "Finding processes using port $PORT..."
    local pids=$(lsof -ti:$PORT)
    if [ ! -z "$pids" ]; then
        echo "Found processes: $pids"
        echo "Killing processes..."
        kill -9 $pids 2>/dev/null
        sleep 1
        echo "Port $PORT cleared"
        return 0
    else
        echo "No processes found using port $PORT"
        return 1
    fi
}

# Function to start uvicorn with specified log level
start_uvicorn() {
    local log_level=$1
    # Kill existing uvicorn if running
    if [ ! -z "$UVICORN_PID" ]; then
        kill $UVICORN_PID 2>/dev/null
        wait $UVICORN_PID 2>/dev/null
    fi
    # Start uvicorn with specified log level and handle output based on mode
    if [ "$DETAIL_MODE" = "minimal" ]; then
        # Redirect stderr to filter out TensorFlow and other warnings
        uvicorn backend.app:app --host 0.0.0.0 --port $PORT --reload --log-level $log_level 2> >(grep -v -E "tensorflow|cuda|WARNING: All log messages|computation_placer") &
    else
        # Show all output in detailed mode
        uvicorn backend.app:app --host 0.0.0.0 --port $PORT --reload --log-level $log_level &
    fi
    UVICORN_PID=$!
}

# Start with warning level by default (less verbose)
start_uvicorn "warning"
DETAIL_MODE="minimal"

# Function to show help
show_help() {
    echo "
Backend launcher written by OnlyForward0613
_____________________________________________"
    echo "
Available commands:"
    echo "  h - Show this help message"
    echo "  r - Reload the backend server"
    echo "  d - Toggle between detailed and minimal logging"
    echo "  k - Kill any processes using port $PORT and restart"
    echo "  q - Quit the server"
    echo "  u - Show backend URL"
    echo "  o - Open backend URL in browser"
    echo "
Current settings:"
    echo "  Port: $PORT"
    echo "  Logging: $([[ $DETAIL_MODE = "detailed" ]] && echo "Detailed" || echo "Minimal")"
    echo
}

# Print initial instructions
echo "Backend server running. Press 'h' for help."

# Handle keyboard input
while true; do
    # Read a single character without requiring Enter
    read -rsn1 key
    
    case $key in
        h|H)
            show_help
            ;;
        r|R)
            echo "Reloading backend..."
            kill -HUP $UVICORN_PID
            ;;
        d|D)
            if [ "$DETAIL_MODE" = "minimal" ]; then
                echo "Switching to detailed logging..."
                DETAIL_MODE="detailed"
                start_uvicorn "debug"
            else
                echo "Switching to minimal logging..."
                DETAIL_MODE="minimal"
                start_uvicorn "warning"
            fi
            ;;
        k|K)
            cleanup_port
            if [ $? -eq 0 ]; then
                echo "Restarting uvicorn..."
                start_uvicorn "$([[ $DETAIL_MODE = "detailed" ]] && echo "debug" || echo "warning")"
            fi
            ;;
        q|Q)
            echo "Shutting down..."
            kill $UVICORN_PID 2>/dev/null
            exit 0
            ;;
        u|U)
            echo "Backend URL: http://localhost:$PORT/"
            ;;
        o|O)
            xdg-open "http://localhost:$PORT/"
            ;;
    esac
done
