from app.models.reminder_model import *
from app.models.message_model import Message, MessageCreate
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
                    chatId=reminder.chatId,
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
                    c.fullname AS course_name,
                    cm.course AS course_id,
                    mc.name AS module_name,
                    COUNT(cmc.id) AS completed_modules,
                    COUNT(cm.id) AS total_modules,
                    COUNT(cmc.id) / COUNT(cm.id) * 100 AS completion_percentage
                    FROM mdl_user u
                    JOIN mdl_user_enrolments ue ON u.id = ue.userid
                    JOIN mdl_enrol e ON ue.enrolid = e.id
                    JOIN mdl_course c ON e.courseid = c.id
                    JOIN mdl_course_modules cm ON cm.course = c.id
                    JOIN mdl_modules mc ON cm.module = mc.id
                    LEFT JOIN mdl_course_modules_completion cmc ON cm.id = cmc.coursemoduleid AND cmc.userid = u.id
                    WHERE
                        (mc.name = 'quiz' OR mc.name = 'assign' OR mc.name = 'label')
                        AND u.id = :user_id
                    GROUP BY
                        c.fullname, cm.course, mc.name;
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
                    role = message.role
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

