from fastapi import APIRouter

from scripts.core.services.auth_services import auth_services
from scripts.core.services.job_services import job_services
from scripts.core.services.organisation_services import organisation_services

router = APIRouter()
router.include_router(auth_services, prefix="/auth", tags=["Auth"])
router.include_router(organisation_services, prefix="/organisation", tags=["Organisation"])
router.include_router(job_services, prefix="/job", tags=["Job"])
