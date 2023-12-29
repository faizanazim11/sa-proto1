from fastapi import APIRouter

from scripts.core.services.auth_services import auth_services

router = APIRouter()
router.include_router(auth_services, prefix="/auth", tags=["Auth"])
