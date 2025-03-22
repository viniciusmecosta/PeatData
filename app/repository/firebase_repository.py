import requests


class FirebaseRepository:
    def __init__(self, api_key, firestore_url):
        self.api_key = api_key
        self.firestore_url = firestore_url

    def _build_url(self, collection, doc_name=""):
        return f"{self.firestore_url}/{collection}/{doc_name}?key={self.api_key}".rstrip("/")

    def send_data(self, collection, data):
        requests.post(self._build_url(collection), json=data)

    def get_data(self, collection):
        response = requests.get(self._build_url(collection))
        if response.status_code != 200:
            return []

        data = response.json()
        return [
            {
                "timestamp": doc["fields"].get("timestamp", {}).get("stringValue", "default_value"),
                "temperature": doc["fields"].get("temperature", {}).get("doubleValue"),
                "humidity": doc["fields"].get("humidity", {}).get("doubleValue"),
                "level": doc["fields"].get("level", {}).get("doubleValue"),
                "name": doc["fields"].get("name", {}).get("stringValue"),
                "number": doc["fields"].get("number", {}).get("integerValue"),
                "email": doc["fields"].get("email", {}).get("stringValue"),
                "comedouro": doc["fields"].get("comedouro", {}).get("integerValue"),
            }
            for doc in data.get("documents", [])
        ]

    def delete_all_documents(self, collection):
        response = requests.get(self._build_url(collection))
        if response.status_code != 200:
            return

        for doc in response.json().get("documents", []):
            requests.delete(self._build_url(collection, doc["name"].split("/")[-1]))
