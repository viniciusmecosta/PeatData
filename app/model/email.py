from pydantic import BaseModel
from uuid import UUID

class Email(BaseModel):
    id: UUID
    name: str
    email: str