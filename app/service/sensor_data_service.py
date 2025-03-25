from sqlalchemy.orm import Session
from app.model.db_models.sensor_data import SensorData
from datetime import datetime, timedelta
import random
import uuid

from app.repository.sensor_data_repository import create_sensor_data, get_last_n_avg_sensor_data, \
    get_sensor_data_by_days, get_last_n_sensor_data_records, get_sensor_data_by_date

class SensorDataService:
    def __init__(self, db: Session):
        self.db = db

    def handle_sensor_data(self, temperature: float, humidity: float):
        create_sensor_data(self.db, temperature, humidity, datetime.now())

    def delete_all_sensor_data(self):
        self.db.query(SensorData).delete()
        self.db.commit()

    def generate_sensor_data(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=31)
        current_date = start_date

        while current_date <= end_date:
            for i in range(2):
                measurement_time = current_date + timedelta(hours=3 * i)

                if measurement_time > datetime.now():
                    continue

                temperature = round(random.uniform(20.0, 30.0), 1)
                humidity = round(random.uniform(50.0, 80.0), 1)

                sensor_data = SensorData(
                    id=uuid.uuid4(),
                    temperature=temperature,
                    humidity=humidity,
                    date=measurement_time
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
