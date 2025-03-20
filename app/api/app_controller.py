from typing import List
from fastapi import APIRouter

from app.model.level import Level
from app.model.sensor_data import SensorData
from app.service.level_service import LevelService
from app.service.temperature_service import TemperatureService

router = APIRouter(prefix="/app")
level_service = LevelService()
temperature_service = TemperatureService()


@router.get(
    "/temperature/avg/{n}",
    response_model=List[SensorData],
    tags=["APP"],
)
async def get_last_avg_temperature(n: int):
    """
    Get the average temperature and humidity for the past N days.

    **Request**:
    - `n`: Number of days for average calculation.

    **Example response**:
    ```json
    [
      {
        "count": 0,
        "date": "18/03",
        "temp": 22.5,
        "humi": 60.0
      },
      {
        "count": 1,
        "date": "17/03",
        "temp": 23.0,
        "humi": 65.0
      }
    ]
    ```
    """
    return temperature_service.get_temperature_last_n_avg(n)


@router.get("/temperature/last/{n}", response_model=List[SensorData], tags=["APP"])
async def get_last_n_temperatures(n: int):
    """
    Get the last N temperature records, ordered by date.

    **Request**:
    - `n`: Number of latest temperature records.

    **Example response**:
    ```json
    [
      {
        "count": 0,
        "date": "2025-03-11T10:20:30Z",
        "temp": 23.5,
        "humi": 10.2
      },
      {
        "count": 1,
        "date": "2025-03-10T10:20:30Z",
        "temp": 23.0,
        "humi": 11.0
      }
    ]
    ```
    """
    return temperature_service.get_last_n_temperature_records(n)


@router.get("/temperature/{n}", response_model=List[SensorData], tags=["APP"])
async def get_temperature_days(days: int):
    """
    Get temperature data for the past X days.

    **Request**:
    - `n`: Number of days to look back.

    **Example response**:
    ```json
    [
      {
        "count": 0,
        "date": "2025-03-11T10:20:30Z",
        "temp": 23.5,
        "humi": 10.2
      },
      {
        "count": 1,
        "date": "2025-03-10T10:20:30Z",
        "temp": 23.0,
        "humi": 11.0
      }
    ]
    ```
    """
    return temperature_service.get_temperature_by_days(days)


@router.get("/temperature/date/{date}", response_model=List[SensorData], tags=["APP"])
async def get_temperature_date(date: str):
    """
    Get temperature data for a specific date.

    **Request**:
    - `date`: Date in `DDMMYYYY` format.

    **Example response**:
    ```json
    [
      {
        "count": 0,
        "date": "2025-03-11T10:20:30Z",
        "temp": 23.5,
        "humi": 10.2
      }
    ]
    ```
    """
    return temperature_service.get_temperature_by_date(date)


@router.get("/level/avg/{n}", response_model=List[Level], tags=["APP"])
async def get_last_n_level(n: int):
    """
    Get the average level for the past N days.

    **Request**:
    - `n`: Number of days for average calculation.

    **Example response**:
    ```json
    [
      {
        "count": 0,
        "date": "18/03",
        "level": 5.0
      },
      {
        "count": 1,
        "date": "17/03",
        "level": 4.8
      }
    ]
    ```
    """
    return level_service.get_levels_last_n_avg(n)


@router.get("/level/last/{n}", response_model=List[Level], tags=["APP"])
async def get_last_n_levels(n: int):
    """
    Get the last N level records, ordered by date.

    **Request**:
    - `n`: Number of latest level records.

    **Example response**:
    ```json
    [
      {
        "count": 0,
        "date": "2025-03-11T10:20:30Z",
        "level": 5.0
      },
      {
        "count": 1,
        "date": "2025-03-10T10:20:30Z",
        "level": 4.9
      }
    ]
    ```
    """
    return level_service.get_last_n_level_records(n)


@router.get("/level/{n}", response_model=List[Level], tags=["APP"])
async def get_level_days(days: int):
    """
    Get level data for the past X days.

    **Request**:
    - `n`: Number of days to look back.

    **Example response**:
    ```json
    [
      {
        "count": 0,
        "date": "2025-03-11T10:20:30Z",
        "level": 5.0
      },
      {
        "count": 1,
        "date": "2025-03-10T10:20:30Z",
        "level": 4.9
      }
    ]
    ```
    """
    return level_service.get_level_by_days(days)


@router.get("/level/date/{n}", response_model=List[Level], tags=["APP"])
async def get_level_date(date: str):
    """
    Get level data for a specific date.

    **Request**:
    - `n`: Date in `DDMMYYYY` format.

    **Example response**:
    ```json
    [
      {
        "count": 0,
        "date": "2025-03-11T10:20:30Z",
        "level": 5.0
      }
    ]
    ```
    """
    return level_service.get_level_by_date(date)
