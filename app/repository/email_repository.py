
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

def update_email(db: Session, email_id: UUID, email: Email):
    db_email = db.query(EmailDB).filter(EmailDB.id == email_id).first()
    if not db_email:
        raise HTTPException(status_code=404, detail="Email não encontrado")
    for key, value in email.dict().items():
        setattr(db_email, key, value)
    db.commit()
    db.refresh(db_email)
    return email

def delete_email(db: Session, email_id: UUID):
    db_email = db.query(EmailDB).filter(EmailDB.id == email_id).first()
    if not db_email:
        raise HTTPException(status_code=404, detail="Email não encontrado")
    db.delete(db_email)
    db.commit()
    return email

def get_all_emails(db: Session):
    return db.query(EmailDB).all()