from app.api.v1.controllers.auth_controller import router as auth_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(auth_router)
