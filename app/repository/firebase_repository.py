import requests


class FirebaseRepository:
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
                    "timestamp": doc["fields"]
                    .get("timestamp", {})
                    .get("stringValue", "default_value"),
                    "temperature": doc["fields"]
                    .get("temperature", {})
                    .get("doubleValue"),
                    "humidity": doc["fields"].get("humidity", {}).get("doubleValue"),
                    "level": doc["fields"].get("level", {}).get("doubleValue"),
                    "name": doc["fields"].get("name", {}).get("stringValue"),
                    "number": doc["fields"].get("number", {}).get("integerValue"),
                    "email": doc["fields"].get("email", {}).get("stringValue"),
                    "comedouro": doc["fields"].get("comedouro", {}).get("integerValue"),
                }
                for doc in data.get("documents", [])
            ]
            return records
        else:
            return []

    def delete_all_documents(self, collection):
        url = f"{self.firestore_url}/{collection}?key={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for doc in data.get("documents", []):
                doc_name = doc["name"].split("/")[-1]
                delete_url = (
                    f"{self.firestore_url}/{collection}/{doc_name}?key={self.api_key}"
                )
                requests.delete(delete_url)
