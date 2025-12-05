"""Configuration settings for the investor recommendation system."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model Configuration
ANTHROPIC_MODEL = "claude-sonnet-4-5-20250929"  # or claude-3-opus-20240229, claude-3-sonnet-20240229

# Data Configuration
DATA_FILE_PATH = "DATA/Investor DATA - Airtable (DFD) .xlsx"
CONTACTS_FILE_PATH = "DATA/Investor DATA - Contacts (DFD).xlsx"
PITCHBOOK_CONTACTS_FILE_PATH = "DATA/Investor DATA - Pitchbook Contacts.xlsx"
PITCH_DECKS_FOLDER = "Pitch Decks"

# Search Configuration
MAX_INVESTORS_TO_SHOW = 725  # Search entire database for better recommendations
MAX_INVESTORS_TO_CLAUDE = 10  # Maximum investors to send to Claude (reduced for efficiency with vector search)

# Results Configuration
RESULTS_FILE_PATH = "results/query_results.json"  # Path to save query results (JSON)
MARKDOWN_RESULTS_DIR = "results/markdown"  # Directory to save individual markdown files

# Validation
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Please set it in .env file.")

