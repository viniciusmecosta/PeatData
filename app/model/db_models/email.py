import uuid

from sqlalchemy import Column, String, UUID
from app.core.database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, index=True)
    name = Column(String)