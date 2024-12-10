from fastapi import APIRouter, Depends, Query, Security
from typing import Annotated
import logging
from app.services.auth_service import auth_wrapper, AuthService
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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
    # get stored_hash
    store_hash = await AuthService.get_stored_hash(request.username);
    if not store_hash: return None
    print("P ",store_hash[0])
    is_valid = password_verify(request.password, store_hash[0])
    if not is_valid: return None
    token = await AuthService.get_token(request.username)
    return token

@router.get("/token")
async def get_token(
                    userId: Annotated[int | None, Query()]=None,
                    auth: HTTPAuthorizationCredentials = Security(HTTPBearer())
                    ):
    print("AUTH 2 : ", auth)


    #for test:
    return {
        "token": "832be2bcb454b8a051d0ee870ddf1027"
    }
    # end
    if not auth.credentials: return None
    session = await AuthService.get_session(auth.credentials)
    print("SESSION: ", session)
    if not session: return None
    if session['userid'] != userId: return None
    print("GET TOKEN OF ", userId)
    token = await AuthService.get_token_by_id(userId)
    return token
