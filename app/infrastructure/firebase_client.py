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
                    "timestamp": doc["fields"]["timestamp"]["stringValue"],
                    "temperature": doc["fields"].get("temperature", {}).get("doubleValue"),
                    "humidity": doc["fields"].get("humidity", {}).get("doubleValue"),
                    "level": doc["fields"].get("level", {}).get("integerValue")
                }
                for doc in data.get("documents", [])
            ]
            return records
        else:
            return []
        
    def add_phone(self, name: str, number: str):
        data = {
            "fields": {
                "name": {"stringValue": name},
                "number": {"stringValue": number},
                "comedouro": {"integerValue": COMEDOURO_ID}
            }
        }
        self.send_data("phone", data)

    def get_all_phones(self):
        url = f"{self.firestore_url}/phone?key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            phones = [
                {
                    "name": doc["fields"]["name"]["stringValue"],
                    "number": doc["fields"]["number"]["stringValue"],
                    "comedouro": doc["fields"]["comedouro"]["integerValue"]
                }
                for doc in data.get("documents", [])
            ]
            return phones
        else:
            return []
    
    def add_email(self, name: str, email: str):
        data = {
            "fields": {
                "name": {"stringValue": name},
                "email": {"stringValue": email},
                "comedouro": {"integerValue": COMEDOURO_ID}
            }
        }
        self.send_data("email", data)

    def get_all_emails(self):
        url = f"{self.firestore_url}/email?key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            emails = [
                {
                    "name": doc["fields"]["name"]["stringValue"],
                    "email": doc["fields"]["email"]["stringValue"],
                    "comedouro": doc["fields"]["comedouro"]["integerValue"]
                }
                for doc in data.get("documents", [])
            ]
            return emails
        else:
            return []