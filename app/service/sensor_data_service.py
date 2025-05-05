from sqlalchemy.orm import Session
from app.model.db_models.sensor_data import SensorData
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random
import uuid

from app.model.sensor_data_response import SensorDataResponse
from app.repository.sensor_data_repository import (
    create_sensor_data,
    get_last_n_avg_sensor_data,
    get_sensor_data_by_days,
    get_last_n_sensor_data_records,
    get_sensor_data_by_date,
)


class SensorDataService:
    def __init__(self, db: Session):
        self.db = db

    def handle_sensor_data(self, temperature: float, humidity: float):
        date = datetime.now(ZoneInfo("America/Fortaleza"))
        create_sensor_data(self.db, temperature, humidity, date)
        return SensorDataResponse(temp=temperature, humi=humidity, date=str(date))

    def delete_all_sensor_data(self):
        self.db.query(SensorData).delete()
        self.db.commit()

    def generate_sensor_data(self):
        tz = ZoneInfo("America/Fortaleza")
        now = datetime.now(tz)
        end_date = now
        start_date = end_date - timedelta(days=31)
        current_date = start_date

        while current_date <= end_date:
            for i in range(2):
                hours_ago = 6 - (i * 3)
                measurement_time = datetime(
                    current_date.year, current_date.month, current_date.day, tzinfo=tz
                ) + timedelta(
                    hours=now.hour - hours_ago, minutes=now.minute, seconds=now.second
                )

                if measurement_time > now:
                    continue

                temperature = round(random.uniform(20.0, 40.0), 1)
                humidity = round(random.uniform(10.0, 98.0), 1)

                sensor_data = SensorData(
                    id=uuid.uuid4(),
                    temperature=temperature,
                    humidity=humidity,
                    date=measurement_time,
                )
                self.db.add(sensor_data)

            current_date += timedelta(days=1)

        self.db.commit()

    def get_sensor_data_last_n_avg(self, n: int):
        return get_last_n_avg_sensor_data(self.db, n)

    def get_last_n_sensor_data_records(self, n: int):
        return get_last_n_sensor_data_records(self.db, n)

    def get_sensor_data_by_days(self, days: int):
        return get_sensor_data_by_days(self.db, days)

    def get_sensor_data_by_date(self, date: str):
        return get_sensor_data_by_date(self.db, date)
