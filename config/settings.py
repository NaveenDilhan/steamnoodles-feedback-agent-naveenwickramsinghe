"""
Configuration settings for SteamNoodles Multi-Agent Framework
"""

import os
from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# If no environment variable, you can set it directly here (not recommended for production)
# OPENAI_API_KEY = 'your-openai-api-key-here'

# LLM Settings
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 200

# File Paths
DATA_DIR = 'data'
OUTPUT_DIR = 'outputs'
REVIEWS_FILE = 'restaurant_reviews.csv'

# Visualization Settings
FIGURE_SIZE = (12, 8)
DPI = 300
PLOT_STYLE = 'seaborn-v0_8'

# Date Range Settings
DEFAULT_DAYS_BACK = 30
MAX_DAYS_BACK = 365

# Agent Settings
AGENT_VERBOSE = True
MAX_AGENT_ITERATIONS = 3

# Sample Data Generation Settings
DEFAULT_SAMPLE_SIZE = 200
SENTIMENT_WEIGHTS = {
    'positive': 0.5,
    'negative': 0.3,
    'neutral': 0.2
}

# Validation
def validate_config():
    """Validate configuration settings"""
    if not OPENAI_API_KEY:
        print("WARNING: OpenAI API key not found!")
        print("Please set OPENAI_API_KEY in environment variables or in this file.")
        return False
    return True

if __name__ == "__main__":
    validate_config()