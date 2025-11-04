import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import function_tool
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

# Load .env from config directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, "config", ".env")
load_dotenv(env_path, override=True)

client = StockHistoricalDataClient(
    api_key=os.getenv("ALPACA_API_KEY"),
    secret_key=os.getenv("ALPACA_SECRET_KEY"),
)



request_params = StockBarsRequest(
    symbol_or_symbols="NVDA",
    start=datetime.now() - timedelta(days=1),
    end=datetime.now(),
    timeframe=TimeFrame(amount=5, unit=TimeFrameUnit.Minute),
)



bars = client.get_stock_bars(request_params)


class GetBarsParams(BaseModel):
    """Parameters for fetching stock bar data."""
    symbol: str = Field(..., description="Stock ticker symbol (e.g., 'AAPL', 'NVDA', 'MSFT')")
    start: str = Field(..., description="Start date in ISO format (YYYY-MM-DD) or relative like '1 day ago'")
    end: str = Field(..., description="End date in ISO format (YYYY-MM-DD) or 'now' for current time")
    timeframe_amount: int = Field(1, description="Amount for timeframe (e.g., 1, 5, 15)")
    timeframe_unit: str = Field("Minute", description="Timeframe unit: 'Minute', 'Hour', 'Day', 'Week', 'Month'")


@function_tool
def get_bars(params: GetBarsParams) -> dict:
    """
    Fetch stock bar data (OHLCV) for a given symbol and time range.
    
    Returns a dictionary with:
    - 'symbol': stock symbol
    - 'data': list of dictionaries, each containing timestamp, open, high, low, close, volume, etc.
    - 'count': number of bars returned
    """
 
    if params.end.lower() == 'now':
        end_date = datetime.now()
    else:
        end_date = datetime.fromisoformat(params.end.replace('Z', '+00:00'))
    
    if 'ago' in params.start.lower():
        days_ago = int(params.start.split()[0])
        start_date = datetime.now() - timedelta(days=days_ago)
    else:
        start_date = datetime.fromisoformat(params.start.replace('Z', '+00:00'))
    
    unit_map = {
        'minute': TimeFrameUnit.Minute,
        'hour': TimeFrameUnit.Hour,
        'day': TimeFrameUnit.Day,
        'week': TimeFrameUnit.Week,
        'month': TimeFrameUnit.Month,
    }
    timeframe_unit = unit_map.get(params.timeframe_unit.lower(), TimeFrameUnit.Minute)
    timeframe = TimeFrame(amount=params.timeframe_amount, unit=timeframe_unit)
    
    request_params = StockBarsRequest(
        symbol_or_symbols=params.symbol,
        start=start_date,
        end=end_date,
        timeframe=timeframe,
    )
    bars = client.get_stock_bars(request_params)
    
    df = bars.df.reset_index()
    df['timestamp'] = df['timestamp'].astype(str)
    
    # Limit to last 500 bars to avoid exceeding token limits (enough for technical analysis)
    # Keep only essential OHLCV fields to reduce data size
    df_limited = df.tail(500)[['timestamp', 'open', 'high', 'low', 'close', 'volume']].copy()
    
    return {
        'symbol': params.symbol,
        'data': df_limited.to_dict('records'),
        'count': len(df_limited),
        'total_bars_available': len(df)
    }
