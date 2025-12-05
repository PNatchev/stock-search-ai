---
title: stock_search_ai
app_file: app.py
sdk: gradio
sdk_version: 5.49.1
---
# Stock Search AI

An intelligent AI-powered trading research assistant that analyzes real-time stock market data to provide actionable entry and exit points for maximum profit potential. Built with OpenAI's agents framework and integrated with Alpaca Markets API for live stock data.

## 🚀 Features

- **AI-Powered Trading Analysis**: Uses OpenAI's GPT models to analyze stock price data and identify optimal trading opportunities
- **Real-Time Stock Data**: Integrates with Alpaca Markets API to fetch live OHLCV (Open, High, Low, Close, Volume) bar data
- **Technical Analysis**: Automated analysis of:
  - Support and resistance levels
  - Price trends and patterns
  - Volume analysis
  - Chart patterns and reversals
- **Actionable Trading Recommendations**: Provides specific:
  - Entry points with price levels
  - Profit targets (primary and secondary)
  - Stop-loss levels for risk management
  - Risk/reward ratio calculations
- **User-Friendly Output**: Clear, easy-to-understand recommendations without excessive technical jargon
- **Tracing Support**: Built-in execution tracing for debugging and monitoring

## 🛠️ Technology Stack

- **AI Framework**: OpenAI Agents SDK
- **Language Model**: GPT models (configurable)
- **Market Data**: Alpaca Markets API (via `alpaca-py`)
- **Python**: Async/await support for concurrent operations
- **Data Processing**: Pandas for data manipulation
- **Configuration**: Environment-based settings management

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Alpaca Markets API credentials (API Key and Secret Key)
- Internet connection for API access

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd stock-search-ai
   ```

2. **Create virtual environment and install dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Or using `uv` (faster):
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env and add your API keys
   ```

### Configuration

Create `config/.env` with the following variables:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Alpaca Markets API Configuration
ALPACA_API_KEY=your_alpaca_api_key_here
ALPACA_SECRET_KEY=your_alpaca_secret_key_here
```

### Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the trading research assistant
python src/main.py
```

The application will analyze the configured stock (default: NVDA) and provide detailed trading recommendations with entry and exit points.

## 📁 Project Structure

```
stock-search-ai/
├── .venv/              # Virtual environment (not in git)
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Modern project configuration
├── README.md           # This file
├── config/             # Configuration directory
│   ├── __init__.py     # Config package initialization
│   └── .env            # Environment variables (create from .env.example)
└── src/                # Source code directory
    ├── main.py         # Main application entry point
    └── alpaca_client.py # Alpaca API integration with get_bars tool
```

## 🔍 How It Works

1. **Stock Data Fetching**: The `get_bars` tool fetches historical OHLCV data from Alpaca Markets API
2. **Technical Analysis**: The AI agent analyzes the price data to identify:
   - Support and resistance levels
   - Trends and patterns
   - Volume confirmation signals
   - Potential reversal points
3. **Recommendation Generation**: Based on the analysis, the agent provides:
   - Specific entry price levels
   - Multiple profit target levels
   - Stop-loss recommendations
   - Risk/reward calculations
4. **User-Friendly Output**: Results are presented in clear, actionable format without excessive technical jargon

## 📊 Sample Output

The application provides comprehensive trading recommendations:

```
### Trading Recommendations:

#### Entry Point
- Buy at $206.50: Support level with bullish reversal confirmation

#### Exit Points
- Take Profit 1: $210.00 (Primary Target)
- Take Profit 2: $211.00 (Secondary Target)
- Stop Loss: $205.50

### Risk Assessment
- Risk/Reward Ratio: 1:3.5
- Position Sizing: 2-5% of trading account recommended
```

## 🛠️ Customization

### Changing the Stock Symbol

Edit `src/main.py` and modify the message in the `main()` function:

```python
message = "Analyze AAPL and provide entry and exit points for trading. Use 5-minute bars from the last 3 days."
```

### Adjusting Timeframe and Period

Modify the message to change the timeframe and data period:

```python
message = "Analyze TSLA and provide entry and exit points. Use 15-minute bars from the last 5 days."
```

The `get_bars` tool accepts:
- `timeframe_amount`: 1, 5, 15, 30, etc.
- `timeframe_unit`: "Minute", "Hour", "Day"
- Date ranges: ISO format or relative ("1 day ago", "now")

## 🛡️ Disclaimer

**⚠️ IMPORTANT**: This application is for educational and research purposes only. The trading recommendations provided are based on technical analysis of historical data and should NOT be considered as financial advice. 

- Always conduct your own research and analysis
- Consult with licensed financial professionals before making trading decisions
- Past performance does not guarantee future results
- Trading involves substantial risk of loss
- Only trade with capital you can afford to lose

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ using OpenAI's Agents Framework and Alpaca Markets API**