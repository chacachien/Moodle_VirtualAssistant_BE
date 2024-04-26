from app.models.message_model import *
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from starlette import status
from app.chatbot.model import ChatBot


class ChatService(object):
    chatbot = ChatBot()
    __instance = None
    def __init__(self):
        pass
    @staticmethod
    async def get_chat_history(chatId: int, session: AsyncSession):
        try:
            query = select(Message).where(Message.chatId == chatId)
            result = await session.execute(query)
            message_history = result.scalars()
            print("MESSAGE LIST: ", message_history)
            if message_history is None:
                return []

            return message_history.all()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    @staticmethod
    async def send_message(message: MessageCreate, session: AsyncSession):
        try:
            # add message into table
            message_obj = Message(
                content = message.content,
                chatId = message.chatId,
                role = message.role,
            )
            session.add(message_obj)
            await session.commit()
            await session.refresh(message_obj)

            res = ChatService.chatbot.get_response(message.content, message.chatId)
            # add response into table
            if res is not None:
                message_obj_res = Message(
                    content= res,
                    chatId= message.chatId,
                    role ="BOT",
                )
                session.add(message_obj_res)
                await session.commit()
                await session.refresh(message_obj_res)

                return res
            else:
                return "Sorry, I don't understand"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    