from fastapi import APIRouter

from app.api.v1.controllers.user_controller import router as user_router

router = APIRouter()
router.include_router(user_router)
