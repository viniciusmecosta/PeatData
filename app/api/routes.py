from fastapi import APIRouter
from typing import List

from app.model.level_model import LevelResponse
from app.model.temperature_humidity_request import TemperatureHumidityRequest
from app.model.level_request import LevelRequest
from app.model.temperature_response import TemperatureResponse
from app.service.services import (
    add_email,
    add_phone,
    get_all_emails,
    get_all_phones,
    handle_temperature_humidity,
    handle_level,
    get_temperature_by_days,
    get_temperature_by_date,
    get_level_by_days,
    get_level_by_date,
    get_last_n_temperature_records,
    get_last_n_level_records,
    get_temperature_last_n_avg, get_levels_last_n_avg
)

router = APIRouter()

@router.post("/temperature-humidity", tags=["ESP"])
async def post_temperature_humidity(data: TemperatureHumidityRequest):
    """
    Endpoint to submit temperature and humidity data.

    **Request body:**
    - `temperature`: The temperature value to be submitted.
    - `humidity`: The humidity value to be submitted.

    **Example request:**
    ```json
    {
      "temperature": 23.5,
      "humidity": 60.0
    }
    ```

    **Response:**
    - Success message when data is received.

    **Example response:**
    ```json
    {
      "message": "Temperature and humidity data received successfully"
    }
    ```
    """
    handle_temperature_humidity(data.temperature, data.humidity)
    return {"message": "Temperature and humidity data received successfully"}

@router.post("/level", tags=["ESP"])
async def post_distance(data: LevelRequest):
    """
    Endpoint to submit Level data.

    **Request body:**
    - `level`: The Level value to be submitted.

    **Example request:**
    ```json
    {
      "level": 5.0
    }
    ```

    **Response:**
    - Success message when data is received.

    **Example response:**
    ```json
    {
      "message": "Level data received successfully"
    }
    ```
    """
    handle_level(data.level)
    return {"message": "Level data received successfully"}

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
    return get_temperature_last_n_avg(n)


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
    return get_last_n_temperature_records(n)

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
    return get_temperature_by_date(date)

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
    return get_levels_last_n_avg(n)
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
    return get_last_n_level_records(n)

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
    return get_level_by_days(days)

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
    return get_level_by_date(date)

@router.post("/phone", tags=["NOTIFY"])
async def post_phone(name: str, number: str):
    """
    Adds a phone number to the system.

    - **name**: Name associated with the phone number.
    - **number**: Phone number (must be 11 digits).

    **Example request:**
    ```json
    {
      "name": "João Silva",
      "number": "11987654321"
    }
    ```

    **Response:**
    - Success message when phone number is added.

    **Example response:**
    ```json
    {
      "message": "Phone number added successfully"
    }
    ```
    """
    if len(number) != 11 or not number.isdigit():
        return {"error": "Number must have 11 digits"}
    
    add_phone(name, number)
    return {"message": "Phone number added successfully"}

@router.get("/phone", tags=["NOTIFY"])
async def get_phones():
    """
    Retrieves all registered phone numbers.

    Returns a list of phone numbers with their associated names.

    **Example response:**
    ```json
    [
      {
        "name": "João Silva",
        "number": "11987654321"
      }
    ]
    ```
    """
    return get_all_phones()

@router.post("/email", tags=["NOTIFY"])
async def post_email(name: str, email: str):
    """
    Adds an email address to the system.

    - **name**: Name associated with the email address.
    - **email**: Email address to be added.

    **Example request:**
    ```json
    {
      "name": "Maria Oliveira",
      "email": "maria.oliveira@example.com"
    }
    ```

    **Response:**
    - Success message when email address is added.

    **Example response:**
    ```json
    {
      "message": "Email added successfully"
    }
    ```
    """
    add_email(name, email)
    return {"message": "Email added successfully"}

@router.get("/email", tags=["NOTIFY"])
async def get_emails():
    """
    Retrieves all registered email addresses.

    Returns a list of email addresses with their associated names.

    **Example response:**
    ```json
    [
      {
        "name": "Maria Oliveira",
        "email": "maria.oliveira@example.com"
      }
    ]
    ```
    """
    return get_all_emails()
