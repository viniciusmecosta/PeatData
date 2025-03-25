from pydantic import BaseModel


class SensorDataResponse(BaseModel):
    date: str
    temp: float
    humi: float