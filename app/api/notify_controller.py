from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from app.auth.token_authenticator import TokenAuthenticator
from app.core.database import get_db
from app.model.email import Email
from app.model.email_request import EmailRequest
from app.model.phone_request import PhoneRequest
from app.service.email_service import EmailService
from app.service.phone_service import PhoneService
from app.model.phone import Phone

router = APIRouter()
auth = TokenAuthenticator()


def get_services(db: Session = Depends(get_db)):
    return {
        "email_service": EmailService(db),
        "phone_service": PhoneService(db),
    }


@router.post("/email", tags=["NOTIFY"])
def post_email(
    request: EmailRequest,
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Adds an email address in the database.

    **Request**:
    - `name`: Name associated with the email address.
    - `email`: Email address to be added.

    **Example request**:
    ```json
    {
      "name": "Maria Oliveira",
      "email": "maria.oliveira@example.com",
    }
    ```

    **Example response (Success)**:
    ```json
    {
      "message": "Email added successfully",
      "name": "Maria Oliveira",
      "email": "maria.oliveira@example.com"
    }
    ```

    **Example response (Error - Email already exists)**:
    ```json
    {
      "detail": "Email 'maria.oliveira@example.com' already exists."
    }
    ```
    """
    result = services["email_service"].add_email(request.name, request.email)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=result["error"]
        )
    return {
        "message": "Email added successfully",
        "name": f"{request.name}",
        "email": f"{request.email}",
    }


@router.get("/email", tags=["NOTIFY"], response_model=List[Email])
def get_emails(
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Retrieves all registered email addresses.

    **Example response**:
    ```json
    [
      {
        "name": "Maria Oliveira",
        "email": "maria.oliveira@example.com",
      }
    ]
    ```
    """
    return services["email_service"].get_all_emails()


@router.post("/phone", tags=["NOTIFY"])
def post_phone(
    request: PhoneRequest,
    services=Depends(get_services),
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

    services["phone_service"].add_phone(request.name, request.number)
    return {
        "message": "Phone number added successfully",
        "name": f"{request.name}",
        "number": f"{request.number}",
    }


@router.get("/phone", tags=["NOTIFY"], response_model=List[Phone])
def get_phones(
    services=Depends(get_services),
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
    return services["phone_service"].get_all_phones()
