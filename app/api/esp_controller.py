from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.model.sensor_data_request import SensorDataRequest
from app.model.level_request import LevelRequest
from app.service.level_service import LevelService
from app.service.sensor_service import SensorService
from app.core.database import get_db

router = APIRouter(prefix="/esp")

def get_sensor_service(db: Session = Depends(get_db)):
    return SensorService(db)

def get_level_service(db: Session = Depends(get_db)):
    return LevelService(db)

@router.post("/temperature-humidity", tags=["ESP"])
async def post_temperature_humidity(
    data: SensorDataRequest,
    sensor_service: SensorService = Depends(get_sensor_service) # Injeta o serviço
):
    """
    Submit temperature and humidity data.
    """
    sensor_service.handle_sensor_data(data.temperature, data.humidity)
    return {"message": "Temperature and humidity data received successfully"}

@router.post("/level", tags=["ESP"])
async def post_distance(
    data: LevelRequest,
    level_service: LevelService = Depends(get_level_service) # Injeta o serviço
):
    """
    Submit level data.
    """
    level_service.handle_level(data.level)
    return {"message": "Level data received successfully"}