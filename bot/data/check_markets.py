import httpx
import asyncio

async def check_markets_and_fetch_assets():
    url = "https://api.bitvavo.com/v2/markets"  # Endpoint for fetching market data
    asset_data = await fetch_asset_data()  # Fetch asset data
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            markets = response.json()
            print("Available markets:")
            for market in markets:
                print(market['market'])  # Print each market symbol
            return markets, asset_data  # Return both markets and asset data
        else:
            print(f"Error fetching markets: {response.status_code} - {response.text}")
            return []

if __name__ == "__main__":
    asyncio.run(check_markets())
