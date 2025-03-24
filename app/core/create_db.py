
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import DATABASE_URL, Base
from app.model.db_models.phone import Phone
from app.model.db_models.email import Email
from app.model.db_models.level import Level
from app.model.db_models.sensor_data import SensorData
from datetime import datetime
import uuid

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Inserir dados de exemplo para Phone
phone1 = Phone(id=uuid.uuid4(), name="João Silva", number="11999999999")
phone2 = Phone(id=uuid.uuid4(), name="Maria Oliveira", number="21988888888")

# Inserir dados de exemplo para Email
email1 = Email(id=uuid.uuid4(), name="joao.silva", email="joao.silva@example.com")
email2 = Email(id=uuid.uuid4(), name="maria.oliveira", email="maria.oliveira@example.com")

# Inserir dados de exemplo para Level
level1 = Level(id=uuid.uuid4(), date=datetime(2023, 10, 26, 10, 0, 0), level=10.5)
level2 = Level(id=uuid.uuid4(), date=datetime(2023, 10, 26, 11, 0, 0), level=11.2)

# Inserir dados de exemplo para SensorData
sensor_data1 = SensorData(id=uuid.uuid4(), date=datetime(2023, 10, 26, 10, 0, 0), temperature=25.0, humidity=60.0)
sensor_data2 = SensorData(id=uuid.uuid4(), date=datetime(2023, 10, 26, 11, 0, 0), temperature=26.5, humidity=65.0)

session.add_all([phone1, phone2, email1, email2, level1, level2, sensor_data1, sensor_data2])
session.commit()
session.close()

print("Dados inseridos com sucesso!")