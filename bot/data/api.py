from flask import Flask, jsonify, request
import pandas as pd  # Import pandas for DataFrame operations
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import mysql.connector
import requests  # Import requests for making API calls

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)
bcrypt = Bcrypt(app)

# Database connection
db_config = {
    'user': 'dim',
    'password': '1304',
    'host': 'localhost',
    'database': 'your_database'
}
from flask_cors import CORS
from .fetchBitvavo import fetch_bitvavo_data
from .fetchBinance import fetch_binance_data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Connect to the database and insert the new user
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Connect to the database and verify user
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and bcrypt.check_password_hash(result[0], password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401
@app.route('/api/binance', methods=['GET'])
# This endpoint fetches data from the Bitvavo API
async def get_binance_data():
    binance_data = await fetch_binance_data()  # Ensure this is awaited
    return jsonify(binance_data.to_dict(orient='records'))

# Duplicate route definition removed

@app.route('/api/bitvavo', methods=['GET'])
def get_bitvavo_data():
    try:
        bitvavo_data = fetch_bitvavo_data()
    except Exception as e:
        print(f"Error fetching Bitvavo data: {e}")
        return jsonify({"error": "Failed to fetch data from Bitvavo"}), 500
    return jsonify(bitvavo_data.to_dict(orient='records'))

def prepare_bitvavo_data(data):
    df = pd.DataFrame(data)  # Convert list of dictionaries to DataFrame
    # Example processing: Add a new feature, normalize data, etc.
    if 'close' in df.columns:
        df['price_change'] = df['close'].diff()  # Calculate price change
    else:
        df['price_change'] = None  # Set to None or handle as needed if 'close' is not present
    df.dropna(inplace=True)  # Remove rows with NaN values
    return df

@app.route('/api/analyze_bitvavo', methods=['GET'])
def analyze_bitvavo():
    data = fetch_bitvavo_data()
    print(data)  # Log the data structure for debugging
    df = pd.DataFrame(data)  # Convert list of dictionaries to DataFrame
    processed_data = prepare_bitvavo_data(df)
    return jsonify(processed_data.to_dict(orient='records'))  # Convert DataFrame to JSON serializable format
@app.route('/api/price-data/yahoo', methods=['GET'])
def get_yahoo_data():
    try:
        yahoo_data = fetch_yfinance_data()
    except Exception as e:
        print(f"Error fetching Yahoo data: {e}")
        return jsonify({"error": "Failed to fetch data from Yahoo"}), 500
    return jsonify(yahoo_data)

@app.route('/api/coingecko', methods=['GET'])
def get_coingecko_data():
    vs_currency = request.args.get('vs_currency', 'usd')
    days = request.args.get('days', '30')
    
    # Here you would typically call the CoinGecko API to fetch the data
    # For example, using requests or another HTTP client
    try:
        # Example of fetching data from CoinGecko API
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/markets', params={
            'vs_currency': vs_currency,
            'days': days
        })
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()  # Parse the JSON response
        return jsonify(data)  # Return the data as JSON
    except Exception as e:
        print(f"Error fetching CoinGecko data: {e}")
        return jsonify({"error": "Failed to fetch data from CoinGecko"}), 500
def home():
    return app.send_static_file('under_construction.html')

if __name__ == '__main__':
    app.run(debug=True)
