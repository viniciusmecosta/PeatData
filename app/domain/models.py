from pydantic import BaseModel

class TemperatureHumidityModel(BaseModel):
    temperature: float
    humidity: float
    timestamp: str

class DistanceModel(BaseModel):
    distance: float
    timestamp: str
