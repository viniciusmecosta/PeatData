import random
from sqlalchemy.orm import Session
from app.model.level import Level
from app.repository.level_repository import create_level, get_last_n_avg_level_data, get_last_n_level_records, \
    get_level_by_days, get_level_by_date
from app.model.db_models.level import Level as LevelDB
from app.core.utils import calculate_comedouro_level
from datetime import datetime, timedelta
import uuid

class LevelService:
    def __init__(self, db: Session):
        self.db = db

    def handle_level(self, level_value: float):
        calculated_level = calculate_comedouro_level(level_value)
        level_data = Level(id=uuid.uuid4(), level=calculated_level, date=datetime.now())
        create_level(self.db, level_data)

    def delete_all_level_data(self):
        self.db.query(LevelDB).delete()
        self.db.commit()

    def generate_level_data(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=31)
        current_date = start_date

        while current_date <= end_date:
            for i in range(2):
                measurement_time = current_date + timedelta(hours=3 * i)

                if measurement_time > datetime.now():
                    continue

                raw_level = round(random.uniform(2.0, 25.0), 1)
                calculated_level = calculate_comedouro_level(raw_level)

                level_data = LevelDB(
                    id=uuid.uuid4(),
                    level=calculated_level,
                    date=measurement_time
                )
                self.db.add(level_data)

            current_date += timedelta(days=1)

        self.db.commit()

    def get_last_n_avg_level(self, n: int):
        return get_last_n_avg_level_data(self.db, n)

    def get_last_n_level_records(self, n: int):
        return get_last_n_level_records(self.db, n)

    def get_level_by_days(self, days: int):
        return get_level_by_days(self.db, days)

    def get_level_by_date(self, date: str):
        return get_level_by_date(self.db, date)
