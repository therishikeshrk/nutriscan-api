import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    GOOGLE_ANALYTICS_ID = os.getenv('NEXT_PUBLIC_GOOGLE_ANALYTICS_ID')
    GOOGLE_AI_API_KEY = os.getenv('NEXT_PUBLIC_GOOGLE_AI_API_KEY')
    # Add other configurations as needed
