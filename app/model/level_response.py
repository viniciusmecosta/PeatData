from pydantic import BaseModel


class LevelResponse(BaseModel):
    date: str
    level: float
