from app.api.v1.routes.auth_routes import router as auth_router
from app.api.v1.routes.user_routes import router as user_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
