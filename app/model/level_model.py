from pydantic import BaseModel

class LevelResponse(BaseModel):
    count: int
    date: str
    level: float
