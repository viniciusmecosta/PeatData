import requests
from app.core.constants import COMEDOURO_ID

class FirebaseClient:
    def __init__(self, api_key, firestore_url):
        self.api_key = api_key
        self.firestore_url = firestore_url

    def send_data(self, collection, data):
        url = f"{self.firestore_url}/{collection}?key={self.api_key}"
        requests.post(url, json=data)

    def get_data(self, collection):
        url = f"{self.firestore_url}/{collection}?key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            records = [
                {
                    "timestamp": doc["fields"].get("timestamp", {}).get("stringValue", "default_value"),

                    "temperature": doc["fields"].get("temperature", {}).get("doubleValue"),
                    "humidity": doc["fields"].get("humidity", {}).get("doubleValue"),
                    "level": doc["fields"].get("level", {}).get("integerValue"),
                    "name": doc["fields"].get("name", {}).get("stringValue"),
                    "number": doc["fields"].get("number", {}).get("stringValue"),
                    "email": doc["fields"].get("email", {}).get("stringValue"),
                    "comedouro": doc["fields"].get("comedouro", {}).get("integerValue")
                }
                for doc in data.get("documents", [])
            ]
            return records
        else:
            return []