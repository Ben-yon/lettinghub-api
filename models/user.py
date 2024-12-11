from enum import unique

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Table, Date
from sqlalchemy.orm import relationship

from core.db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


