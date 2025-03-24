# app/repository/level_repository.py
from sqlalchemy.orm import Session
from app.model.db_models.level import Level as LevelDB
from app.model.level import Level
from fastapi import HTTPException
from uuid import UUID

def get_level(db: Session, level_id: UUID):
    return db.query(LevelDB).filter(LevelDB.id == level_id).first()

def create_level(db: Session, level: Level):
    db_level = LevelDB(**level.dict()) # Convert Pydantic to SQLAlchemy
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return level # Return Pydantic Model

def update_level(db: Session, level_id: UUID, level: Level):
    db_level = db.query(LevelDB).filter(LevelDB.id == level_id).first()
    if not db_level:
        raise HTTPException(status_code=404, detail="Level não encontrado")
    for key, value in level.dict().items():
        setattr(db_level, key, value)
    db.commit()
    db.refresh(db_level)
    return level

def delete_level(db: Session, level_id: UUID):
    db_level = db.query(LevelDB).filter(LevelDB.id == level_id).first()
    if not db_level:
        raise HTTPException(status_code=404, detail="Level não encontrado")
    db.delete(db_level)
    db.commit()
    return level