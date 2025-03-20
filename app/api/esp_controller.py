from fastapi import APIRouter
from app.model.sensor_data_request import SensorDataRequest
from app.model.level_request import LevelRequest
from app.service.level_service import LevelService
from app.service.temperature_service import TemperatureService

router = APIRouter(prefix="/esp")
temperature_service = TemperatureService()
level_service = LevelService()


@router.post("/temperature-humidity", tags=["ESP"])
async def post_temperature_humidity(data: SensorDataRequest):
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
      "message": "Temperature and humidity data received successfully"
    }
    ```
    """
    temperature_service.handle_temperature_humidity(data.temperature, data.humidity)
    return {"message": "Temperature and humidity data received successfully"}


@router.post("/level", tags=["ESP"])
async def post_distance(data: LevelRequest):
    """
    Submit level data.

    **Request body**:
    - `level`: Level value.

    **Example request**:
    ```json
    {
      "level": 5.0
    }
    ```

    **Example response**:
    ```json
    {
      "message": "Level data received successfully"
    }
    ```
    """
    level_service.handle_level(data.level)
    return {"message": "Level data received successfully"}
