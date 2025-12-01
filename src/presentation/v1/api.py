from fastapi import APIRouter

from .controller import (
    auth_controller,
    user_controller,
    banner_controller,
    legal_controller
)

api_router = APIRouter()

api_router.include_router(auth_controller.router)
api_router.include_router(user_controller.router)
api_router.include_router(banner_controller.router)
api_router.include_router(legal_controller.router)
