from fastapi import APIRouter
from api.v1 import auth,personal_info


router = APIRouter()
router.include_router(auth.router, tags=["Authentication"])
router.include_router(personal_info.router, tags=["Personal Info"])
