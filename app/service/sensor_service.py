
from sqlalchemy.orm import Session
from app.repository.sensor_data_repository import create_sensor_data
from datetime import datetime

class SensorService:
    def __init__(self, db: Session):
        self.db = db

    def handle_sensor_data(self, temperature: float, humidity: float):
        create_sensor_data(self.db, temperature, humidity, datetime.now())