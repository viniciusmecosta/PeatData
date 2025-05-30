from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.auth.token_authenticator import TokenAuthenticator
from app.core.database import get_db
from app.service.email_service import EmailService
from app.service.level_service import LevelService
from app.service.phone_service import PhoneService
from app.service.sensor_data_service import SensorDataService

router = APIRouter()
auth = TokenAuthenticator()


def get_services(db: Session = Depends(get_db)):
    return {
        "email_service": EmailService(db),
        "phone_service": PhoneService(db),
        "sensor_data_service": SensorDataService(db),
        "level_service": LevelService(db),
    }


@router.post(
    "/generate-temp-humi-data",
    summary="Generate mock temperature and humidity data",
    description="Generates mock temperature and humidity data for the past 31 days, with two entries per day.",
)
async def generate_sensor_data(
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    services["sensor_data_service"].generate_sensor_data()
    return {"message": "Sensor data generated successfully!"}


@router.delete(
    "/temp-humi",
    summary="Delete all sensor data",
    description="Deletes all records from the `sensor_data` table in the database.",
)
async def delete_sensor_data(
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):

    services["sensor_data_service"].delete_all_sensor_data()
    return {"message": "All sensor data deleted successfully!"}


@router.post(
    "/generate-level-data",
    summary="Generate mock level/distance data",
    description="Generates mock level/distance data for the past 31 days, with two entries per day.",
)
async def generate_level_data(
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):

    services["level_service"].generate_level_data()
    return {"message": "Level/distance data generated successfully!"}


@router.delete(
    "/level",
    summary="Delete all level data",
    description="Deletes all records from the `level` table in the database.",
)
async def delete_level_data(
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):

    services["level_service"].delete_all_level_data()
    return {"message": "All level/distance data deleted successfully!"}


@router.post(
    "/generate-email/{n}",
    summary="Generate mock email data",
    description="Generates `n` mock email records and stores them in the database.",
)
async def generate_email_data(
    n: int,
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):

    services["email_service"].generate_email_data(n)
    return {"message": "Email data generated successfully!"}


@router.delete(
    "/email",
    summary="Delete all email records",
    description="Deletes all records from the `email` table in the database.",
)
async def delete_email_data(
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):

    services["email_service"].delete_all_email_data()
    return {"message": "All emails deleted successfully!"}


@router.post(
    "/generate-phone/{n}",
    summary="Generate mock phone data",
    description="Generates `n` mock phone records and stores them in the database.",
)
async def generate_phone_data(
    n: int,
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    services["phone_service"].generate_phone_data(n)
    return {"message": "Phone data generated successfully!"}


@router.delete(
    "/phone",
    summary="Delete all phone records",
    description="Deletes all records from the `phone` table in the database.",
)
async def delete_phone_data(
    services=Depends(get_services),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    services["phone_service"].delete_all_phone_data()
    return {"message": "All phone data deleted successfully!"}
