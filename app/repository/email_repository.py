from sqlalchemy.orm import Session
from app.model.email import Email
from app.model.db_models.email import Email as EmailDB
from fastapi import HTTPException
from uuid import UUID


def get_email(db: Session, email_id: UUID):
    return db.query(EmailDB).filter(EmailDB.id == email_id).first()


def create_email(db: Session, email: Email):
    db_email = EmailDB(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return email


def get_all_emails(db: Session):
    return db.query(EmailDB).all()
