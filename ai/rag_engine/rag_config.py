import os
from dotenv import load_dotenv
load_dotenv()

def get_openai_api():
    return os.getenv("OPENAI_API_KEY")