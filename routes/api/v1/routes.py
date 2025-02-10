from fastapi import APIRouter
from settings import settings
from .endpoints import (
    checkphish,
    virus_total
)

router = APIRouter(
    prefix=settings.api_version,
)

router.include_router(checkphish.router)
router.include_router(virus_total.router)
