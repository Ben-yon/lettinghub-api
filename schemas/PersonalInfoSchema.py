from datetime import datetime

from pydantic import BaseModel
from datetime import date


class PersonalInfoBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    date_of_birth: date
    age: int
    address: str
    profession: str
    contact: str
    bio: str

    class Config:
        orm_mode = True
        from_attributes=True

class PersonalInfoUpdate(PersonalInfoBase):
    pass

class PersonalInfoCreate(PersonalInfoBase):
    pass

class PersonalInfoSchema(PersonalInfoBase):
    id: int
