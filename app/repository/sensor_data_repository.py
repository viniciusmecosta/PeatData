from datetime import datetime

from sqlalchemy.orm import Session
from app.model.db_models.sensor_data import SensorData
from fastapi import HTTPException
from uuid import UUID

def get_sensor_data(db: Session, sensor_data_id: UUID):
    return db.query(SensorData).filter(SensorData.id == sensor_data_id).first()

def create_sensor_data(db: Session, temperature: float, humidity: float, date: datetime):
    sensor_data = SensorData(temperature=temperature, humidity=humidity, date=date)
    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)
    return sensor_data

def update_sensor_data(db: Session, sensor_data_id: UUID, sensor_data: SensorData):
    db_sensor_data = db.query(SensorData).filter(SensorData.id == sensor_data_id).first()
    if not db_sensor_data:
        raise HTTPException(status_code=404, detail="SensorData não encontrado")
    for key, value in sensor_data.dict().items():
        setattr(db_sensor_data, key, value)
    db.commit()
    db.refresh(db_sensor_data)
    return db_sensor_data

def delete_sensor_data(db: Session, sensor_data_id: UUID):
    db_sensor_data = db.query(SensorData).filter(SensorData.id == sensor_data_id).first()
    if not db_sensor_data:
        raise HTTPException(status_code=404, detail="SensorData não encontrado")
    db.delete(db_sensor_data)
    db.commit()
    return db_sensor_data