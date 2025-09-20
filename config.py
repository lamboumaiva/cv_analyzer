from dotenv import load_dotenv
import os

load_dotenv()  # charge les variables depuis .env

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

if not DEEPSEEK_API_KEY:
    raise EnvironmentError("DEEPSEEK_API_KEY not set in .env")
