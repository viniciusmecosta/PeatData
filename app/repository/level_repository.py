from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.model.db_models.level import Level as LevelDB
from app.model.level import Level
from fastapi import HTTPException
from uuid import UUID

# Get Level by ID
def get_level(db: Session, level_id: UUID):
    return db.query(LevelDB).filter(LevelDB.id == level_id).first()

# Create Level
def create_level(db: Session, level: Level):
    db_level = LevelDB(**level.dict())  # Convert Pydantic to SQLAlchemy
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return level  # Return Pydantic Model

def get_last_n_avg_level_data(db: Session, n: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=n)

    result = db.query(
        func.strftime('%d/%m', LevelDB.date).label('date'),
        func.avg(LevelDB.level).label('level')
    ).filter(LevelDB.date >= start_date)\
     .group_by(func.strftime('%d/%m', LevelDB.date))\
     .order_by(func.strftime('%Y-%m-%d', LevelDB.date).desc())\
     .all()

    return [{"date": r.date, "level": r.level} for r in result]

# Get Last N Level Records
def get_last_n_level_records(db: Session, n: int):
    result = db.query(LevelDB.date, LevelDB.level)\
        .order_by(LevelDB.date.desc())\
        .limit(n).all()

    return [{"date": r[0].strftime("%d/%m/%Y %H:%M"), "level": r[1]} for r in result]

def get_level_by_days(db: Session, days: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    result = db.query(LevelDB.date, LevelDB.level)\
        .filter(LevelDB.date >= start_date)\
        .order_by(LevelDB.date.desc()).all()

    return [{"date": r[0].strftime("%d/%m/%Y %H:%M"), "level": r[1]} for r in result]

def get_level_by_date(db: Session, date: str):
    date_obj = datetime.strptime(date, "%d%m%Y").date()

    result = db.query(LevelDB.date, LevelDB.level) \
        .filter(func.date(LevelDB.date) == date_obj) \
        .order_by(LevelDB.date.desc()) \
        .all()

    return [{"date": r[0].strftime("%H:%M"), "level": r[1]} for r in result]
