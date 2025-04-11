from fastapi.responses import FileResponse
from fastapi import APIRouter
import os

router = APIRouter()

favicon_path = "assets/favicon.ico"


@router.get("/", include_in_schema=False)
def read_root():
    return "Welcome S2!"


@router.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    else:
        return {"detail": "Favicon not found"}
