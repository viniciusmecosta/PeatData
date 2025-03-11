from fastapi import APIRouter
from app.domain.services import (
    handle_temperature_humidity,
    handle_distance,
    get_temperature_by_days,
    get_temperature_by_date,
    get_distance_by_days,
    get_distance_by_date
)
from pydantic import BaseModel
from typing import List

router = APIRouter()

class TemperatureHumidityRequest(BaseModel):
    temperature: float
    humidity: float

class DistanceRequest(BaseModel):
    distance: float

class TemperatureResponse(BaseModel):
    count: int
    data: str
    temp: float

class DistanceResponse(BaseModel):
    count: int
    data: str
    distance: float

@router.post("/temperature-humidity", tags=["ESP"])
async def post_temperature_humidity(data: TemperatureHumidityRequest):
    """
    Endpoint to submit temperature and humidity data.

    **Request body:**
    - `temperature`: The temperature value to be submitted.
    - `humidity`: The humidity value to be submitted.

    **Example:**
    ```json
    {
      "temperature": 23.5,
      "humidity": 60.0
    }
    ```

    **Response:**
    - Success message when data is received.
    """
    handle_temperature_humidity(data.temperature, data.humidity)
    return {"message": "Temperature and humidity data received successfully"}

@router.post("/distance", tags=["ESP"])
async def post_distance(data: DistanceRequest):
    """
    Endpoint to submit distance data.

    **Request body:**
    - `distance`: The distance value to be submitted.

    **Example:**
    ```json
    {
      "distance": 5.0
    }
    ```

    **Response:**
    - Success message when data is received.
    """
    handle_distance(data.distance)
    return {"message": "Distance data received successfully"}

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

    **Example:**
    ```json
    [
      {
        "count": 1,
        "data": "2025-03-11T10:20:30Z",
        "temp": 23.5
      }
    ]
    ```
    """
    return get_temperature_by_days(days)

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

    **Example:**
    ```json
    [
      {
        "count": 1,
        "data": "2025-03-11T10:20:30Z",
        "temp": 23.5
      }
    ]
    ```
    """
    return get_temperature_by_date(date)

@router.get("/distance/{days}", response_model=List[DistanceResponse], tags=["APP"])
async def get_distance_days(days: int):
    """
    Endpoint to get distance data for the past X days.

    **Request path parameter:**
    - `days`: Number of days to look back for distance data.

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Timestamp when the data was recorded.
    - `distance`: Recorded distance value.

    **Example:**
    ```json
    [
      {
        "count": 1,
        "data": "2025-03-11T10:20:30Z",
        "distance": 5.0
      }
    ]
    ```
    """
    return get_distance_by_days(days)

@router.get("/distance/date/{date}", response_model=List[DistanceResponse], tags=["APP"])
async def get_distance_date(date: str):
    """
    Endpoint to get distance data for a specific date.

    **Request path parameter:**
    - `date`: The date in `DDMMYYYY` format (e.g., "11032025").

    **Response model:**
    - `count`: Sequence number of the data.
    - `data`: Timestamp when the data was recorded.
    - `distance`: Recorded distance value.

    **Example:**
    ```json
    [
      {
        "count": 1,
        "data": "2025-03-11T10:20:30Z",
        "distance": 5.0
      }
    ]
    ```
    """
    return get_distance_by_date(date)
