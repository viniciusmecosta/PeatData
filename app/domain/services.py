from app.infrastructure.firebase_client import FirebaseClient
from app.core.settings import settings
from datetime import datetime
import pytz

fortaleza_tz = pytz.timezone('America/Fortaleza')

firebase_client = FirebaseClient(
    api_key=settings.FIREBASE_API_KEY,
    firestore_url=settings.FIREBASE_URL
)

def handle_temperature_humidity(temperature: float, humidity: float):
    timestamp = datetime.now(fortaleza_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "fields": {
            "timestamp": {"stringValue": timestamp},
            "temperature": {"doubleValue": temperature},
            "humidity": {"doubleValue": humidity}
        }
    }
    firebase_client.send_data("sensor_data", data)

def handle_distance(distance: float):
    timestamp = datetime.now(fortaleza_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "fields": {
            "timestamp": {"stringValue": timestamp},
            "distance": {"doubleValue": distance}
        }
    }
    firebase_client.send_data("sensor_distance", data)

def get_all_records():
    pass
