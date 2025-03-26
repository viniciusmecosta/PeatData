from pydantic import BaseModel
from datetime import datetime


class LevelResponse(BaseModel):
    date: str
    level: float
