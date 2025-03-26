# app/repository/phone_repository.py
from sqlalchemy.orm import Session
from app.model.db_models.phone import Phone
from fastapi import HTTPException
from uuid import UUID

def get_phone(db: Session, phone_id: UUID):
    return db.query(Phone).filter(Phone.id == phone_id).first()

def create_phone(db: Session, phone: Phone):
    db_phone = Phone(**phone.dict())
    db.add(db_phone)
    db.commit()
    db.refresh(db_phone)
    return db_phone


def get_all_phones(db: Session):
    return db.query(Phone).all()