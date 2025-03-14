from pydantic import BaseModel

class TemperatureResponse(BaseModel):
    count: int
    data: str
    temp: float
    humi: float