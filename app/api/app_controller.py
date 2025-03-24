# app/api/app_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.sensor_data import SensorData
from typing import List
from app.model.sensor_data_response import SensorDataAvg
from app.service.sensor_service import SensorService

router = APIRouter(prefix="/app")

def get_sensor_service(db: Session = Depends(get_db)):
    return SensorService(db)

@router.get(
    "/temperature/avg/{n}",
    response_model=List[SensorDataAvg],
    tags=["APP"],
)
async def get_last_avg_temperature(n: int, sensor_service: SensorService = Depends(get_sensor_service)):
    return sensor_service.get_temperature_last_n_avg(n)

@router.get("/temperature/last/{n}", response_model=List[SensorData], tags=["APP"])
async def get_last_n_temperatures(n: int, sensor_service: SensorService = Depends(get_sensor_service)):
    return sensor_service.get_last_n_temperature_records(n)

@router.get("/temperature/{days}", response_model=List[SensorData], tags=["APP"])
async def get_temperature_days(days: int, sensor_service: SensorService = Depends(get_sensor_service)):
    return sensor_service.get_temperature_by_days(days)

@router.get("/temperature/date/{date}", response_model=List[SensorData], tags=["APP"])
async def get_temperature_date(date: str, sensor_service: SensorService = Depends(get_sensor_service)):
    return sensor_service.get_temperature_by_date(date)