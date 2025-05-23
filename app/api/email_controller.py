from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from app.auth.token_authenticator import TokenAuthenticator
from app.core.database import get_db
from app.model.email import Email
from app.model.email_request import EmailRequest
from app.service.email_service import EmailService

router = APIRouter()
auth = TokenAuthenticator()


def get_email_service(db: Session = Depends(get_db)) -> EmailService:
    return EmailService(db)


@router.post("/email")
def post_email(
    request: EmailRequest,
    services=Depends(get_email_service),
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
    result = services.add_email(request.name, request.email)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=result["error"]
        )
    return {
        "message": "Email added successfully",
        "name": f"{request.name}",
        "email": f"{request.email}",
    }


@router.get("/email", response_model=List[Email])
def get_emails(
    services=Depends(get_email_service),
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
    return services.get_all_emails()
