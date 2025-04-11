from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.model.sensor_data_request import SensorDataRequest
from app.model.level_request import LevelRequest
from app.service.level_service import LevelService
from app.service.sensor_data_service import SensorDataService
from app.core.database import get_db

router = APIRouter(prefix="/esp")


def get_services(db: Session = Depends(get_db)):
    return {
        "sensor_service": SensorDataService(db),
        "level_service": LevelService(db),
    }


@router.post("/temperature-humidity", tags=["ESP"])
async def post_temperature_humidity(
    data: SensorDataRequest, services=Depends(get_services)
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
    sensorData = services["sensor_service"].handle_sensor_data(
        data.temperature, data.humidity
    )
    return {
        "message": "Temperature and humidity data received successfully",
        "temperature": f"{sensorData.temp}",
        "humidity": f"{sensorData.humi}",
        "date": f"{sensorData.date}",
    }


@router.post("/level", tags=["ESP"])
async def post_distance(data: LevelRequest, services=Depends(get_services)):
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
      "message": "Level data received successfully",
      "level": "78.0",
      "date": "2025-04-11 09:46:52.799926"
    }
    ```
    """
    response = services["level_service"].handle_level(data.level)
    return {
        "message": "Level data received successfully",
        "level": f"{response.level}",
        "date": f"{response.date}",
    }
