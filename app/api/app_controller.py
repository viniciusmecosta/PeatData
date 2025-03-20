from typing import List

from fastapi import APIRouter

from app.model.level_model import LevelResponse
from app.model.temperature_response import TemperatureResponse
from app.service.level_service import LevelService
from app.service.temperature_service import TemperatureService

router = APIRouter()
level_service = LevelService()
temperature_service = TemperatureService()

@router.get("/temperature/last_n_avg/{n}", response_model=List[TemperatureResponse], tags=["APP"])
async def get_last_n_avg_temperatures(n: int):
    """
    Endpoint to get the average temperature and humidity for the past N days.

    **Request path parameter:**
    - `n`: Number of days to calculate the average.

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Formatted date (DD/MM).
    - `temp`: Average temperature for the day.
    - `humi`: Average humidity for the day.

    **Example request:**
    ```json
    GET /temperature/last_n_avg/3
    ```

    **Example response:**
    ```json
    [
      {
        "count": 0,
        "data": "18/03",
        "temp": 22.5,
        "humi": 60.0
      },
      {
        "count": 1,
        "data": "17/03",
        "temp": 23.0,
        "humi": 65.0
      },
      {
        "count": 2,
        "data": "16/03",
        "temp": 21.0,
        "humi": 62.0
      }
    ]
    ```
    """
    return temperature_service.get_temperature_last_n_avg(n)


@router.get("/temperature/last/{n}", response_model=List[TemperatureResponse], tags=["APP"])
async def get_last_n_temperatures(n: int):
    """
    Endpoint to get the last N temperature records, ordered by date.

    **Request path parameter:**
    - `n`: Number of latest temperature records to retrieve.

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Timestamp when the data was recorded.
    - `temp`: Recorded temperature value.
    - `humi`: Recorded humidity value.

    **Example request:**
    ```json
    GET /temperature/last/5
    ```

    **Example response:**
    ```json
    [
      {
        "count": 0,
        "data": "2025-03-11T10:20:30Z",
        "temp": 23.5,
        "humi": 10.2
      }
    ]
    ```
    """
    return temperature_service.get_last_n_temperature_records(n)

@router.get("/temperature/{days}", response_model=List[TemperatureResponse], tags=["APP"])
async def get_temperature_days(days: int):
    """
    Endpoint to get temperature data for the past X days.

    **Request path parameter:**
    - `days`: Number of days to look back for temperature data.

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Timestamp when the data was recorded.
    - `temp`: Recorded temperature value.
    - `humi`: Recorded humidity value.

    **Example request:**
    ```json
    GET /temperature/7
    ```

    **Example response:**
    ```json
    [
      {
        "count": 0,
        "data": "2025-03-11T10:20:30Z",
        "temp": 23.5,
        "humi": 10.2
      }
    ]
    ```
    """
    return temperature_service.get_temperature_by_days(days)

@router.get("/temperature/date/{date}", response_model=List[TemperatureResponse], tags=["APP"])
async def get_temperature_date(date: str):
    """
    Endpoint to get temperature data for a specific date.

    **Request path parameter:**
    - `date`: The date in `DDMMYYYY` format (e.g., "11032025").

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Timestamp when the data was recorded.
    - `temp`: Recorded temperature value.
    - `humi`: Recorded humidity value.

    **Example request:**
    ```json
    GET /temperature/date/11032025
    ```

    **Example response:**
    ```json
    [
      {
        "count": 0,
        "data": "2025-03-11T10:20:30Z",
        "temp": 23.5,
        "humi": 10.2
      }
    ]
    ```
    """
    return temperature_service.get_temperature_by_date(date)

@router.get("/level/last_n_avg/{n}", response_model=List[LevelResponse], tags=["APP"])
async def get_last_n_avg_levels(n: int):
    """
    Endpoint to get the average temperature and humidity for the past N days.

    **Request path parameter:**
    - `n`: Number of days to calculate the average.

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Formatted date (DD/MM).
    - `temp`: Average temperature for the day.
    - `humi`: Average humidity for the day.

    **Example request:**
    ```json
    GET /temperature/last_n_avg/3
    ```

    **Example response:**
    ```json
    [
      {
        "count": 0,
        "data": "18/03",
        "temp": 22.5,
        "humi": 60.0
      },
      {
        "count": 1,
        "data": "17/03",
        "temp": 23.0,
        "humi": 65.0
      },
      {
        "count": 2,
        "data": "16/03",
        "temp": 21.0,
        "humi": 62.0
      }
    ]
    ```
    """
    return level_service.get_levels_last_n_avg(n)
@router.get("/level/last/{n}", response_model=List[LevelResponse], tags=["APP"])
async def get_last_n_levels(n: int):
    """
    Endpoint to get the last N level records, ordered by date.

    **Request path parameter:**
    - `n`: Number of latest level records to retrieve.

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Timestamp when the data was recorded.
    - `level`: Recorded level value.

    **Example request:**
    ```json
    GET /level/last/5
    ```

    **Example response:**
    ```json
    [
      {
        "count": 0,
        "data": "2025-03-11T10:20:30Z",
        "level": 5.0
      }
    ]
    ```
    """
    return level_service.get_last_n_level_records(n)

@router.get("/level/{days}", response_model=List[LevelResponse], tags=["APP"])
async def get_level_days(days: int):
    """
    Endpoint to get level data for the past X days.

    **Request path parameter:**
    - `days`: Number of days to look back for level data.

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Timestamp when the data was recorded.
    - `level`: Recorded level value.

    **Example request:**
    ```json
    GET /level/7
    ```

    **Example response:**
    ```json
    [
      {
        "count": 0,
        "data": "2025-03-11T10:20:30Z",
        "level": 5.0
      }
    ]
    ```
    """
    return level_service.get_level_by_days(days)

@router.get("/level/date/{date}", tags=["APP"])
async def get_level_date(date: str):
    """
    Endpoint to get level data for a specific date.

    **Request path parameter:**
    - `date`: The date in `DDMMYYYY` format (e.g., "11032025").

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Timestamp when the data was recorded.
    - `level`: Recorded level value.

    **Example request:**
    ```json
    GET /level/date/11032025
    ```

    **Example response:**
    ```json
    [
      {
        "count": 0,
        "data": "2025-03-11T10:20:30Z",
        "level": 5.0
      }
    ]
    ```
    """
    return level_service.get_level_by_date(date)