from datetime import datetime
from typing import Dict, Any
from .BaseFetcher import BaseFetcher

class BitvavoFetcher(BaseFetcher):
    def __init__(self):
        super().__init__("https://api.bitvavo.com/v2/candlestick")
        self.client.headers.update({'Bitvavo-Access-Version': '2'})

    def build_params(self, symbol: str, interval: str, limit: int = 100, **kwargs) -> Dict[str, Any]:
        # Convert to Bitvavo's expected timestamp format (seconds)
        end_time = int(datetime.now().timestamp())
        start_time = end_time - (24 * 3600)  # 24 hours
        
        return {
            'symbol': symbol,
            'interval': interval,
            'start': start_time * 1000,  # Convert to milliseconds
            'end': end_time * 1000,
            'limit': limit
        }

    def parse_response(self, data: list) -> list:
        return [{
            'timestamp': entry[0],
            'open': float(entry[1]),
            'high': float(entry[2]),
            'low': float(entry[3]),
            'close': float(entry[4]),
            'volume': float(entry[5])
        } for entry in data]