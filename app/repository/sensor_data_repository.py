from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.model.db_models.sensor_data import SensorData
from uuid import UUID


def get_sensor_data(db: Session, sensor_data_id: UUID):
    return db.query(SensorData).filter(SensorData.id == sensor_data_id).first()


def create_sensor_data(
    db: Session, temperature: float, humidity: float, date: datetime
):
    sensor_data = SensorData(temperature=temperature, humidity=humidity, date=date)
    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)
    return sensor_data


def get_last_n_avg_sensor_data(db: Session, n: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=n)

    result = (
        db.query(
            func.strftime("%d/%m", SensorData.date).label("date"),
            func.round(func.avg(SensorData.temperature), 1).label("temp"),
            func.round(func.avg(SensorData.humidity), 1).label("humi"),
        )
        .filter(SensorData.date >= start_date)
        .group_by(func.strftime("%d/%m", SensorData.date))
        .order_by(func.strftime("%Y-%m-%d", SensorData.date).desc())
        .all()
    )

    return [{"date": r.date, "temp": r.temp, "humi": r.humi} for r in result]


def get_last_n_sensor_data_records(db: Session, n: int):
    result = (
        db.query(SensorData.date, SensorData.temperature, SensorData.humidity)
        .order_by(SensorData.date.desc())
        .limit(n)
        .all()
    )

    return [
        {"date": r[0].strftime("%H:%M %d/%m/%y"), "temp": r[1], "humi": r[2]}
        for r in result
    ]


def get_sensor_data_by_days(db: Session, days: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    result = (
        db.query(SensorData.date, SensorData.temperature, SensorData.humidity)
        .filter(SensorData.date >= start_date)
        .order_by(SensorData.date.desc())
        .all()
    )

    return [
        {"date": r[0].strftime("%d/%m/%Y %H:%M"), "temp": r[1], "humi": r[2]}
        for r in result
    ]


def get_sensor_data_by_date(db: Session, date: str):
    date_obj = datetime.strptime(date, "%d%m%Y").date()

    result = (
        db.query(SensorData.date, SensorData.temperature, SensorData.humidity)
        .filter(func.date(SensorData.date) == date_obj)
        .order_by(SensorData.date.desc())
        .all()
    )

    return [
        {"date": r[0].strftime("%H:%M"), "temp": r[1], "humi": r[2]} for r in result
    ]
