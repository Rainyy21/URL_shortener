from sqlalchemy.orm import Session
from . import models


def create_url(db: Session, short_code: str, long_url: str):
    db_url = models.URL(short_code=short_code, long_url=long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()
