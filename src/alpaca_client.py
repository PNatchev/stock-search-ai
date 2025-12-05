import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import function_tool
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

# Load environment variables
# For Hugging Face Spaces: use environment variables directly
# For local development: load from .env file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, "config", ".env")
# Only load .env if it exists (for local development)
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)

# Initialize client (will use environment variables from HF Spaces or .env file)
api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

if not api_key or not secret_key:
    raise ValueError(
        "ALPACA_API_KEY and ALPACA_SECRET_KEY must be set as environment variables. "
        "For Hugging Face Spaces, add them as secrets in Space settings."
    )

# Note: Alpaca API keys determine sandbox vs production mode
# Sandbox keys start with different prefixes than production keys
# If you get subscription errors on HF Spaces, ensure you're using PRODUCTION keys, not sandbox keys
client = StockHistoricalDataClient(
    api_key=api_key,
    secret_key=secret_key,
)


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
    
    try:
        bars = client.get_stock_bars(request_params)
    except Exception as e:
        error_msg = str(e)
        # Provide helpful error messages for common issues
        if "subscription" in error_msg.lower() or "403" in error_msg or "unauthorized" in error_msg.lower():
            raise Exception(
                f"Alpaca API subscription error: {error_msg}\n\n"
                "Possible solutions:\n"
                "1. Verify your API keys are production keys (not sandbox keys)\n"
                "2. Check your Alpaca subscription tier allows API access\n"
                "3. For Hugging Face Spaces, ensure API keys are set as secrets\n"
                "4. Contact Alpaca support if you need to upgrade your subscription"
            )
        raise
    
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
