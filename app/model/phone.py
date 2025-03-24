from pydantic import BaseModel
from uuid import UUID

class Phone(BaseModel):
    id: UUID
    number: str
    name: str