from fastapi import APIRouter, Depends, Query
from typing import Annotated
import logging
from app.services.auth_service import auth_wrapper, AuthService

logger = logging.getLogger()
router = APIRouter()


@router.get("/token")
async def get_history(
                    userId: Annotated[int | None, Query()]=None,
                    ):

    print("GET TOKEN OF ", userId)
    token = await AuthService.get_token(userId)
    return token
