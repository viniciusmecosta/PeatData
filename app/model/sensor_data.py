from pydantic import BaseModel
from datetime import datetime

class SensorData(BaseModel):
    id: int
    temperature: float
    humidity: float
    date: datetime