# app/service/email_service.py
from sqlalchemy.orm import Session
from app.repository import email_repository
from app.model.email import Email
from typing import List
from uuid import UUID, uuid4

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