from fastapi import APIRouter
from app.api import admin_controller, esp_controller, app_controller, notify_controller

router = APIRouter()

router.include_router(esp_controller.router)
router.include_router(app_controller.router)
router.include_router(notify_controller.router)
router.include_router(admin_controller.router)
