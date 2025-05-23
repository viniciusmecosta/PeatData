from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.auth.token_authenticator import TokenAuthenticator
from app.model.sensor_data_request import SensorDataRequest
from app.model.sensor_data_response import SensorDataResponse
from app.service.sensor_data_service import SensorDataService
from app.core.database import get_db

router = APIRouter()
auth = TokenAuthenticator()


def get_sensor_data_service(db: Session = Depends(get_db)) -> SensorDataService:
    return SensorDataService(db)


@router.post(
    "/temp-humi",
    summary="Submit temperature and humidity data",
    description="This endpoint allows you to submit temperature and humidity data to the database.",
)
async def post_temperature_humidity(
    data: SensorDataRequest,
    services=Depends(get_sensor_data_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Submit temperature and humidity data.

    **Request body**:
    - `temperature`: Temperature value.
    - `humidity`: Humidity value.

    **Example request**:
    ```json
    {
      "temperature": 23.5,
      "humidity": 60.0
    }
    ```

    **Example response**:
    ```json
    {
      "message": "Temperature and humidity data received successfully",
      "temperature": "23.5",
      "humidity": "60.0",
      "date": "2025-04-11 09:46:52.799926"
    }
    ```
    """
    sensorData = services.handle_sensor_data(data.temperature, data.humidity)
    return {
        "message": "Temperature and humidity data received successfully",
        "temperature": f"{sensorData.temp}",
        "humidity": f"{sensorData.humi}",
        "date": f"{sensorData.date}",
    }


@router.get(
    "/temp-humi/avg/{n}",
    summary="Get average temperature and humidity for the past N days",
    description="This endpoint retrieves the average temperature and humidity for the past N days.",
)
async def get_last_avg_sensor_data(
    n: int,
    services=Depends(get_sensor_data_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Get the average temperature and humidity for the past N days.

    **Request**:
    - `n`: Number of days for average calculation.

    **Example response**:
    ```json
    [
      {
        "date": "18/03",
        "temp": 22.5,
        "humi": 60.0
      },
      {
        "date": "17/03",
        "temp": 23.0,
        "humi": 65.0
      }
    ]
    ```
    """
    return services.get_sensor_data_last_n_avg(n)


@router.get(
    "/temp-humi/last/{n}",
    response_model=List[SensorDataResponse],
    summary="Get the last N temperature and humidity records",
    description="This endpoint retrieves the last N temperature and humidity records, ordered by date.",
)
async def get_last_n_sensor_data(
    n: int,
    services=Depends(get_sensor_data_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Get the last N temperature and humididty records, ordered by date.

    **Request**:
    - `n`: Number of latest temperature records.

    **Example response**:
    ```json
    [
      {
        "date": "2025-03-11T10:20:30Z",
        "temp": 23.5,
        "humi": 10.2
      },
      {
        "date": "2025-03-10T10:20:30Z",
        "temp": 23.0,
        "humi": 11.0
      }
    ]
    ```
    """
    return services.get_last_n_sensor_data_records(n)


@router.get(
    "/temp-humi/days/{days}",
    response_model=List[SensorDataResponse],
    summary="Get temperature and humidity data for the past X days",
    description="This endpoint retrieves temperature and humidity data for the past X days, with two entries per day.",
)
async def get_sensor_data_days(
    days: int,
    services=Depends(get_sensor_data_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Get temperature and humidity data for the past X days.

    **Request**:
    - `days`: Number of days to look back.

    **Example response**:
    ```json
    [
      {
        "date": "2025-03-11T10:20:30Z",
        "temp": 23.5,
        "humi": 10.2
      },
      {
        "date": "2025-03-10T10:20:30Z",
        "temp": 23.0,
        "humi": 11.0
      }
    ]
    ```
    """
    return services.get_sensor_data_by_days(days)


@router.get(
    "/temp-humi/date/{date}",
    response_model=List[SensorDataResponse],
    summary="Get temperature and humidity data for a specific date",
    description="This endpoint retrieves temperature and humidity data for a specific date in `DDMMYYYY` format.",
)
async def get_sensor_data_date(
    date: str,
    services=Depends(get_sensor_data_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Get temperature data for a specific date.

    **Request**:
    - `date`: Date in `DDMMYYYY` format.

    **Example response**:
    ```json
    [
      {
        "date": "10:20",
        "temp": 23.5,
        "humi": 10.2
      }
    ]
    ```
    """
    return services.get_sensor_data_by_date(date)
