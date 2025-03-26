import uuid

from sqlalchemy import Column, Integer, DateTime, Float, UUID
from app.core.database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    date = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
