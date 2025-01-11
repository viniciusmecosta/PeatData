from fastapi import APIRouter
from app.domain.services import handle_temperature_humidity, handle_distance, get_all_records

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
