from sqlalchemy import Column, String, UUID
from app.core.database import Base
import uuid


class Phone(Base):
    __tablename__ = "phones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    number = Column(String)
