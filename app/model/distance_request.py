from pydantic import BaseModel

class DistanceRequest(BaseModel):
    distance: float