from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.utils import get_current_user_id
from services.personal_info_service import PersonalInfoService
from schemas.PersonalInfoSchema import PersonalInfoCreate, PersonalInfoBase, PersonalInfoUpdate, PersonalInfoSchema
from core.db import get_db

router = APIRouter()

@router.get("/personal_info", response_model=list[PersonalInfoSchema])
def read_personal_info(user_id = Depends(get_current_user_id),db: Session = Depends(get_db)):
    return PersonalInfoService(db, user_id).get_all_personal_info()

@router.post("/personal_info", response_model=PersonalInfoSchema)
def create_personal_info(personal_info: PersonalInfoCreate,user_id = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return PersonalInfoService(db, user_id).create_personal_info(personal_info)

@router.put("/personal_info/{branch_id}", response_model=PersonalInfoSchema)
def update_personal_info(personal_info_id: int,  personal_info: PersonalInfoUpdate,user_id = Depends(get_current_user_id), db: Session = Depends(get_db)):
    personal_info_service = PersonalInfoService(db, user_id)
    db_branch = personal_info_service.get_personal_info(personal_info_id)
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return personal_info_service.update_personal_info(personal_info_id, personal_info)

@router.delete("/personal_info/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    personal_info_service = PersonalInfoService(db, user_id)
    db_branch = personal_info_service.get_personal_info(branch_id)
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return personal_info_service.delete_personal_info(branch_id)
