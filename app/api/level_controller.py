from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.auth.token_authenticator import TokenAuthenticator
from app.model.level_request import LevelRequest
from app.model.level_response import LevelResponse
from app.service.level_service import LevelService
from app.core.database import get_db

router = APIRouter()
auth = TokenAuthenticator()


def get_level_service(db: Session = Depends(get_db)) -> LevelService:
    return LevelService(db)


@router.post(
    "/level",
    summary="Adds feeder occupation data",
    description="Submit level data to the database.",
)
async def post_distance(
    data: LevelRequest,
    services: LevelService = Depends(get_level_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    response = services.handle_level(data.level)
    return {
        "message": "Level data received successfully",
        "level": f"{response.level}",
        "date": f"{response.date}",
    }


@router.get(
    "/level",
    summary="Gets feeder occupation data based on query parameters",
    description="Retrieve level data using one of the query parameters: `avg`, `last`, `days`, or `date`.\n\n"
    "Only one parameter should be provided per request.",
)
async def get_level(
    avg: Optional[int] = None,
    last: Optional[int] = None,
    days: Optional[int] = None,
    date: Optional[str] = None,
    services: LevelService = Depends(get_level_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    params_provided = sum(p is not None for p in [avg, last, days, date])

    if params_provided == 0:
        raise HTTPException(
            status_code=400,
            detail="Please provide one query parameter: 'avg', 'last', 'days', or 'date'.",
        )
    if params_provided > 1:
        raise HTTPException(
            status_code=400,
            detail="Please provide only one of the query parameters: 'avg', 'last', 'days', or 'date'.",
        )

    if avg is not None:
        return services.get_last_n_avg_level(avg)
    elif last is not None:
        return services.get_last_n_level_records(last)
    elif days is not None:
        return services.get_level_by_days(days)
    elif date is not None:
        return services.get_level_by_date(date)

    raise HTTPException(
        status_code=500, detail="Internal server error: No valid parameter processed."
    )
