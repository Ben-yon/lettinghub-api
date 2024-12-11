
from sqlalchemy import Integer, String, Date, Column

from core.db import Base


class PersonalInfo(Base):
    __tablename__ = 'PersonalInfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(String)
    address = Column(String)
    profession = Column(String)
    date_of_birth = Column(Date)
    email = Column(String, unique=True, index=True)
    contact = Column(String)
    bio = Column(String)