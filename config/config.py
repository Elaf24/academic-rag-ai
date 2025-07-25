from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration settings
CONFIG = {
    "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
    "AZURE_OPENAI_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    "OPENAI_CHAT_API_VERSION": os.getenv("OPENAI_CHAT_API_VERSION"),
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
    "OPENAI_EMBEDDING_API_VERSION": os.getenv("OPENAI_EMBEDDING_API_VERSION"),
    "TESSERACT_PATH": "/opt/homebrew/bin/tesseract"
}

# Set Tesseract path if specified
if CONFIG["TESSERACT_PATH"]:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = CONFIG["TESSERACT_PATH"]