from sqlalchemy import false

from app.models.message_model import *
import os
from datetime import datetime
import json


# class ChatService(object):
#     chatbot = ChatBot()
#     __instance = None
#     def __init__(self):
#         pass
#     @staticmethod
#     async def get_chat_history(chatId: int, session: AsyncSession):
#         try:
#             query = select(Message).where(Message.chatId == chatId)
#             result = await session.execute(query)
#             message_history = result.scalars()
#             print("MESSAGE LIST: ", message_history)
#             if message_history is None:
#                 return []
#             return message_history.all()
#         except Exception as e:
#             print(e)
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
#
#     @staticmethod
#     async def send_message(message: MessageCreate, session: AsyncSession):
#         try:
#             # add message into table
#             #res = ChatService.chatbot.get_response(message.content, message.chatId, message.courseId)
#             # just test
#
#         # First save the user's message to the database
#             user_message = Message(
#                 content=message.content,
#                 chatId=message.chatId,
#                 role=TypeRoleChoices.USER,
#             )
#             session.add(user_message)
#             await session.commit()
#             await session.refresh(user_message)
#
#             # To store the complete bot response for saving later
#             full_bot_response = []
#
#             async def response_generator():
#                 try:
#                     async for chunk in ChatService.chatbot.get_response(
#                         message.content, message.chatId, message.courseId, 1
#                     ):
#                         # Append each chunk to full_bot_response so that we can save it later
#                         full_bot_response.append(chunk)
#                         # Stream the chunk
#
#                         yield chunk
#                 except Exception as e:
#                     print(e)
#                     raise HTTPException(
#                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                         detail="Error in generating response"
#                     )
#
#             # Start streaming the response
#             return response_generator(), full_bot_response
#
#             # async def response_generator():
#             #     async for chunk in ChatService.chatbot.get_response(message.content, message.chatId, message.courseId):
#             #         yield chunk
#             #     yield "Button here"
#             # return response_generator()
#
#             # message_obj = Message(
#             #     content = message.content,
#             #     chatId = message.chatId,
#             #     role = TypeRoleChoices.USER,
#             # )
#             # session.add(message_obj)
#             # await session.commit()
#             # await session.refresh(message_obj)
#
#             # if res is not None:
#             #     message_obj_res = Message(
#             #         content= res,
#             #         chatId= message.chatId,
#             #         role = TypeRoleChoices.BOT,
#             #     )
#             #     session.add(message_obj_res)
#             #     await session.commit()
#             #     await session.refresh(message_obj_res)
#
#             #     return res
#             # else:
#             #     return "Sorry, I don't understand"
#         except Exception as e:
#             print(e)
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
#
#
#     @staticmethod
#     async def delete_message(chatId: int, session: AsyncSession):
#         try:
#             async with session.begin():
#                 # Fetch messages to be deleted
#                 query = select(Message).where(Message.chatId == chatId)
#                 result = await session.execute(query)
#                 message_history = result.scalars().all()
#
#                 if not message_history:
#                     return []
#
#                 # Add messages to MessageDeleted table
#                 for message in message_history:
#                     message_deleted = MessageDeleted(
#                         content=message.content,
#                         chatId=message.chatId,
#                         role=TypeRoleChoices.USER
#                     )
#                     session.add(message_deleted)
#
#                 # Delete messages from Message table
#                 query = delete(Message).where(Message.chatId == chatId)
#                 await session.execute(query)
#                 await session.commit()
#             return "Messages deleted successfully"
#         except Exception as e:
#             print(e)
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
#

import asyncpg
from fastapi import HTTPException
from starlette import status
from app.chatbot.model import ChatBot


class ChatServiceV2(object):
    chatbot = ChatBot()
    list_text = ["Tìm kiếm thông tin\n", "Phân tích tài liệu\n", "Nội dung sẳn sàng\n", "&start&", 'Bạn chịu khó đợi một tí nhé!', 'Thông tin đang được xử lý rồi!']

    def __init__(self):
        pass

    # Function to create a connection to the database
    @staticmethod
    async def get_db_connection():
        try:
            # Adjust the database connection settings accordingly

            connection = await asyncpg.connect(
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                database=os.getenv("POSTGRES_DB"),
                host=os.getenv("POSTGRES_SERVER"),
                port=os.getenv("POSTGRES_PORT")
            )
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection error")

    # Function to close the connection
    @staticmethod
    async def close_db_connection(connection):
        try:
            await connection.close()
        except Exception as e:
            print(f"Error closing the database connection: {e}")

    # Function to get chat history without ORM
    @staticmethod
    async def get_chat_history(chatId: int):
        connection = await ChatServiceV2.get_db_connection()
        try:
            # Execute the SQL query to fetch the chat history
            query = "SELECT * FROM message_bot WHERE chat_id = $1 Order By id"
            records = await connection.fetch(query, chatId)

            # Convert the fetched records into a list of dictionaries
            message_history = [dict(record) for record in records]

            if not message_history:
                return []
            return message_history
        except Exception as e:
            print(f"Error fetching chat history: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            # Close the database connection
            await ChatServiceV2.close_db_connection(connection)

    @staticmethod
    async def update_bot_message(message_id, chat_id: int, new_message: str):
        connection = await ChatServiceV2.get_db_connection()
        try:
            # SQL query to update the bot's message
            sql = """
                UPDATE message_bot
                SET content = jsonb_set(content, '{bot,message}', $2::jsonb, false)
                WHERE chat_id = $1 and id =$3
                RETURNING content;
            """

            # Execute the query with the new bot message
            updated_content = await connection.fetchval(sql, chat_id, json.dumps(new_message), message_id)

            # Return the updated content as a result
            return {"updated_content": updated_content}
        except Exception as e:
            print(f"Error updating bot message: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await connection.close()

    @staticmethod
    async def send_message(message: MessageCreate):
        try:
            full_bot_response = []
            async def response_generator():
                try:
                    i = 0
                    async for chunk in ChatServiceV2.chatbot.get_response(
                        message.content, message.chatId, message.courseId, message.role
                    ):
                        # Append each chunk to full_bot_response so that we can save it later
                        full_bot_response.append(chunk) if chunk not in ChatServiceV2.list_text else None
                        yield chunk
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error in generating response: {e}"
                    )

            content = {
                "user": {
                    "message": message.content,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Current timestamp
                },
                "bot": {
                    "message": "",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],  # Current timestamp
                    "role": message.role
                }
            }
            content_json = json.dumps(content)
            sql = """
                INSERT INTO message_bot (chat_id, content)
                VALUES ($1, $2)
                RETURNING id;
                """
            connection = await ChatServiceV2.get_db_connection()
            if connection is None: return None, None, None
            message_id = await connection.fetchval(sql,message.chatId, content_json)
            return response_generator(), full_bot_response, message_id

        except Exception as e:
            print(f"Error inserting message: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            # Close the database connection
            await ChatServiceV2.close_db_connection(connection)

    @staticmethod
    async def insert_message(user_message, bot_message, bot_role, chat_id):

        content = {
            "user": {
                "message": user_message,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Current timestamp
            },
            "bot": {
                "message": bot_message,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],  # Current timestamp
                "role": bot_role
            }
        }
        content_json = json.dumps(content)

        sql = """
            INSERT INTO message_bot (chat_id, content)
            VALUES ($1, $2)
            RETURNING id;
            """
        connection = await ChatServiceV2.get_db_connection()
        if connection is None: return None

        message_id = await connection.fetchval(sql,chat_id, content_json)

        return message_id


    @staticmethod
    async def delete_message(chat_id: int):
        connection = await ChatServiceV2.get_db_connection()
        try:
            # SQL query to update the bot's message
            sql = """
                       DELETE FROM message_bot
                       WHERE chat_id = $1;
                   """

            # Execute the query with the new bot message
            updated_content = await connection.execute(sql, chat_id)

            # Return the updated content as a result
            return {"updated_content": updated_content}
        except Exception as e:
            print(f"Error updating bot message: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await connection.close()
        # try:
        #     async with session.begin():
        #         # Fetch messages to be deleted
        #         query = select(Message).where(Message.chatId == chatId)
        #         result = await session.execute(query)
        #         message_history = result.scalars().all()
        #
        #         if not message_history:
        #             return []
        #
        #         # Add messages to MessageDeleted table
        #         for message in message_history:
        #             message_deleted = MessageDeleted(
        #                 content=message.content,
        #                 chatId=message.chatId,
        #                 role=TypeRoleChoices.USER
        #             )
        #             session.add(message_deleted)
        #
        #         # Delete messages from Message table
        #         query = delete(Message).where(Message.chatId == chatId)
        #         await session.execute(query)
        #         await session.commit()
        #     return "Messages deleted successfully"
        # except Exception as e:
        #     print(e)
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        #
