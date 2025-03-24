from pydantic import BaseModel


class SensorDataAvg(BaseModel):
    date: str
    temp: float
    humi: float