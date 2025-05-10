from fastapi import APIRouter

from app.api.v1.controllers.auth_controller import router as auth_router

router = APIRouter()
router.include_router(auth_router)
