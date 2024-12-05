import os
import asyncpg
from app.models.reminder_model import *
from app.models.message_model import MessageCreate, TypeRoleChoices
from sqlmodel import select, delete, insert
from fastapi import HTTPException
from starlette import status
from app.core.config import get_url_notsync
from sqlalchemy import create_engine, MetaData, Table, text

DATABASE_URL = get_url_notsync()
class ReminderService(object):
    __instance = None
    engine = create_engine(DATABASE_URL)
    def __init__(self):
        pass

    @staticmethod
    def store_reminder(reminder: ReminderCreate):
        try:
            with ReminderService.engine.connect() as connection:
                query = insert(Reminder).values(
                    type=reminder.type,
                    content=reminder.content,
                    chat_id=reminder.chat_id,
                    time_remind=reminder.time_remind
                )
                connection.execute(
                    query
                )
                connection.commit()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    @staticmethod
    def send_message(message: MessageCreate):
        try:
            with ReminderService.engine.connect() as connection:
                query = insert(Message).values(
                    chatId = message.chatId,
                    content = message.content,
                    role = TypeRoleChoices.USER
                )
                res = connection.execute(
                    query
                )
                connection.commit()
                return res

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

    @staticmethod
    def get_coursename(courseid):
        try:
            with ReminderService.engine.connect() as connection:
                query = text("SELECT fullname FROM mdl_course where id = :id")
                result = connection.execute(
                        query.bindparams(
                            id = courseid
                        )
                    )
                rows = result.fetchall()
                coursename = rows[0][0]
                return coursename
                
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

class ReminderServiceV2(object):
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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database connection error")

    @staticmethod
    async def set_time(time: Settime):
        connection = await ReminderServiceV2.get_db_connection()
        try:
            if time.status == 1:
                query = """
                    INSERT INTO service_setting (name, value) 
                    VALUES ($1, $2)
                    ON CONFLICT (name) 
                    DO UPDATE SET value = EXCLUDED.value;
                """
                result = await connection.execute(query, 'time_reminder', time.time)
                return result
            else:
                query = """
                    DELETE FROM service_setting 
                    WHERE name = 'time_reminder'
                """

                result = await connection.execute(query)
                print(result)
                return result
            return "Settime success"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await ReminderServiceV2.close_db_connection(connection)


    @staticmethod
    async def set_status_reminder_user(time: Settime):
        connection = await ReminderServiceV2.get_db_connection()
        try:
            query = """
                        INSERT INTO user_reminder (user_id, reminder)
                        VALUES ($1, $2)
                        ON CONFLICT (user_id)
                        DO UPDATE SET reminder = EXCLUDED.reminder;
                    """
            result = await connection.execute(query, time.userId, time.status==1)
            return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await ReminderServiceV2.close_db_connection(connection)


    @staticmethod
    async def close_db_connection(connection):
        try:
            await connection.close()
        except Exception as e:
            print(f"Error closing the database connection: {e}")

    @staticmethod
    async def get_time():
        connection = await ReminderServiceV2.get_db_connection()
        try:
            query = """
                SELECT value FROM service_setting WHERE name = 'time_reminder'
            """
            result = await connection.fetchrow(query)
            return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await ReminderServiceV2.close_db_connection(connection)

    @staticmethod
    async def get_is_remind(user_id: int):
        connection = await ReminderServiceV2.get_db_connection()
        try:
            query = """
                SELECT reminder FROM user_reminder WHERE user_id = $1
            """
            result = await connection.fetchrow(query, user_id)
            if not result: return False
            return result["reminder"]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await ReminderServiceV2.close_db_connection(connection)

    @staticmethod
    async def get_mod_id(course: int, module: int, instance: int):
        connection = await ReminderServiceV2.get_db_connection()
        try:
            query = """
                select id from mdl_course_modules where course = $1 and module = $2 and instance = $3            
            """
            result = await connection.fetchrow(query, course, module, instance)
            if not result: return 0
            print("RESULT: ", result)
            return result["id"]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await ReminderServiceV2.close_db_connection(connection)