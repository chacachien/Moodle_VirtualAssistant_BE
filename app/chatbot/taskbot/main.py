from sympy import re
from app.chatbot.root import RootBot
from app.core.config import get_url_notsync
from sqlalchemy import create_engine, MetaData, Table, text
import datetime
class TaskBot(RootBot):
    def __init__(self):
        super().__init__()
        self.TIME_INTERVAL = 10*60
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

            return rows

    def check_time(self, check_time):
        time_now = datetime.datetime.now()
        current_time = int(time_now.timestamp())
        if current_time - check_time > 0 and current_time - check_time <self.TIME_INTERVAL:
            return True
        return False


    def check_quiz(self, u_c):
        for row in u_c:
            with self.engine.connect() as connection:

                query = text('''
                    SELECT q.*
                    FROM mdl_quiz q
                    LEFT JOIN mdl_quiz_attempts qa ON q.id = qa.quiz AND qa.userid = :user_id
                    WHERE q.course = :course_id
                    AND (qa.state IS NULL OR qa.state != 'finished')
                ''')


                result = connection.execute(
                    query.bindparams(
                        course_id=row[1],
                        #current_time=time_now,
                        user_id = row[0],
                        #interval = self.TIME_INTERVAL
                    )
                )
                rows = result.fetchall()
                # check quiz create, open, close

                if rows:
                    # # Iterate over each row
                    column_names = list(result.keys())
                    col_timecreated = column_names.index('timecreated')
                    col_timeopen = column_names.index('timeopen')
                    col_timeclose = column_names.index('timeclose')


                    # Iterate over each row
                    for row in rows:
                        # Access column value by index
                        time_created = row[col_timecreated]
                        time_open = row[col_timeopen]
                        time_close = row[col_timeclose]
                        print("Checking row: ", row)
                        if self.check_time(time_created):
                            print("Quiz ... in course ... is created ")

                        if self.check_time(time_open):
                            print("QUiz ... in course ... is open")

                        if self.check_time(time_close):
                            print('Quiz ... in course ... is due')


                
    def check_assign(self, u_c):
        

    def check(self):

        # get user and course
        u_c = self.get_user_course()

        # check quiz table
        self.check_quiz(u_c)
        
                
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