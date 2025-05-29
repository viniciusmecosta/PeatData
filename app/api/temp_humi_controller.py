from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
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
    services: SensorDataService = Depends(get_sensor_data_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    sensorData = services.handle_sensor_data(data.temperature, data.humidity)
    return {
        "message": "Temperature and humidity data received successfully",
        "temperature": f"{sensorData.temp}",
        "humidity": f"{sensorData.humi}",
        "date": f"{sensorData.date}",
    }


@router.get(
    "/temp-humi",
    summary="Gets temperature and humidity data based on query parameters",
    description="Retrieve temperature and humidity data using one of the query parameters: `avg`, `last`, `days`, or `date`.\n\n"
    "Only one parameter should be provided per request.",
)
async def get_temp_humi_data(
    avg: Optional[int] = None,
    last: Optional[int] = None,
    days: Optional[int] = None,
    date: Optional[str] = None,
    services: SensorDataService = Depends(get_sensor_data_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    params_provided = sum(p is not None for p in [avg, last, days, date])

    if params_provided == 0:
        raise HTTPException(
            status_code=400,
            detail="Please provide one query parameter: 'avg', 'last', 'days', or 'date'.",
        )
    if params_provided > 1:
        raise HTTPException(
            status_code=400,
            detail="Please provide only one of the query parameters: 'avg', 'last', 'days', or 'date'.",
        )

    if avg is not None:
        return services.get_sensor_data_last_n_avg(avg)
    elif last is not None:
        return services.get_last_n_sensor_data_records(last)
    elif days is not None:
        return services.get_sensor_data_by_days(days)
    elif date is not None:
        return services.get_sensor_data_by_date(date)

    raise HTTPException(
        status_code=500, detail="Internal server error: No valid parameter processed."
    )
