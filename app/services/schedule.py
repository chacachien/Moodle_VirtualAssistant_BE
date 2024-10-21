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
    def get_user_course():
        try:
            with ReminderService.engine.connect() as connection:
                # Execute the query
                query = text('''
                                SELECT u.id as user_id, c.id AS course_id
                                FROM mdl_user u
                                JOIN mdl_user_enrolments ue ON u.id = ue.userid
                                JOIN mdl_enrol e ON ue.enrolid = e.id
                                JOIN mdl_course c ON e.courseid = c.id
                                 ''')
                result = connection.execute(query)
                return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    @staticmethod
    def get_user_daily_check():
        try:
            with ReminderService.engine.connect() as connection:
                # Execute the query
                query = text('''
                    SELECT DISTINCT u.id as user_id
                    FROM mdl_user u
                    JOIN mdl_user_enrolments ue ON u.id = ue.userid
                    JOIN mdl_enrol e ON ue.enrolid = e.id
                    JOIN mdl_course c ON e.courseid = c.id 
                                 ''')
                result = connection.execute(query)
                return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    @staticmethod
    def get_quiz(courseid, userid):
        try:
            with ReminderService.engine.connect() as connection:
                query = text('''
                    SELECT q.*
                    FROM mdl_quiz q
                    LEFT JOIN mdl_quiz_attempts qa ON q.id = qa.quiz AND qa.userid = :user_id
                    WHERE q.course = :course_id
                    AND (qa.state IS NULL OR qa.state != 'finished')
                    ''')

                result = connection.execute(
                    query.bindparams(
                        course_id=courseid,
                        user_id = userid,
                    )
                )
               
                return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    @staticmethod
    def get_assign(courseid, userid):
        try:
            with ReminderService.engine.connect() as connection:
                query = text('''
                    SELECT a.*
                    FROM mdl_assign a
                    LEFT JOIN mdl_assign_submission a_s ON a.id = a_s.assignment AND a_s.userid = :user_id
                    WHERE a.course = :course_id
                    AND (a_s.status IS NULL OR a_s.status != 'submitted')
                    ''')

                result = connection.execute(
                    query.bindparams(
                        course_id=courseid,
                        user_id = userid,
                    )
                )
                return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    @staticmethod
    def get_chapter(courseid, userid):
        try:
            with ReminderService.engine.connect() as connection:
                query = text("""
                    SELECT *
                    FROM mdl_label l
                    LEFT JOIN mdl_course_modules cm ON cm.instance = l.id
                    LEFT JOIN mdl_course_modules_completion cmc ON cm.id = cmc.coursemoduleid AND cmc.userid = :user_id
                    WHERE cm.module = 13
                    AND l.course = :course_id
                    AND (cmc.userid IS NULL OR cmc.completionstate != 1);

                    """)
                result = connection.execute(
                    query.bindparams(
                        course_id=courseid,
                        user_id = userid,
                    )
                )
                return result
            
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    @staticmethod
    def get_completion(userid):
        try:
            with ReminderService.engine.connect() as connection:
                query = text("""
                    SELECT 
                    	c.fullname,
                        cm.course AS course_id,
                        mc.name AS module_name,
                        COUNT(cmc.id) AS completed_modules,
                        COUNT(cm.id) AS total_modules,
                        COUNT(cmc.id) / COUNT(cm.id) * 100 AS completion_percentage
                    FROM 
                        mdl_course_modules cm
                    JOIN 
                        mdl_modules mc ON cm.module = mc.id
                    LEFT JOIN 
                        mdl_course_modules_completion cmc ON cm.id = cmc.coursemoduleid AND cmc.userid = :user_id
                    JOIN mdl_course c on c.id = cm.course
                    WHERE mc.name = 'quiz' or mc.name = 'assign' or mc.name = 'label'
                    GROUP BY 
                        cm.course, mc.name;
                """)
                result = connection.execute(
                    query.bindparams(
                        user_id = userid,
                    )
                )
                return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    @staticmethod
    def get_message_reminder(userid):
        try:
            current_time = datetime.now()
            #current_time = int(time_now.timestamp())

            with ReminderService.engine.connect() as connection:
                query = text("""
                    SELECT *
                    FROM messages_reminders_chatbot
                    WHERE 
                        time_remind < :current_time
                        AND is_remind = 0
                        AND chatId = :userid;
                """)

                result = connection.execute(
                        query.bindparams(
                            current_time=current_time,
                            userid = userid
                        )
                    )
                return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    @staticmethod
    def get_user_active(interval):
        try:
            time_now = datetime.now()
            current_time = int(time_now.timestamp())
            with ReminderService.engine.connect() as connection:
                query = text("""
                    SELECT id
                    FROM mdl_user
                    WHERE 
                        :current_time > lastaccess
                        AND (:current_time - lastaccess) < :interval
                """)

                result = connection.execute(
                        query.bindparams(
                            current_time=current_time,
                            interval=interval
                        )
                    )
                return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    @staticmethod
    def update_message_reminder(userid, reminderid):
        try:
            with ReminderService.engine.connect() as connection:
                query = text("""
                    UPDATE messages_reminders_chatbot
                    SET is_remind = 1
                    WHERE 
                        id = :reminderid
                        AND is_remind = 0;
                """)

                result = connection.execute(
                    query.bindparams(
                        reminderid=reminderid
                    )
                )
                connection.commit()
                return result

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
    def get_username(userid):
        try:
            with ReminderService.engine.connect() as connection:
                query = text("SELECT firstname, lastname FROM mdl_user where id = :id")
                result = connection.execute(
                        query.bindparams(
                            id = userid
                        )
                    )
                rows = result.fetchall()
                username = " ".join(rows[0])
                return username
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
                query = text("""
                    DELETE FROM service_setting 
                    WHERE name = 'time_reminder'
                """)

                result = await connection.execute(query)

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
            result = await connection.execute(query, time.user_id, time.status==1)
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

