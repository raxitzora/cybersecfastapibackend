import os
from dotenv import load_dotenv
load_dotenv()

#Groq model for basic tasks
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_MODEL = os.getenv("GROQ_MODEL")


#metallama model for research
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
LLAMA_API_URL=os.getenv("LLAMA_API_URL")
LLAMA_MODEL=os.getenv("LLAMA_MODEL")


#code writing
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL=os.getenv("DEEPSEEK_API_URL")
DEEPSEEK_MODEL=os.getenv("DEEPSEEK_MODEL")

#router model for routing
MISTRAL_API_KEY=os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL=os.getenv("MISTRAL_API_URL")
MISTRAL_MODEL=os.getenv("MISTRAL_MODEL")
