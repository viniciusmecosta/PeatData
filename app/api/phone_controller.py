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


@router.post("/phone")
def post_phone(
    request: PhoneRequest,
    services=Depends(get_phone_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Adds a phone number in the database.

    **Request**:
    - `name`: Name associated with the phone number.
    - `number`: Phone number (must be 11 digits).

    **Example request**:
    ```json
    {
      "name": "João Silva",
      "number": "11987654321"
    }
    ```

    **Example response**:
    ```json
    {
      "message": "Phone number added successfully",
      "name": "João Silva",
      "number": "11987654321"
    }
    ```
    """
    if len(request.number) != 11 or not request.number.isdigit():
        raise HTTPException(status_code=400, detail="Number must have 11 digits")

    services.add_phone(request.name, request.number)
    return {
        "message": "Phone number added successfully",
        "name": f"{request.name}",
        "number": f"{request.number}",
    }


@router.get("/phone", response_model=List[Phone])
def get_phones(
    services=Depends(get_phone_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Retrieves all registered phone numbers.

    **Example response**:
    ```json
    [
      {
        "name": "João Silva",
        "number": "11987654321",
      }
    ]
    ```
    """
    return services.get_all_phones()
