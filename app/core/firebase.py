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
