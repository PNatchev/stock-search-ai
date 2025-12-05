"""
Hugging Face Spaces Entry Point
This file is used by Hugging Face Spaces to launch the Gradio app.
"""

import sys
import os

# Add src directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main application
from main import main

if __name__ == "__main__":
    main()

