# app/service/email_service.py
import uuid

from sqlalchemy.orm import Session
from app.repository import email_repository
from app.model.email import Email
from app.model.db_models.email import Email as EmailDB
from typing import List
from uuid import UUID, uuid4
from app.core.utils import generate_random_email,generate_random_name


class EmailService:
    def __init__(self, db: Session):
        self.db = db

    def add_email(self, name: str, email: str):
        email_data = Email(id=uuid4(), name=name, email=email)
        return email_repository.create_email(self.db, email_data)

    def get_email(self, email_id: UUID):
        return email_repository.get_email(self.db, email_id)

    def update_email(self, email_id: UUID, email: Email):
        return email_repository.update_email(self.db, email_id, email)

    def delete_email(self, email_id: UUID):
        return email_repository.delete_email(self.db, email_id)

    def get_all_emails(self) -> List[Email]:
        return email_repository.get_all_emails(self.db)

    def generate_email_data(self, n: int):
        for _ in range(n):
            name = generate_random_name()
            email_address = generate_random_email(name)
            email = EmailDB(id=uuid.uuid4(), name=name, email=email_address)
            self.db.add(email)
        self.db.commit()

    def delete_all_email_data(self):
        self.db.query(EmailDB).delete()
        self.db.commit()