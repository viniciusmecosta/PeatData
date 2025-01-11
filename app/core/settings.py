import os

class Settings:
    FIREBASE_API_KEY = os.getenv("API_KEY", "default_api_key")
    FIREBASE_URL = os.getenv("FIRESTORE_URL", "default_firestore_url")

settings = Settings()
