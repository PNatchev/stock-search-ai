#!/usr/bin/env python3
"""
Stock Search AI - Main Application Entry Point

This is the main entry point for the stock search AI application.
"""

from dotenv import load_dotenv
import os



# Load .env from config directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
env_path = os.path.join(project_root, "config", ".env")
load_dotenv(env_path, override=True)


print("hello")
