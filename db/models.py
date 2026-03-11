from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from sqlalchemy.sql.traversals import ColIdentityComparatorStrategy
from .database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True)
    long_url = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow)
