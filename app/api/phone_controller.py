from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from app.auth.token_authenticator import TokenAuthenticator
from app.core.database import get_db
from app.model.phone_request import PhoneRequest
from app.service.phone_service import PhoneService
from app.model.phone import Phone

router = APIRouter()
auth = TokenAuthenticator()


def get_phone_service(db: Session = Depends(get_db)) -> PhoneService:
    return PhoneService(db)


@router.post(
    "/phone",
    summary="Adds a phone number",
    description="This endpoint allows you to add a phone number to the database. The phone number must be 11 digits long.",
)
def post_phone(
    request: PhoneRequest,
    services=Depends(get_phone_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
   
    if len(request.number) != 11 or not request.number.isdigit():
        raise HTTPException(status_code=400, detail="Number must have 11 digits")

    services.add_phone(request.name, request.number)
    return {
        "message": "Phone number added successfully",
        "name": f"{request.name}",
        "number": f"{request.number}",
    }


@router.get(
    "/phone",
    response_model=List[Phone],
    summary="Retrieves all registered phone numbers",
    description="This endpoint retrieves all phone numbers registered in the system.",
)
def get_phones(
    services=Depends(get_phone_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    
    return services.get_all_phones()
