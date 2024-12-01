import re
from http.client import HTTPException

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.db.db import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

from typing import Annotated
import logging
from app.models.message_model import *
from app.services.auth_service import auth_wrapper
from fastapi.responses import StreamingResponse

from app.services.chat_service import ChatServiceV2

logger = logging.getLogger()
router = APIRouter()


@router.get("/chat")
async def get_history(
                    chatid: Annotated[int | None, Query()]=None,
                    user = Depends(auth_wrapper)
                    ):
    print("GET HISTORY OF ", chatid)
    history = await ChatServiceV2.get_chat_history(chatid)
    return history

@router.post("/chat")
async def send_message(
                    message: MessageCreate,
                    user=Depends(auth_wrapper)
                    ):
    print("VIP: ", user)
    if user != message.chatId:
        raise HTTPException(status.HTTP_409_CONFLICT)
    response_generator, full_bot_response, message_id = await ChatServiceV2.send_message(message, user)
    async def streaming_response():
        try:
            async for chunk in response_generator:
                yield chunk
            # Once the response is finished, save the full response to the database
            bot_message_content = ''.join(full_bot_response)
            await ChatServiceV2.update_bot_message(message_id,message.chatId, bot_message_content)
        except Exception as e:
            print(e)
            yield "Xin lỗi nhưng bạn có thể đặt lại câu hỏi được không ạ?"
    return StreamingResponse(streaming_response(), media_type='text/plain')

@router.delete("/chat")
async def delete_message(
                    chatid: Annotated[int | None, Query()]=None,
                    user=Depends(auth_wrapper)
                    ):
    if user != chatid:
        raise HTTPException(status.HTTP_409_CONFLICT)
    result = await ChatServiceV2.delete_message(chatid)
    print('Answer: ', result)
    return result


