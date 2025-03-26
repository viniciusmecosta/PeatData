from fastapi.responses import FileResponse
from fastapi import APIRouter
import os

router = APIRouter()


@router.get("/", include_in_schema=False)
def read_root():
    return "Welcome S2!"
