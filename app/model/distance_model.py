from pydantic import BaseModel

class DistanceResponse(BaseModel):
    count: int
    data: str
    level: int