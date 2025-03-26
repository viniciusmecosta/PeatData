from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.email_service import EmailService
from app.service.level_service import LevelService
from app.service.phone_service import PhoneService
from app.service.sensor_data_service import SensorDataService

router = APIRouter(prefix="/admin")


def get_services(db: Session = Depends(get_db)):
    return {
        "email_service": EmailService(db),
        "phone_service": PhoneService(db),
        "sensor_data_service": SensorDataService(db),
        "level_service": LevelService(db),
    }


@router.post("/generate-sensor-data", tags=["ADMIN"])
async def generate_sensor_data(services=Depends(get_services)):
    """
    Generates mock temperature and humidity data for the past 31 days,
    with two entries per day.
    """
    services["sensor_data_service"].generate_sensor_data()
    return {"message": "Sensor data generated successfully!"}


@router.delete("/sensor-data", tags=["ADMIN"])
async def delete_sensor_data(services=Depends(get_services)):
    """
    Deletes all records from the `sensor_data` table in the database.
    """
    services["sensor_data_service"].delete_all_sensor_data()
    return {"message": "All sensor data deleted successfully!"}


@router.post("/generate-level-data", tags=["ADMIN"])
async def generate_level_data(services=Depends(get_services)):
    """
    Generates mock level/distance data for the past 31 days,
    with two entries per day.
    """
    services["level_service"].generate_level_data()
    return {"message": "Level/distance data generated successfully!"}


@router.delete("/level", tags=["ADMIN"])
async def delete_level_data(services=Depends(get_services)):
    """
    Deletes all records from the `level_data` table in the database.
    """
    services["level_service"].delete_all_level_data()
    return {"message": "All level/distance data deleted successfully!"}


@router.post("/generate-email/{n}", tags=["ADMIN"])
async def generate_email_data(n: int, services=Depends(get_services)):
    """
    Generates `n` mock email records and stores them in the database.
    """
    services["email_service"].generate_email_data(n)
    return {"message": "Email data generated successfully!"}


@router.delete("/email", tags=["ADMIN"])
async def delete_email_data(services=Depends(get_services)):
    """
    Deletes all records from the `email` table in the database.
    """
    services["email_service"].delete_all_email_data()
    return {"message": "All emails deleted successfully!"}


@router.post("/generate-phone/{n}", tags=["ADMIN"])
async def generate_phone_data(n: int, services=Depends(get_services)):
    """
    Generates `n` mock phone records and stores them in the database.
    """
    services["phone_service"].generate_phone_data(n)
    return {"message": "Phone data generated successfully!"}


@router.delete("/phone", tags=["ADMIN"])
async def delete_phone_data(services=Depends(get_services)):
    """
    Deletes all records from the `phone` table in the database.
    """
    services["phone_service"].delete_all_phone_data()
    return {"message": "All phone data deleted successfully!"}
