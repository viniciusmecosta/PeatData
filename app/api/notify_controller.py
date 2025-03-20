from fastapi import APIRouter

from app.service.email_service import EmailService
from app.service.phone_service import PhoneService

router = APIRouter()
phone_service = PhoneService()
email_service = EmailService()


@router.post("/phone", tags=["NOTIFY"])
async def post_phone(name: str, number: str):
    """
    Adds a phone number to the system.

    - **name**: Name associated with the phone number.
    - **number**: Phone number (must be 11 digits).

    **Example request:**
    ```json
    {
      "name": "João Silva",
      "number": "11987654321"
    }
    ```

    **Response:**
    - Success message when phone number is added.

    **Example response:**
    ```json
    {
      "message": "Phone number added successfully"
    }
    ```
    """
    if len(number) != 11 or not number.isdigit():
        return {"error": "Number must have 11 digits"}

    phone_service.add_phone(name, number)
    return {"message": "Phone number added successfully"}


@router.get("/phone", tags=["NOTIFY"])
async def get_phones():
    """
    Retrieves all registered phone numbers.

    Returns a list of phone numbers with their associated names.

    **Example response:**
    ```json
    [
      {
        "name": "João Silva",
        "number": "11987654321"
      }
    ]
    ```
    """
    return phone_service.get_all_phones()


@router.post("/email", tags=["NOTIFY"])
async def post_email(name: str, email: str):
    """
    Adds an email address to the system.

    - **name**: Name associated with the email address.
    - **email**: Email address to be added.

    **Example request:**
    ```json
    {
      "name": "Maria Oliveira",
      "email": "maria.oliveira@example.com"
    }
    ```

    **Response:**
    - Success message when email address is added.

    **Example response:**
    ```json
    {
      "message": "Email added successfully"
    }
    ```
    """
    email_service.add_email(name, email)
    return {"message": "Email added successfully"}


@router.get("/email", tags=["NOTIFY"])
async def get_emails():
    """
    Retrieves all registered email addresses.

    Returns a list of email addresses with their associated names.

    **Example response:**
    ```json
    [
      {
        "name": "Maria Oliveira",
        "email": "maria.oliveira@example.com"
      }
    ]
    ```
    """
    return email_service.get_all_emails()
