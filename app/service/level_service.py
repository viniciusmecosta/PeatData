import random

from sqlalchemy.orm import Session

from app.model.level import Level
from app.repository.level_repository import create_level
from app.model.db_models.level import Level as LevelDB

from datetime import datetime, timedelta
import uuid

class LevelService:
    def __init__(self, db: Session):
        self.db = db

    def handle_level(self, level_value: float):
        level_data = Level(id=uuid.uuid4(), level=level_value, date=datetime.now()) # Use Pydantic Model
        create_level(self.db, level_data)

    def delete_all_level_data(self):
        self.db.query(LevelDB).delete()
        self.db.commit()

    def generate_level_data(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=31)
        current_date = start_date

        while current_date <= end_date:
            level = random.uniform(0.0, 10.0)
            level_data = LevelDB(id=uuid.uuid4(), level=level, date=current_date)
            self.db.add(level_data)
            current_date += timedelta(hours=random.randint(1, 4))

        self.db.commit()