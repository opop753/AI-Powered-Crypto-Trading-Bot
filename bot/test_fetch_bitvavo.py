import os
from data.fetchBitvavo import fetch_bitvavo_data

# Set environment variables for testing
# Ensure that the API key and secret are set
if 'BITVAVO_API_KEY' not in os.environ or 'BITVAVO_API_SECRET' not in os.environ:
    raise EnvironmentError("Please set the BITVAVO_API_KEY and BITVAVO_API_SECRET environment variables.")

os.environ['BITVAVO_API_KEY'] = 'actual_api_key_here'  # Replace with actual key
os.environ['BITVAVO_API_SECRET'] = 'actual_api_secret_here'  # Replace with actual secret

# Test the fetch_bitvavo_data function with error handling
try:
    data = fetch_bitvavo_data()
    print(data)
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check your API key and secret, and ensure the Bitvavo API is accessible.")
if __name__ == "__main__":
    data = fetch_bitvavo_data()
    print(data)
