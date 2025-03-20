import random
from datetime import datetime, timedelta
import pytz

from app.core.constants import COMEDOURO_ID
from app.core.utils import (
    calculate_comedouro_level,
    generate_random_phone,
    generate_random_name,
    generate_random_email,
)
from app.repository.firebase_repository import FirebaseRepository
from app.core.settings import settings


class AdminService:
    def __init__(self):
        self.repository = FirebaseRepository(
            api_key=settings.FIREBASE_API_KEY, firestore_url=settings.FIREBASE_URL
        )
        self.fortaleza_tz = pytz.timezone("America/Fortaleza")

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

    def delete_all(self, document):
        return self.repository.delete_all_documents(document)

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

    def generate_email_data(self, n):
        for i in range(n):

            name = generate_random_name()
            email = generate_random_email(name)

            data = {
                "fields": {
                    "name": {"stringValue": name},
                    "email": {"stringValue": email},
                    "comedouro": {"integerValue": COMEDOURO_ID},
                }
            }

            self.repository.send_data("email", data)

    def generate_phone_data(self, n):
        for i in range(n):

            name = generate_random_name()
            number = generate_random_phone()

            data = {
                "fields": {
                    "name": {"stringValue": name},
                    "number": {"integerValue": number},
                    "comedouro": {"integerValue": COMEDOURO_ID},
                }
            }

            self.repository.send_data("phone", data)
