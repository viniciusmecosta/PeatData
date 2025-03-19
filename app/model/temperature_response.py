from pydantic import BaseModel

class TemperatureResponse(BaseModel):
    count: int
    date: str
    temp: float
    humi: float