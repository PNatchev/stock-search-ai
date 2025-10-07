# Stock Search AI

An intelligent AI-powered application that uses OpenAI's agents framework to research and recommend the best S&P 500 stocks for investment based on real-time web data and financial analysis.

## 🚀 Features

- **AI-Powered Research**: Uses OpenAI's GPT-4o-mini with web search capabilities
- **S&P 500 Focus**: Specialized in analyzing S&P 500 stocks specifically
- **Real-Time Data**: Leverages web search to get current market information
- **Comprehensive Analysis**: Evaluates stocks based on:
  - Recent analyst ratings and price targets
  - Current market trends and sector performance
  - Fundamental metrics (P/E ratios, growth prospects, dividend yields)
  - Recent earnings results and guidance
- **Actionable Insights**: Provides specific stock recommendations with tickers and rationale
- **Tracing Support**: Built-in execution tracing for debugging and monitoring

## 🛠️ Technology Stack

- **AI Framework**: OpenAI Agents SDK
- **Language Model**: GPT-4o-mini
- **Web Search**: WebSearchTool integration
- **Python**: Async/await support for concurrent operations
- **Configuration**: Environment-based settings management

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection for web search functionality

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

3. **Set up environment variables**:
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env and add your OpenAI API key
   ```

### Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the stock research agent
python src/main.py
```

The application will automatically search for the best S&P 500 stocks to invest in and provide a comprehensive analysis with specific recommendations.

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
│   ├── settings.py     # Settings management
│   └── .env.example    # Environment variables template
└── src/                # Source code directory
    ├── __init__.py     # Package initialization
    └── main.py         # Main application entry point
```

## ⚙️ Configuration

The application loads configuration from `config/.env`. Required variables:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Custom model settings
# OPENAI_MODEL=gpt-4o-mini
```

## 🔍 How It Works

1. **Initialization**: Creates an AI agent with web search capabilities
2. **Research**: The agent searches the web for current S&P 500 stock information
3. **Analysis**: Evaluates stocks based on multiple financial criteria
4. **Recommendation**: Provides specific stock picks with reasoning
5. **Output**: Delivers concise, actionable investment insights

## 📊 Sample Output

The application provides research findings in a structured format:
- Stock recommendations with ticker symbols
- Brief rationale for each recommendation
- Current market context and trends
- Key metrics and analyst insights

## 🛡️ Disclaimer

This application is for educational and research purposes only. The information provided should not be considered as financial advice. Always conduct your own research and consult with financial professionals before making investment decisions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Built with ❤️ using OpenAI's Agents Framework**