import requests
import json

class FirebaseClient:
    def __init__(self, api_key, firestore_url):
        self.api_key = api_key
        self.firestore_url = firestore_url

    def send_data(self, collection, data):
        url = f"{self.firestore_url}/{collection}?key={self.api_key}"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Dados enviados para {collection} com sucesso!")
        else:
            print(f"Erro ao enviar dados para {collection}: {response.text}")

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
                    "distance": doc["fields"].get("distance", {}).get("doubleValue")
                }
                for doc in data.get("documents", [])
            ]
            return records
        else:
            print(f"Erro ao buscar dados de {collection}: {response.text}")
            return []