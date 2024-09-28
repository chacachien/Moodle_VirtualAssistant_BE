from fastapi import APIRouter, Depends, HTTPException, Query, Path
from starlette.responses import JSONResponse
from starlette import status
from app.db.db import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.services.chat_service import ChatService
from typing import Annotated
import logging
from app.models.message_model import *
from app.services.auth_service import auth_wrapper
from starlette.requests import Request
from fastapi.responses import StreamingResponse


logger = logging.getLogger()
router = APIRouter()


@router.get("/chat")
async def get_history(
                    chatid: Annotated[int | None, Query()]=None,
                    chat_service: ChatService = Depends(), 
                    session:AsyncSession=Depends(get_session),
                    #user=Depends(auth_wrapper)
                    ):
    # if user == 'fail':
    #     raise HTTPException(status_code=401, detail="Invalid token")

    print("GET HISTORY OF ", chatid)
    history = await chat_service.get_chat_history(chatid, session)
    return history


@router.post("/chat")
async def send_message(
                    message: MessageCreate,
                    chat_service: ChatService = Depends(),
                    session: AsyncSession = Depends(get_session),
                    #user=Depends(auth_wrapper)
                    ):
    response_generator, full_bot_response = await chat_service.send_message(message, session)

    async def streaming_response():
        async for chunk in response_generator:
            yield chunk

        # Once the response is finished, save the full response to the database
        bot_message_content = ''.join(full_bot_response)
        if bot_message_content:
            # Save the bot's message to the database
            bot_message = Message(
                content=bot_message_content,
                chatId=message.chatId,
                role=TypeRoleChoices.BOT,
            )
            session.add(bot_message)
            await session.commit()
            await session.refresh(bot_message)

    # Return the streamed response to the client
    return StreamingResponse(streaming_response(), media_type='text/plain')
    return StreamingResponse(await chat_service.send_message(message, session), media_type='text/plain')
    # if user == 'fail':
    #     raise HTTPException(status_code=401, detail="Invalid token")

    # import time 
    # s = time.time()
    # print("SEND MESSAGE TO ", message)
    # result = await  chat_service.send_message(message, session)
    # print('Answer: ', result)
    # e = time.time()
    # print("ALL TIME: ", e-s)
    # return {"message": result}

@router.delete("/chat/{chatid}")
async def delete_message(
                    chatid: int = Path(..., title="The ID of the chat"),
                    chat_service: ChatService = Depends(),
                    session: AsyncSession = Depends(get_session),
                    user=Depends(auth_wrapper)
                    ):
    if user == 'fail':
        raise HTTPException(status_code=401, detail="Invalid token")

    print("DELETE MESSAGE FROM ", chatid)
    result = await chat_service.delete_message(chatid, session)
    print('Answer: ', result)
    return result


