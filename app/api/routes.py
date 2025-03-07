from fastapi import APIRouter
from app.domain.services import (
    handle_temperature_humidity,
    handle_distance,
    get_all_records,
    get_temperature_by_days,
    get_temperature_by_date,
    get_distance_by_days,
    get_distance_by_date
)

router = APIRouter()

@router.post("/temperature-humidity")
async def post_temperature_humidity(temperature: float, humidity: float):
    handle_temperature_humidity(temperature, humidity)
    return {"message": "Temperature and humidity data received successfully"}

@router.post("/distance")
async def post_distance(distance: float):
    handle_distance(distance)
    return {"message": "Distance data received successfully"}

@router.get("/records")
async def get_records():
    return get_all_records()

@router.get("/temperature/{days}")
async def get_temperature_days(days: int):
    return get_temperature_by_days(days)

@router.get("/temperature/date/{date}")
async def get_temperature_date(date: str):
    return get_temperature_by_date(date)

@router.get("/distance/{days}")
async def get_distance_days(days: int):
    return get_distance_by_days(days)

@router.get("/distance/date/{date}")
async def get_distance_date(date: str):
    return get_distance_by_date(date)