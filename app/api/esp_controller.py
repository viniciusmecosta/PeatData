from fastapi import APIRouter

from app.model.temperature_humidity_request import TemperatureHumidityRequest
from app.model.level_request import LevelRequest
from app.service.level_service import LevelService
from app.service.temperature_service import TemperatureService

router = APIRouter()
temperature_service = TemperatureService()
level_service = LevelService()


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
    temperature_service.handle_temperature_humidity(data.temperature, data.humidity)
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
    level_service.handle_level(data.level)
    return {"message": "Level data received successfully"}
