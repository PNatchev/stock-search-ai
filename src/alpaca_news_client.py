import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import function_tool
from alpaca.data.historical import NewsClient
from alpaca.data.requests import NewsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import json

# Load .env from config directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, "config", ".env")
load_dotenv(env_path, override=True)

client = NewsClient(
    api_key=os.getenv("ALPACA_API_KEY"),
    secret_key=os.getenv("ALPACA_SECRET_KEY"),
)

# Fetch news
news_response = client.get_news(NewsRequest(
    symbol="NVDA",
    start=datetime.now() - timedelta(days=1),
    end=datetime.now(),
    limit=5
))

# Extract only headline and URL using dot notation
filtered_news = [
    {"headline": article.headline, "url": article.url}
    for article in news_response.data["news"]
]

# Convert to JSON
news_json = json.dumps(filtered_news, indent=4)

# Print JSON
print(news_json)