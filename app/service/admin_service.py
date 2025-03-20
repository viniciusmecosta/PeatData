import random
from datetime import datetime, timedelta
import pytz

from app.core.utils import calculate_comedouro_level
from app.repository.firebase_repository import FirebaseRepository
from app.core.settings import settings


class AdminService:
    def __init__(self):
        self.repository = FirebaseRepository(
            api_key=settings.FIREBASE_API_KEY, firestore_url=settings.FIREBASE_URL
        )
        self.fortaleza_tz = pytz.timezone("America/Fortaleza")

    def delete_all_sensor_distance(self):
        return self.repository.delete_all_documents("sensor_distance")

    def generate_distance_data(self):
        end_date = datetime.now(self.fortaleza_tz)
        for i in range(31):
            date = end_date - timedelta(days=i)
            timestamp = date.strftime("%Y-%m-%dT%H:%M:%SZ")

            level = round(random.uniform(2, 25), 1)
            level = calculate_comedouro_level(level)

            data = {
                "fields": {
                    "timestamp": {"stringValue": timestamp},
                    "level": {"doubleValue": level},
                }
            }

            self.repository.send_data("sensor_distance", data)

    def delete_all_sensor_data(self):
        return self.repository.delete_all_documents("sensor_data")

    def generate_sensor_data(self):
        end_date = datetime.now(self.fortaleza_tz)
        for i in range(31):
            date = end_date - timedelta(days=i)
            timestamp = date.strftime("%Y-%m-%dT%H:%M:%SZ")

            temperature = round(random.uniform(20, 38), 1)
            humidity = round(random.uniform(30, 85), 1)

            data = {
                "fields": {
                    "timestamp": {"stringValue": timestamp},
                    "temperature": {"doubleValue": temperature},
                    "humidity": {"doubleValue": humidity},
                }
            }

            self.repository.send_data("sensor_data", data)
