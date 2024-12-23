from app.models.base_model import get_default_datetime
from app.models.message_model import *
import os
import json
import asyncpg
from fastapi import HTTPException
from starlette import status
from app.chatbot.model import ChatBot
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import markdown

class ChatServiceV2(object):
    chatbot = ChatBot()

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
    async def send_message(message: MessageCreate, user_role: int):
        try:
            full_bot_response = []
            async def response_generator():
                try:
                    async for chunk in ChatServiceV2.chatbot.get_response(
                        message.content, message.chatId, message.courseId, message.role, user_role
                    ):
                        full_bot_response.append(chunk) #if chunk not in ChatServiceV2.list_text else None
                        yield chunk
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error in generating response: {e}"
                    )

            content = {
                "user": {
                    "message": message.content,
                    "time": get_default_datetime().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Current timestamp
                },
                "bot": {
                    "message": "",
                    "time": get_default_datetime().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],  # Current timestamp
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
            connection.close()

    @staticmethod
    async def insert_message(user_message, bot_message, bot_role, chat_id):

        content = {
            "user": {
                "message": user_message,
                "time": get_default_datetime().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Current timestamp
            },
            "bot": {
                "message": bot_message,
                "time": get_default_datetime().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],  # Current timestamp
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
            ChatServiceV2.chatbot = ChatBot()
            # Return the updated content as a result
            return {"updated_content": updated_content}
        except Exception as e:
            print(f"Error updating bot message: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await connection.close()

    @staticmethod
    async def send_email(user_id, bot_message, subject):
        connection = await ChatServiceV2.get_db_connection()
        try:
            # Execute the SQL query to fetch the chat history
            query = "SELECT email FROM mdl_user WHERE id = $1"
            records = await connection.fetch(query, user_id)

            # Convert the fetched records into a list of dictionaries
            if not records:
                return "User email does not exist"
            recipient_email = records[0]
            print("EMAIL: ", recipient_email)
            # Close the database connection
            sender_email = "chacachiene@gmail.com"
            password = "ivmh xgit bnkm nksf"
            #password = "unxf lrzw eizs wrcn"
            #recipient_email = "phat.nguyennpk1311@hcmut.edu.vn"
            message = MIMEMultipart('alternative')
            message["From"] = sender_email
            #message["To"] = recipient_email
            message["Subject"] = "[Moodle Bot] Daily reminder" if subject =="daily" else "[Moodle Bot] Important event"
            html_content = markdown.markdown(bot_message)
            #message.attach(MIMEText(f"Message: {bot_message}", "plain"))
            message.attach(MIMEText(bot_message, 'plain'))
            message.attach(MIMEText(html_content, 'html'))
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, recipient_email, message.as_string())

            return {"message": "Email sent successfully"}
        except Exception as e:
            print(f"Error sending email: {e}")
            return {"message": "Email sent fail!"}