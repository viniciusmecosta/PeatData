from fastapi import APIRouter
from app.api import (
    admin_controller,
    email_controller,
    level_controller,
    phone_controller,
    root_contoller,
    temp_humi_controller,
)

router = APIRouter()

router.include_router(root_contoller.router)

router.include_router(temp_humi_controller.router, tags=["Temp-Humi"])
router.include_router(level_controller.router, tags=["Level"])
router.include_router(phone_controller.router, tags=["Phone"])
router.include_router(email_controller.router, tags=["Email"])
router.include_router(admin_controller.router, tags=["Admin"])
