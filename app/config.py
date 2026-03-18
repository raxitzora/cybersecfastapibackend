import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    META_API_KEY = os.getenv("META_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()