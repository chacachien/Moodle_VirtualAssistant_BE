from numpy import insert
from app.models.message_model import *
from sqlmodel import select, delete
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
            #res = ChatService.chatbot.get_response(message.content, message.chatId, message.courseId)
            # just test

        # First save the user's message to the database
            user_message = Message(
                content=message.content,
                chatId=message.chatId,
                role=TypeRoleChoices.USER,
            )
            session.add(user_message)
            await session.commit()
            await session.refresh(user_message)

            # To store the complete bot response for saving later
            full_bot_response = []

            async def response_generator():
                try:
                    async for chunk in ChatService.chatbot.get_response(
                        message.content, message.chatId, message.courseId, 1
                    ):
                        # Append each chunk to full_bot_response so that we can save it later
                        full_bot_response.append(chunk)
                        # Stream the chunk

                        yield chunk
                except Exception as e:
                    print(e)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Error in generating response"
                    )

            # Start streaming the response
            return response_generator(), full_bot_response

            # async def response_generator():
            #     async for chunk in ChatService.chatbot.get_response(message.content, message.chatId, message.courseId):
            #         yield chunk
            #     yield "Button here"
            # return response_generator()
        
            # message_obj = Message(
            #     content = message.content,
            #     chatId = message.chatId,
            #     role = TypeRoleChoices.USER,
            # )
            # session.add(message_obj)
            # await session.commit()
            # await session.refresh(message_obj)

            # if res is not None:
            #     message_obj_res = Message(
            #         content= res,
            #         chatId= message.chatId,
            #         role = TypeRoleChoices.BOT,
            #     )
            #     session.add(message_obj_res)
            #     await session.commit()
            #     await session.refresh(message_obj_res)

            #     return res
            # else:
            #     return "Sorry, I don't understand"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

    @staticmethod
    async def delete_message(chatId: int, session: AsyncSession):
        try:
            async with session.begin():
                # Fetch messages to be deleted
                query = select(Message).where(Message.chatId == chatId)
                result = await session.execute(query)
                message_history = result.scalars().all()
                
                if not message_history:
                    return []

                # Add messages to MessageDeleted table
                for message in message_history:
                    message_deleted = MessageDeleted(
                        content=message.content,
                        chatId=message.chatId,
                        role=TypeRoleChoices.USER
                    )
                    session.add(message_deleted)
                
                # Delete messages from Message table
                query = delete(Message).where(Message.chatId == chatId)
                await session.execute(query)
                await session.commit()
            return "Messages deleted successfully"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")