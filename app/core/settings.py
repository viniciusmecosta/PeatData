from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "default_api_key") 
    FIREBASE_URL = os.getenv("FIREBASE_URL", "default_firestore_url")

settings = Settings()
