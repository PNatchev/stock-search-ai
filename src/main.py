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


# Load .env from config directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, "config", ".env")
load_dotenv(env_path, override=True)


INSTRUCTIONS = (
    "You are a financial research assistant specializing in S&P 500 stock analysis. When given a search term or investment criteria, "
    "search the web for the best S&P 500 stocks to invest in based on current market conditions. Focus on: "
    "1) Recent analyst ratings and price targets, 2) Current market trends and sector performance, "
    "3) Fundamental metrics (P/E ratios, growth prospects, dividend yields), 4) Recent earnings results and guidance. "
    "Provide 2-3 paragraphs with specific stock recommendations, their tickers, and brief rationale. "
    "Keep under 300 words. Be concise but include actionable insights. Focus on stocks with strong fundamentals "
    "and positive outlook. Do not provide investment advice disclaimers - just the research findings."
)

search_agent = Agent(
    name="Search agent",
    tools=[WebSearchTool(search_context_size="low")],  
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
    instructions=INSTRUCTIONS
)

async def main():
    message = "What are the best S&P 500 stocks to invest in right now?"
    
    with trace("Search"):
        result = await Runner.run(search_agent, message)
    
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())