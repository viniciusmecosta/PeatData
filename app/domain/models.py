from pydantic import BaseModel

class TemperatureHumidityModel(BaseModel):
    temperature: float
    humidity: float
    timestamp: str

class DistanceModel(BaseModel):
    distance: float
    timestamp: str

class TemperatureHumidityRequest(BaseModel):
    temperature: float
    humidity: float

class DistanceRequest(BaseModel):
    distance: float

class TemperatureResponse(BaseModel):
    count: int
    data: str
    temp: float
    humi: float

class DistanceResponse(BaseModel):
    count: int
    data: str
    distance: float