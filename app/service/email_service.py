from app.repository.firebase_repository import FirebaseRepository
from app.core.settings import settings

from app.core.constants import COMEDOURO_ID
import pytz


class EmailService:
    def __init__(self):
        self.repository = FirebaseRepository(
            api_key=settings.FIREBASE_API_KEY, firestore_url=settings.FIREBASE_URL
        )
        self.fortaleza_tz = pytz.timezone("America/Fortaleza")

    def add_email(self, name: str, email: str):
        data = {
            "fields": {
                "name": {"stringValue": name},
                "email": {"stringValue": email},
                "comedouro": {"integerValue": COMEDOURO_ID},
            }
        }
        self.repository.send_data("email", data)

    def get_all_emails(self):
        records = self.repository.get_data("email")
        return [
            {
                "name": record["name"],
                "email": record["email"],
                "comedouro": record["comedouro"],
            }
            for record in records
        ]
