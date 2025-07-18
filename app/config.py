from dotenv import load_dotenv
import os

load_dotenv()  # this loads the variables from .env into os.environ

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
