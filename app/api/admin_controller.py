from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.email_service import EmailService
from app.service.level_service import LevelService
from app.service.phone_service import PhoneService
from app.service.sensor_service import SensorService

router = APIRouter(prefix="/admin")

def get_email_service(db: Session = Depends(get_db)):
    return EmailService(db)

def get_phone_service(db: Session = Depends(get_db)):
    return PhoneService(db)

def get_sensor_service(db: Session = Depends(get_db)):
    return SensorService(db)

def get_level_service(db: Session = Depends(get_db)):
    return LevelService(db)

@router.post("/generate-sensor-data", tags=["ADMIN"])
async def generate_sensor_data(sensor_service: SensorService = Depends(get_sensor_service)): # Correção
    sensor_service.generate_sensor_data()
    return {"message": "Sensor data generated successfully!"}

@router.delete("/sensor-data", tags=["ADMIN"])
async def delete_sensor_data(sensor_service: SensorService = Depends(get_sensor_service)): # Correção
    sensor_service.delete_all_sensor_data()
    return {"message": "All sensor data deleted successfully"}

@router.post("/generate-level-data", tags=["ADMIN"])
async def generate_level_data(level_service: LevelService = Depends(get_level_service)): # Correção
    level_service.generate_level_data()
    return {"message": "Distance data generated successfully!"}

@router.delete("/level", tags=["ADMIN"])
async def delete_sensor_distance(level_service: LevelService = Depends(get_level_service)): # Correção
    level_service.delete_all_level_data()
    return {"message": "All sensor distance data deleted successfully"}

@router.post("/generate-email/{n}", tags=["ADMIN"])
async def generate_email_data(n: int, email_service: EmailService = Depends(get_email_service)): # Correção
    email_service.generate_email_data(n)
    return {"message": "Email data generated successfully!"}

@router.delete("/email", tags=["ADMIN"])
async def delete_email(email_service: EmailService = Depends(get_email_service)): # Correção
    email_service.delete_all_email_data()
    return {"message": "All emails deleted successfully"}

@router.post("/generate-phone/{n}", tags=["ADMIN"])
async def generate_phone_data(n: int, phone_service: PhoneService = Depends(get_phone_service)): # Correção
    phone_service.generate_phone_data(n)
    return {"message": "Phone data generated successfully!"}

@router.delete("/phone", tags=["ADMIN"])
async def delete_phone(phone_service: PhoneService = Depends(get_phone_service)): # Correção
    phone_service.delete_all_phone_data()
    return {"message": "All phones deleted successfully"}