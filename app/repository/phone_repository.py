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

def update_phone(db: Session, phone_id: UUID, phone: Phone):
    db_phone = db.query(Phone).filter(Phone.id == phone_id).first()
    if not db_phone:
        raise HTTPException(status_code=404, detail="Phone não encontrado")
    for key, value in phone.dict().items():
        setattr(db_phone, key, value)
    db.commit()
    db.refresh(db_phone)
    return db_phone

def delete_phone(db: Session, phone_id: UUID):
    db_phone = db.query(Phone).filter(Phone.id == phone_id).first()
    if not db_phone:
        raise HTTPException(status_code=404, detail="Phone não encontrado")
    db.delete(db_phone)
    db.commit()
    return db_phone

def get_all_phones(db: Session):
    return db.query(Phone).all()