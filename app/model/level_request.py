from pydantic import BaseModel

class LevelRequest(BaseModel):
    level: float