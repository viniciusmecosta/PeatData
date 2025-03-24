from datetime import datetime, timedelta

from sqlalchemy import func
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

def get_last_n_avg_sensor_data(db: Session, n: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=n)

    result = db.query(
        func.date_format(SensorData.date, '%d/%m').label('date'),
        func.avg(SensorData.temperature).label('temp'),
        func.avg(SensorData.humidity).label('humi')
    ).filter(SensorData.date >= start_date).group_by(func.date_format(SensorData.date, '%d/%m')).all()

    return result

def get_last_n_sensor_data_records(db: Session, n: int):
    return db.query(SensorData).order_by(SensorData.date.desc()).limit(n).all()

def get_sensor_data_by_days(db: Session, days: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return db.query(SensorData).filter(SensorData.date >= start_date).all()

def get_sensor_data_by_date(db: Session, date: str):
    try:
        date_obj = datetime.strptime(date, '%d%m%Y')
    except ValueError:
        return []

    start_date = date_obj.replace(hour=0, minute=0, second=0)
    end_date = date_obj.replace(hour=23, minute=59, second=59)
    return db.query(SensorData).filter(SensorData.date.between(start_date, end_date)).all()