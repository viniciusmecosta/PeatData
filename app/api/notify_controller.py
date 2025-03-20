from fastapi import APIRouter
from typing import List

from app.model.email import Email
from app.model.email_request import EmailRequest
from app.model.phone import Phone
from app.model.phone_request import PhoneRequest
from app.service.email_service import EmailService
from app.service.phone_service import PhoneService

router = APIRouter(prefix="/notify")
phone_service = PhoneService()
email_service = EmailService()


@router.post("/phone", tags=["NOTIFY"])
async def post_phone(request: PhoneRequest):
    """
    Adds a phone number to the system.

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
      "message": "Phone number added successfully"
    }
    ```
    """
    if len(request.number) != 11 or not request.number.isdigit():
        return {"error": "Number must have 11 digits"}

    phone_service.add_phone(request.name, request.number)
    return "Phone number added successfully"


@router.get("/phone", tags=["NOTIFY"], response_model=List[Phone])
async def get_phones():
    """
    Retrieves all registered phone numbers.

    **Example response**:
    ```json
    [
      {
        "name": "João Silva",
        "number": "11987654321",
        "comedouro": 1,
      }
    ]
    ```
    """
    return phone_service.get_all_phones()


@router.post("/email", tags=["NOTIFY"])
async def post_email(request: EmailRequest):
    """
    Adds an email address to the system.

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

    **Example response**:
    ```json
    {
      "message": "Email added successfully"
    }
    ```
    """
    email_service.add_email(request.name, request.email)
    return "Email added successfully"


@router.get("/email", tags=["NOTIFY"], response_model=List[Email])
async def get_emails():
    """
    Retrieves all registered email addresses.

    **Example response**:
    ```json
    [
      {
        "name": "Maria Oliveira",
        "email": "maria.oliveira@example.com",
        "comedouro": 1
      }
    ]
    ```
    """
    return email_service.get_all_emails()
