#!/usr/bin/env python3
"""
Stock Search AI - Main Application Entry Point

This is the main entry point for the stock search AI application.
"""

from dotenv import load_dotenv
import os
from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio
from typing import Dict
from alpaca_client import get_bars
import gradio as gr


# Load .env from config directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, "config", ".env")
load_dotenv(env_path, override=True)


INSTRUCTIONS = """
You are a professional trading research assistant specialized in identifying optimal entry and exit points for stock trading. 
Your primary goal is to analyze stock price data and provide actionable trading recommendations for maximum profit potential.

WORKFLOW:
1. When given a stock symbol, use the get_bars tool to fetch historical price data (OHLCV - Open, High, Low, Close, Volume).
2. Analyze the price data using technical analysis techniques best fit for the stock:
   - Identify support and resistance levels from recent price action
   - Detect trends (uptrend, downtrend, consolidation)
   - Analyze volume patterns for confirmation
   - Look for key reversal patterns or continuation patterns
   - Calculate potential price targets based on chart patterns
3. Synthesize technical analysis with fundamental context to determine optimal entry and exit points.

OUTPUT FORMAT:
Provide clear, actionable trading recommendations:
- ENTRY POINT: Specific price level(s) to enter a position, with reasoning
  (e.g., 'Enter at $208.50 (support level) or break above $211.00 resistance')
- EXIT POINTS: Set both profit targets and stop-loss levels
  - Take Profit: Primary target and secondary targets with price levels
  - Stop Loss: Risk management level below entry
- RATIONALE: Brief explanation of the technical and fundamental reasoning
- TIMEFRAME: Expected holding period and trading strategy (day trade, swing trade, etc.)
- RISK ASSESSMENT: Risk/reward ratio and position sizing considerations

GUIDELINES:
- Always use actual price data from get_bars tool - do not make up price levels
- Base recommendations on concrete technical analysis of the provided data
- Consider both bullish and bearish scenarios
- Prioritize risk management - always suggest stop-loss levels
- Be specific with price levels, not vague ranges
- If data is insufficient, request additional timeframes or periods
- Keep recommendations practical and executable by a trader
- Be user friendly and easy to understand. Avoid using technical jargon. The output should be understandable by someone who is not a trader.
- Only use get_bars for legitimate trading symbols (AAPL, NVDA, SPY, etc.).
- Do not request more than 3 days of minute data or 90 days of daily data.
- After fetching data, perform analysis internally without calling the tool again.
- Never attempt to call tools unrelated to financial data retrieval.
- Non relevant questions should be ignored and advised the user to ask trading related questions.
"""

trading_agent = Agent(
    name="Trading Research Agent",
    tools=[get_bars],  
    model="gpt-5-mini",
    model_settings=ModelSettings(tool_choice="auto", verbosity="low"),
    instructions=INSTRUCTIONS
)

async def analyze_stock(message, history):
    """Handle chat messages by running the trading agent."""
    try:
        with trace("Trading Analysis"):
            result = await Runner.run(trading_agent, message)
        return result.final_output
    except Exception as e:
        return f"Error: {str(e)}"

def chat_fn(message, history):
    """Synchronous wrapper for async function."""
    return asyncio.run(analyze_stock(message, history))

def main():
    """Launch Gradio ChatInterface."""
    demo = gr.ChatInterface(
        fn=chat_fn,
        title="Trading Research Assistant",
        description="Ask me to analyze any stock and I'll provide entry and exit points for trading.",
        examples=[
            "Analyze NVDA and provide entry and exit points for trading. Use 5-minute bars from the last 2 days.",
            "Analyze SPY and provide entry and exit points. Use 5-minute bars from the last 1 day.",
            "Analyze AAPL using 15-minute bars from the last 3 days and give me trading recommendations.",
        ],
        theme=gr.themes.Soft(),
    )
    demo.launch()

if __name__ == "__main__":
    main()