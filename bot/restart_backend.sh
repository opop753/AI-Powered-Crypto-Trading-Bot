#!/bin/bash

# Activate the virtual environment
source /opt/lampp/htdocs/venv/bin/activate

if [ "$?" -ne 0 ]; then
    echo "Failed to activate the virtual environment. Please check the path."
    exit 1
fi

echo "Virtual environment activated. Checking for required modules..."
pip list

if [ "$1" == "--help" ]; then
    echo "Usage: $0 [--debug] or $0 [--help]"
    echo "  --debug   Run the server in debug mode, displaying errors in the terminal."
    echo "  --help    Display this help message."
    exit 0
fi

if [ "$#" -eq 0 ]; then
    echo "No parameters passed. Usage: $0 [--debug] or $0 [--help]"
    exit 1
fi

echo "Starting backend server..."
if [ "$1" == "--debug" ]; then
    echo "Running in debug mode..."
    # Start the backend server with debug options
    {
        echo "Starting the backend server..."
        echo "Executing command: PYTHONPATH=/opt/lampp/htdocs /opt/lampp/htdocs/venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload"
        PYTHONPATH=/opt/lampp/htdocs /opt/lampp/htdocs/venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload || { echo "Failed to start the backend server"; exit 1; }
    } &> /opt/lampp/htdocs/logs/backend.log | while read line; do
        if [[ "$line" == *"ModuleNotFoundError"* ]]; then
            module_name=$(echo "$line" | grep -oP "(?<=No module named ')[^']+")
            echo "Error: A required module is missing: $module_name. Please check your setup."
        elif [[ "$line" == *"running on"* ]]; then
            echo "Backend server is running."
        elif [[ "$line" == *"started"* ]]; then
            echo "Launch script started."
        fi
    done
    exit 0
else
    # Start the backend server without displaying errors and log output
    echo "Executing command: /opt/lampp/htdocs/venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload"
    /opt/lampp/htdocs/venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload || { echo "Failed to start the backend server"; exit 1; } &> /dev/null &
fi

START_TIME=$(date +%s)

END_TIME=$(date +%s)
ELAPSED_TIME=$((END_TIME - START_TIME))
echo "Backend server started. Elapsed time: $ELAPSED_TIME seconds."
