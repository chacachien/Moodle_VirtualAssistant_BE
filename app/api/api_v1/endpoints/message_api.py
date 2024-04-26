from fastapi import APIRouter, Depends, HTTPException, Query, Path
from starlette.responses import JSONResponse
from starlette import status
from app.db.db import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.api.api_v1.services.chat_service import ChatService
from typing import Annotated
import logging
from app.models.message_model import *

logger = logging.getLogger()
router = APIRouter()


@router.get("/chat")
async def get_history(
                    chatid: Annotated[int | None, Query()]=None,
                    chat_service: ChatService = Depends(), 
                    session:AsyncSession=Depends(get_session)):
    print("GET HISTORY OF ", chatid)
    history = await chat_service.get_chat_history(chatid, session)
    return history


@router.post("/chat")
async def send_message(
                    message: MessageCreate,
                    chat_service: ChatService = Depends(),
                    session: AsyncSession = Depends(get_session)):
    print("SEND MESSAGE TO ", message)
    result = await chat_service.send_message(message, session)
    print('Answer: ', result)
    return result

@router.delete("/chat/{chatid}")
async def delete_message(
                    chatid: int = Path(..., title="The ID of the chat"),
                    chat_service: ChatService = Depends(),
                    session: AsyncSession = Depends(get_session)):
    print("DELETE MESSAGE FROM ", chatid)
    result = await chat_service.delete_message(chatid, session)
    print('Answer: ', result)
    return result


