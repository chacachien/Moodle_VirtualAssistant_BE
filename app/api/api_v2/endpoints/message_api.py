import re
from http.client import HTTPException

from fastapi import APIRouter, Depends, Query
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
    if user == 0:
        return "Require token to access bot!"

    print("GET HISTORY OF ", chatid)
    history = await ChatServiceV2.get_chat_history(chatid)
    return history


@router.post("/chat")
async def send_message(
                    message: MessageCreate,
                    user=Depends(auth_wrapper)
                    ):
    try:
        if user == 0:
            return "Require token to access bot!"

        response_generator, full_bot_response, message_id = await ChatServiceV2.send_message(message)
        async def streaming_response():
            async for chunk in response_generator:
                yield chunk

            # Once the response is finished, save the full response to the database
            bot_message_content = ''.join(full_bot_response)
            print("BOT_MESSAGE_CONTENT: ", bot_message_content)
            if bot_message_content:
                match = re.search(r"&start&\n(.*)", bot_message_content, re.DOTALL)

                if match:
                    bot_message_content = match.group(1)
                    print(bot_message_content.strip())  # Optional: Use strip() to remove leading/trailing spaces or newlines
                else:
                    print("No match found.")
                await ChatServiceV2.update_bot_message(message_id,message.chatId, bot_message_content)
                # Save the bot's message to the database
        # Return the streamed response to the client
        return StreamingResponse(streaming_response(), media_type='text/plain')
    except Exception as e:
        return "Xin lỗi nhưng bạn có thể đặt lại câu hỏi được không ạ?"

@router.delete("/chat")
async def delete_message(
                    chatid: Annotated[int | None, Query()]=None,
                    user=Depends(auth_wrapper)
                    ):
    if user == 0:
        raise HTTPException(status_code=401, detail="Invalid token")

    print("DELETE MESSAGE FROM ", chatid)
    result = await ChatServiceV2.delete_message(chatid)
    print('Answer: ', result)
    return result


