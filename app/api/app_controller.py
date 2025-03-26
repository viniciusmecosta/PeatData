from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.model.level_response import LevelResponse
from app.model.sensor_data_response import SensorDataResponse
from app.service.level_service import LevelService
from app.service.sensor_data_service import SensorDataService
from app.core.database import get_db

router = APIRouter()


def get_services(db: Session = Depends(get_db)):
    return {
        "sensor_data_service": SensorDataService(db),
        "level_service": LevelService(db),
    }


@router.get("/sensor_data/avg/{n}", tags=["APP"])
async def get_last_avg_sensor_data(n: int, services=Depends(get_services)):
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
    return services["sensor_data_service"].get_sensor_data_last_n_avg(n)


@router.get(
    "/sensor_data/last/{n}", response_model=List[SensorDataResponse], tags=["APP"]
)
async def get_last_n_sensor_data(n: int, services=Depends(get_services)):
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
    return services["sensor_data_service"].get_last_n_sensor_data_records(n)


@router.get(
    "/sensor_data/days/{days}", response_model=List[SensorDataResponse], tags=["APP"]
)
async def get_sensor_data_days(days: int, services=Depends(get_services)):
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
    return services["sensor_data_service"].get_sensor_data_by_days(days)


@router.get(
    "/sensor_data/date/{date}", response_model=List[SensorDataResponse], tags=["APP"]
)
async def get_sensor_data_date(date: str, services=Depends(get_services)):
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
    return services["sensor_data_service"].get_sensor_data_by_date(date)


@router.get("/level/avg/{n}", tags=["APP"])
async def get_last_avg_level(n: int, services=Depends(get_services)):
    """
    Get the average level for the past N days.

    **Request**:
    - `n`: Number of days for average calculation.

    **Example response**:
    ```json
    [
      {
        "date": "18/03",
        "level": 5.0
      },
      {
        "date": "17/03",
        "level": 4.8
      }
    ]
    ```
    """
    return services["level_service"].get_last_n_avg_level(n)


@router.get("/level/last/{n}", response_model=List[LevelResponse], tags=["APP"])
async def get_last_n_level_data(n: int, services=Depends(get_services)):
    """
    Get the last N level records, ordered by date.

    **Request**:
    - `n`: Number of latest level records.

    **Example response**:
    ```json
    [
      {
        "date": "2025-03-11T10:20:30Z",
        "level": 5.0
      },
      {
        "date": "2025-03-10T10:20:30Z",
        "level": 4.9
      }
    ]
    ```
    """
    return services["level_service"].get_last_n_level_records(n)


@router.get("/level/days/{days}", response_model=List[LevelResponse], tags=["APP"])
async def get_level_days(days: int, services=Depends(get_services)):
    """
    Get level data for the past X days.

    **Request**:
    - `days`: Number of days to look back.

    **Example response**:
    ```json
    [
      {
        "date": "2025-03-11T10:20:30Z",
        "level": 5.0
      },
      {
        "date": "2025-03-10T10:20:30Z",
        "level": 4.9
      }
    ]
    ```
    """
    return services["level_service"].get_level_by_days(days)


@router.get("/level/date/{date}", response_model=List[LevelResponse], tags=["APP"])
async def get_level_date(date: str, services=Depends(get_services)):
    """
    Get level data for a specific date.

    **Request**:
    - `date`: Date in `DDMMYYYY` format.

    **Example response**:
    ```json
    [
      {
        "date": "10:20",
        "level": 5.0
      }
    ]
    ```
    """
    return services["level_service"].get_level_by_date(date)
