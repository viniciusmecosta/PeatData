from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Level(BaseModel):
    id: UUID
    level: float
    date: datetime