# app/api/notify_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.email import Email
from app.model.email_request import EmailRequest
from app.model.phone_request import PhoneRequest
from app.service.email_service import EmailService
from app.service.phone_service import PhoneService
from app.model.phone import Phone
from typing import List

router = APIRouter(prefix="/notify")

def get_email_service(db: Session = Depends(get_db)):
    return EmailService(db)

def get_phone_service(db: Session = Depends(get_db)):
    return PhoneService(db)

@router.post("/email", tags=["NOTIFY"])
def post_email(request: EmailRequest, email_service: EmailService = Depends(get_email_service)):
    """
    Adds an email address to the system.
    """
    email_service.add_email(request.name, request.email)
    return {"message": "Email added successfully"}

@router.get("/email", tags=["NOTIFY"], response_model=List[Email])
def get_emails(email_service: EmailService = Depends(get_email_service)):
    """
    Retrieves all registered email addresses.
    """
    return email_service.get_all_emails()

@router.post("/phone", tags=["NOTIFY"])
def post_phone(request: PhoneRequest, phone_service: PhoneService = Depends(get_phone_service)):
    """
    Adds a phone number to the system.
    """
    if len(request.number) != 11 or not request.number.isdigit():
        raise HTTPException(status_code=400, detail="Number must have 11 digits")

    phone_service.add_phone(request.name, request.number)
    return {"message": "Phone number added successfully"}

@router.get("/phone", tags=["NOTIFY"], response_model=List[Phone])
def get_phones(phone_service: PhoneService = Depends(get_phone_service)):
    """
    Retrieves all registered phone numbers.
    """
    return phone_service.get_all_phones()