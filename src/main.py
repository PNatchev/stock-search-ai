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
"""

trading_agent = Agent(
    name="Trading Research Agent",
    tools=[get_bars],  
    model="gpt-5-mini",
    model_settings=ModelSettings(tool_choice="required"),
    instructions=INSTRUCTIONS
)

async def main():
    message = "Analyze NVDA and provide entry and exit points for trading. Use 5-minute bars from the last 3 days."
    
    with trace("Trading Analysis"):
        result = await Runner.run(trading_agent, message)
    
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())