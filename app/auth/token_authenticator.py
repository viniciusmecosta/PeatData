import os
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


class TokenAuthenticator:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("API_TOKEN")
        if self.TOKEN is None:
            raise ValueError("API_TOKEN environment variable not set")

    def verify_token(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        if credentials.credentials == self.TOKEN:
            return credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token provided",
                headers={"WWW-Authenticate": "Bearer"},
            )
