from pydantic import BaseModel

class SensorDataRequest(BaseModel):
    temperature: float
    humidity: float
