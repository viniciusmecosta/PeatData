
from sqlalchemy.orm import Session
from app.repository.level_repository import create_level
from app.model.level import Level # Pydantic Model
from datetime import datetime
import uuid

class LevelService:
    def __init__(self, db: Session):
        self.db = db

    def handle_level(self, level_value: float):
        level_data = Level(id=uuid.uuid4(), level=level_value, date=datetime.now()) # Use Pydantic Model
        create_level(self.db, level_data)