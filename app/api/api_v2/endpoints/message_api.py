from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from starlette import status
from app.db.db import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
#from app.services.chat_service import ChatService
from typing import Annotated
import logging
from app.models.message_model import *
from app.services.auth_service import auth_wrapper, auth_wrapper_lamda
from starlette.requests import Request
from fastapi.responses import StreamingResponse

from app.services.chat_service import ChatServiceV2

logger = logging.getLogger()
router = APIRouter()


@router.get("/chat")
async def get_history(
                    chatid: Annotated[int | None, Query()]=None,
                    #chat_service: ChatService = Depends(),
                    session:AsyncSession=Depends(get_session),
                    user = Depends(auth_wrapper)
                    ):
    #user =auth_wrapper(3)  # Passing chatId to the auth wrapper

    if user == 0:
        raise HTTPException(status_code=401, detail="Invalid token")

    print("GET HISTORY OF ", chatid)
    history = await ChatServiceV2.get_chat_history(chatid)
    return history


@router.post("/chat")
async def send_message(
                    message: MessageCreate,
                    #chat_service: ChatService = Depends(),
                    session: AsyncSession = Depends(get_session),
                    #user=Depends(auth_wrapper)
                    ):
    # if user == 0:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    response_generator, full_bot_response, message_id = await ChatServiceV2.send_message(message)
    async def streaming_response():
        async for chunk in response_generator:
            yield chunk

        # Once the response is finished, save the full response to the database
        bot_message_content = ''.join(full_bot_response)
        if bot_message_content:
            await ChatServiceV2.update_bot_message(message_id,message.chatId, bot_message_content)
            # Save the bot's message to the database


    # Return the streamed response to the client
    return StreamingResponse(streaming_response(), media_type='text/plain')


@router.delete("/chat")
async def delete_message(
                    chatid: Annotated[int | None, Query()]=None,
                    #chat_service: ChatService = Depends(),
                    session: AsyncSession = Depends(get_session),
                    #user=Depends(auth_wrapper)
                    ):
    # if user == 'fail':
    #     raise HTTPException(status_code=401, detail="Invalid token")

    print("DELETE MESSAGE FROM ", chatid)
    result = await ChatServiceV2.delete_message(chatid, session)
    print('Answer: ', result)
    return result


