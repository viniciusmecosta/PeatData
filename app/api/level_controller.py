from typing import List
from fastapi import APIRouter, Depends
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


@router.post("/level")
async def post_distance(
    data: LevelRequest,
    services=Depends(get_level_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Submit level data.

    **Request body**:
    - `level`: Level value.

    **Example request**:
    ```json
    {
      "level": 5.0
    }
    ```

    **Example response**:
    ```json
    {
      "message": "Level data received successfully",
      "level": "78.0",
      "date": "2025-04-11 09:46:52.799926"
    }
    ```
    """
    response = services.handle_level(data.level)
    return {
        "message": "Level data received successfully",
        "level": f"{response.level}",
        "date": f"{response.date}",
    }


@router.get("/level/avg/{n}")
async def get_last_avg_level(
    n: int,
    services=Depends(get_level_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Get the average level for the past N days.

    **Request**:
    - `n`: Number of days for average calculation.

    **Example response**:
    ```json
    [
      {
        "date": "18/03",
        "level": 5.0
      },
      {
        "date": "17/03",
        "level": 4.8
      }
    ]
    ```
    """
    return services.get_last_n_avg_level(n)


@router.get("/level/last/{n}", response_model=List[LevelResponse])
async def get_last_n_level_data(
    n: int,
    services=Depends(get_level_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Get the last N level records, ordered by date.

    **Request**:
    - `n`: Number of latest level records.

    **Example response**:
    ```json
    [
      {
        "date": "2025-03-11T10:20:30Z",
        "level": 5.0
      },
      {
        "date": "2025-03-10T10:20:30Z",
        "level": 4.9
      }
    ]
    ```
    """
    return services.get_last_n_level_records(n)


@router.get("/level/days/{days}", response_model=List[LevelResponse])
async def get_level_days(
    days: int,
    services=Depends(get_level_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Get level data for the past X days.

    **Request**:
    - `days`: Number of days to look back.

    **Example response**:
    ```json
    [
      {
        "date": "2025-03-11T10:20:30Z",
        "level": 5.0
      },
      {
        "date": "2025-03-10T10:20:30Z",
        "level": 4.9
      }
    ]
    ```
    """
    return services.get_level_by_days(days)


@router.get("/level/date/{date}", response_model=List[LevelResponse])
async def get_level_date(
    date: str,
    services=Depends(get_level_service),
    credentials: HTTPAuthorizationCredentials = Depends(auth.verify_token),
):
    """
    Get level data for a specific date.

    **Request**:
    - `date`: Date in `DDMMYYYY` format.

    **Example response**:
    ```json
    [
      {
        "date": "10:20",
        "level": 5.0
      }
    ]
    ```
    """
    return services.get_level_by_date(date)
