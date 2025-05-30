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


@router.post(
    "/email",
    summary="Adds an email address",
    description="This endpoint allows you to add an email address to the database. The email must be valid and unique.",
)
def post_email(
    request: EmailRequest,
    services=Depends(get_email_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):

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


@router.get(
    "/email",
    response_model=List[Email],
    summary="Retrieves all registered email addresses",
    description="This endpoint retrieves all email addresses registered in the system.",
)
def get_emails(
    services=Depends(get_email_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    return services.get_all_emails()
