from fastapi import APIRouter, Depends, Query
from typing import Annotated
import logging
from app.services.auth_service import auth_wrapper, AuthService
from passlib.hash import bcrypt
import hmac
from app.models.base_model import VerifyRequest

logger = logging.getLogger()
router = APIRouter()


def password_verify(password: str, hash: str) -> bool:
    try:
        # Use passlib's bcrypt implementation for verification
        return bcrypt.verify(password, hash)
    except Exception:
        # Fallback to constant-time comparison if hash format is different
        generated = bcrypt.using(rounds=12, ident="2a").hash(password)
        return hmac.compare_digest(hash.encode('utf-8'), generated.encode('utf-8'))



@router.post("/verify")
async def verify_password(request: VerifyRequest):
    is_valid = password_verify(request.password, request.stored_hash)
    return {"verified": is_valid}
@router.get("/token")
async def get_history(
                    userId: Annotated[int | None, Query()]=None,
                    ):

    print("GET TOKEN OF ", userId)
    token = await AuthService.get_token(userId)
    return token
