import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join("..", ".env"))
load_dotenv(".env") # fallback

# Database Configuration
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "sales_intelligence")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")

# Gemini Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please check your .env file.")

# File Paths
FORECAST_CSV_PATH = os.path.join("data", "processed", "forecast_results.csv")
if not os.path.exists(FORECAST_CSV_PATH):
    # fallback for nested execution
    FORECAST_CSV_PATH = os.path.join("..", "data", "processed", "forecast_results.csv")
