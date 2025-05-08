from app.api.v1.controllers.user_controller import router as user_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(user_router)
