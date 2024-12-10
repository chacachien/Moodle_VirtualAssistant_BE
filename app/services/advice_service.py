from app.models.base_model import get_default_datetime
from app.models.message_model import *
import os
import json
import asyncpg
from fastapi import HTTPException
from starlette import status


class AdviceService(object):
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


    @staticmethod
    async def get_advice_information(user_id: int):
        connection = await AdviceService.get_db_connection()
        try:
            sql = """
                   SELECT 
                   q.name as quiz, 
                   generalfeedback as source,
                   mc.fullname as course_name, 
                   mquiza.sumgrades as quiz_grade,
                   CASE 
                       WHEN rightanswer != responsesummary THEN true 
                       ELSE false 
                   END as is_wrong
                FROM mdl_quiz_attempts mquiza 
                JOIN mdl_question_attempts mquestion ON mquiza.id = mquestion.questionusageid
                JOIN mdl_quiz q ON q.id = mquiza.quiz
                JOIN mdl_question mq ON mq.id = mquestion.questionid
                JOIN mdl_course mc ON mc.id = q.course
                INNER JOIN (
                   SELECT quiz, userid, MAX(sumgrades) as max_grade
                   FROM mdl_quiz_attempts
                   GROUP BY quiz, userid
                ) latest ON mquiza.quiz = latest.quiz AND mquiza.sumgrades = latest.max_grade
                WHERE mquiza.userid = $1
                ORDER BY course, quiz;
                       """
            # Execute the query with the new bot message
            quiz = await connection.fetch(sql, user_id)

            sql = """
                SELECT
    	        a.name AS assignment_name,
    	        mag.grade,
    	        activity as source,
    	        commenttext as teacher_comment,
    	        c.fullname as course_name
    	    FROM
    	        mdl_user u
    	        JOIN mdl_user_enrolments ue ON u.id = ue.userid
    	        JOIN mdl_enrol e ON ue.enrolid = e.id
    	        JOIN mdl_course c ON e.courseid = c.id
    	        JOIN mdl_assign a ON c.id = a.course
    	        join mdl_assign_grades mag on mag.assignment = a.id 
    	        INNER JOIN (
    				    select userid, assignment,  MAX(grade) as max_grade 
    				    FROM mdl_assign_grades 
    				    GROUP BY assignment, userid
    				) latest 
    				ON mag.assignment = latest.assignment 
    				AND mag.grade = latest.max_grade
    	        join mdl_assignfeedback_comments mac on mac.assignment = a.id
    	        LEFT JOIN mdl_assign_submission s ON a.id = s.assignment AND u.id = s.userid
    	    WHERE
    	         s.status = 'submitted' and mag.userid = $1
    	    ORDER by a.duedate;
                """
            assignment = await connection.fetch(sql, user_id)

            # Return the updated content as a result
            return quiz, assignment
        except Exception as e:
            print(f"Error updating bot message: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        finally:
            await connection.close()
