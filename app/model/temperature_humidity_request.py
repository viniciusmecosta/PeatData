from pydantic import BaseModel

class TemperatureHumidityRequest(BaseModel):
    temperature: float
    humidity: float
