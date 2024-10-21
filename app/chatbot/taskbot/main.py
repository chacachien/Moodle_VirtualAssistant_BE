from app.core.config import get_url_notsync
from sqlalchemy import create_engine, MetaData, Table, text
from datetime import datetime, timedelta
from app.chatbot.taskbot.reminder import Reminder
from app.services.schedule import ReminderService
from app.services.label_service import LabelService
import json
from datetime import datetime, time
from app.chatbot.ragBot.pgData import LoadData

class TaskHandle():
    def __init__(self):
        super().__init__()
        self.TIME_INTERVAL = 1*60
        DATABASE_URL = get_url_notsync()
        self.engine = create_engine(DATABASE_URL)
        self.reminder = Reminder()
        self.LoadData = LoadData()
        self.time_daily = "7:00"
        self.TIME_REMINDER_BEFORE = 1*24*60*60

    def check_time(self, check_time):
        time_now = datetime.now()
        current_time = int(time_now.timestamp())
        if current_time - check_time > 0 and current_time - check_time <self.TIME_INTERVAL:
            return True
        return False

    # move done
    def check_quiz(self, u_c):
        print("CHECK QUIZ: ", u_c)
        for row in u_c:
            userid = row[0]
            courseid = row[1]
            result = ReminderService.get_quiz(courseid, userid)
            rows = result.fetchall()
            #print("Quiz: ", rows)
            if rows:
                column_names = list(result.keys())
                col_timecreated = column_names.index('timecreated')
                col_timeopen = column_names.index('timeopen')
                col_timeclose = column_names.index('timeclose')
                col_title = column_names.index('name')

                # Iterate over each row
                for row in rows:
                    # Access column value by index
                    time_created = row[col_timecreated]
                    time_open = row[col_timeopen]
                    time_close = row[col_timeclose]
                    title = row[col_title]

                    time_remind = datetime.now() - timedelta(seconds =self.TIME_INTERVAL)

                    if self.check_time(time_created):
                        time_created = datetime.fromtimestamp(time_created)
                        content = self.reminder.create_content_reminder('quiz',title, userid, courseid, 'was created', time_created, time_remind)

                    if self.check_time(time_open):
                        time_open = datetime.fromtimestamp(time_open)
                        content = self.reminder.create_content_reminder('quiz',title, userid, courseid, 'was opened', time_open, time_remind)
                    
                    
                    if self.check_time(time_close - self.TIME_REMINDER_BEFORE):
                        time_close = datetime.fromtimestamp(time_close)
                        time_remind = time_close - timedelta(days = 1)
                        content = self.reminder.create_content_reminder('quiz',title, userid, courseid, 'will close', time_close, time_remind)

    # move done
    def check_assign(self, u_c):
        print("CHECK ASSING: ", u_c)

        for row in u_c:
            userid = row[0]
            courseid = row[1]
            result = ReminderService.get_assign(courseid, userid)
            rows = result.fetchall()
            #print("Assign: ", rows)

            if rows:
                column_names = list(result.keys())

                col_timeopen = column_names.index('allowsubmissionsfromdate')
                col_timeclose = column_names.index('duedate')
                col_title = column_names.index('name')
                # Iterate over each row
                for row in rows:
                    # Access column value by index
                    time_open = row[col_timeopen]
                    time_close = row[col_timeclose]
                    title = row[col_title]
                    #print("Checking row: ", row)

                    time_remind = datetime.now() - timedelta(seconds =self.TIME_INTERVAL)

                    if self.check_time(time_open):
                        time_open = datetime.fromtimestamp(time_open)
                        content = self.reminder.create_content_reminder('assignment',title, userid, courseid, 'allow submissions', time_open, time_remind)
                    
                    time_remind = time_close - self.TIME_REMINDER_BEFORE
                    if self.check_time(time_remind):
                        time_close = datetime.fromtimestamp(time_close)
                        time_remind = time_close - timedelta(days = 1)
                        content = self.reminder.create_content_reminder('assignment',title, userid, courseid, 'due date', time_close, time_remind)
    # move done
    def check_chapter(self, u_c):
        print("CHECK CHAPTER: ", u_c)
        for row in u_c:
            userid = row[0]
            courseid = row[1]
            result = ReminderService.get_chapter(courseid, userid)
            rows = result.fetchall()
            #print("chappter: ", rows)
            if rows:
                column_names = list(result.keys())

                col_timeopen = column_names.index('added')
                col_timemodified = column_names.index('timemodified')
                col_title = column_names.index('name')
                #col_timeclose = column_names.index('duedate')

                # Iterate over each row
                for row in rows:
                    # Access column value by index
                    time_open = row[col_timeopen]
                    title = row[col_title]
                    time_modified = row[col_timemodified]
                    #print("Checking row: ", row)

                    time_remind = datetime.now() - timedelta(seconds =self.TIME_INTERVAL)

                    if self.check_time(time_open):
                        time_open = datetime.fromtimestamp(time_open)
                        content = self.reminder.create_content_reminder('chapter', title, userid, courseid, 'was added', time_open, time_remind)
                    if self.check_time(time_modified):
                        time_modified = datetime.fromtimestamp(time_modified)
                        content = self.reminder.create_content_reminder('chapter', title, userid, courseid, 'was modified', time_modified, time_remind)                       
    




    def check_label_change(self):
        labels = LabelService.get_all_label()
        if labels:
            for row in labels:
                print("time: ", row['timemodified'])
                if self.check_time(row['timemodified']):
                    print('UPLOADING NEW DATA')
                    self.LoadData.update_data(row)
                else:
                    print('old')
    
    def run(self):
        self.check()
        self.check_user_active()
        self.check_label_change()

                
def main():
    taskBot = TaskHandle()
    taskBot.check_label_change()


if __name__ =='__main__':
    main()
