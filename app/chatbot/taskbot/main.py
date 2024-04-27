from sympy import re
from app.chatbot.root import RootBot
from app.core.config import get_url_notsync
from sqlalchemy import create_engine, MetaData, Table, text
import datetime
class TaskBot(RootBot):
    def __init__(self):
        super().__init__()
        self.TIME_INTERVAL = 10
        DATABASE_URL = get_url_notsync()
        self.engine = create_engine(DATABASE_URL)

    def get_user_course(self):
        with self.engine.connect() as connection:
            # Execute the query
            
            query = text('''SELECT u.id as user_id, c.id AS course_id
                            FROM mdl_user u
                            JOIN mdl_user_enrolments ue ON u.id = ue.userid
                            JOIN mdl_enrol e ON ue.enrolid = e.id
                            JOIN mdl_course c ON e.courseid = c.id ''')
            result = connection.execute(query)
            # Fetch all rows
            rows = result.fetchall()
            for row in rows:
                print(row)
            return rows
    def check(self):

        # get user and course
        u_c = self.get_user_course()
        time_now = datetime.datetime.now()
        time_now = int(time_now.timestamp())
        for row in u_c:
            with self.engine.connect() as connection:
                # check from noti table
                query = text('''SELECT * FROM mdl_quiz 
                            WHERE course = :course_id 
                            AND timecreated < :current_time 
                            AND timeclose > :current_time
                            AND id NOT IN (
                                SELECT instance FROM mdl_quiz_attempts WHERE userid = :user_id
                            )
                            ''')
                result = connection.execute(
                    query.bindparams(
                        course_id=row[1],
                        current_time=time_now,
                        user_id=row[0]
                    )
                )
                print(result.fetchall())

            # check from assign table


            # check from page table


            # add into reminder table
    def run(self):
        self.check()

def main():
    bot = TaskBot()
    #bot.get_user_course()
    bot.check()

if __name__ == "__main__":
    main()