from app.repository.firebase_repository import FirebaseRepository
from app.core.settings import settings
from app.core.constants import COMEDOURO_ID
import pytz


class PhoneService:
    def __init__(self):
        self.repository = FirebaseRepository(
            api_key=settings.FIREBASE_API_KEY, firestore_url=settings.FIREBASE_URL
        )
        self.fortaleza_tz = pytz.timezone("America/Fortaleza")

    def add_phone(self, name: str, number: str):
        data = {
            "fields": {
                "name": {"stringValue": name},
                "number": {"integerValue": number},
                "comedouro": {"integerValue": COMEDOURO_ID},
            }
        }
        self.repository.send_data("phone", data)

    def get_all_phones(self):
        records = self.repository.get_data("phone")
        return [
            {
                "name": record["name"],
                "number": record["number"],
                "comedouro": record["comedouro"],
            }
            for record in records
        ]
