from sqlalchemy.orm import Session

from models.personal_info import PersonalInfo
from schemas.PersonalInfoSchema import PersonalInfoCreate, PersonalInfoUpdate


class PersonalInfoService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def get_all_personal_info(self):
        return self.db.query(PersonalInfo).all()

    def get_personal_info(self, personal_info_id: int):
        return self.db.query(PersonalInfo).filter(PersonalInfo.id == personal_info_id).first()

    def create_personal_info(self, personal_info: PersonalInfoCreate):
        personal_info = personal_info.model_dump()
        db_personal_info = PersonalInfo(**personal_info)
        self.db.add(db_personal_info)
        self.db.commit()
        self.db.refresh(db_personal_info)
        return db_personal_info

    def update_personal_info(self, personal_info_id: int, personal_info: PersonalInfoUpdate):
        db_personal_info = self.db.query(PersonalInfo).filter(PersonalInfo.id == personal_info_id).first()
        for var, value in personal_info.model_dump().items():
            setattr(db_personal_info, var, value)
        self.db.commit()
        self.db.refresh(db_personal_info)
        return db_personal_info

    def delete_personal_info(self, personal_id: int):
        db_personal_info = self.db.query(PersonalInfo).filter(PersonalInfo.id == personal_id).first()
        self.db.delete(db_personal_info)
        self.db.commit()
        return db_personal_info



