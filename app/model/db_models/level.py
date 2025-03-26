import uuid


from sqlalchemy import Column, DateTime, Float, UUID
from app.core.database import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    date = Column(DateTime)
    level = Column(Float)
