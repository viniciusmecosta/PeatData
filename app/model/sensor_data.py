from pydantic import BaseModel


class SensorData(BaseModel):
    count: int
    date: str
    temp: float
    humi: float
