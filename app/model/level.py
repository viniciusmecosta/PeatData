from pydantic import BaseModel


class Level(BaseModel):
    count: int
    date: str
    level: float
