from app.core.config import get_url_notsync
from sqlalchemy import create_engine,  MetaData, Table, text
from app.models.reminder_model import ReminderCreate
from app.services.schedule import ReminderService 
from app.models.reminder_model import ReminderCreate
from app.db.db import get_session
from datetime import datetime, timedelta
from app.chatbot.taskbot.bot import ReminderBot
from app.models.message_model import MessageCreate, TypeRoleChoices

class Reminder:
    
    def __init__(self):
        DATABASE_URL = get_url_notsync()
        self.engine = create_engine(DATABASE_URL)
        self.bot_reminder = ReminderBot()
    
    def create_reminder_database(self, name, user, time_reminder, content):
        reminder_create = ReminderCreate(
                type= name,
                content = content,
                chatId = user,
                time_remind = time_reminder
        )

        result = ReminderService.store_reminder(reminder_create)

    
    def create_content_reminder(self, name, title, user, course, type_action, time_action, time_reminder):
        # get user name, get course name
        username = ReminderService.get_username(user)
        coursename = ReminderService.get_coursename(course)
        reminder_content =f'''
            User: {username}
            Type: {name}
            Title: {title}
            Action: {type_action}
            Course: {coursename}
            At: {str(time_action)}
        '''
        #reminder_content = "User " + username + " have "+ name+ " " +type_action + " in course "+coursename +" at "+str(time_action)  # Converting time_action to string
        print("reminder content: ", reminder_content)

        reminder_ai = self.bot_reminder.reminder(reminder_content)
        print("reminder ai: ", reminder_ai)

        self.create_reminder_database(name, user, time_reminder, reminder_ai)
        return reminder_content

    def daily_reminder(self, user, list_content, time_reminder):
        username = ReminderService.get_username(user)
        full_content = f"User: {username}\n" + list_content
        reminder_ai = self.bot_reminder.reminder_daily(full_content)
        messages = reminder_ai
        #messages = reminder_ai.split("\n\n")

        print("remind list", messages)
        # for m in messages:
        self.create_reminder_database('daily', user, time_reminder, messages)


    def remind_user(self, userid):
        result = ReminderService.get_message_reminder(userid)
        rows = result.fetchall()
        print("remind message: ", rows)
        if rows:
            column_names = list(result.keys())
            col_content = column_names.index('content')
            col_userid = column_names.index('chatId')
            col_time_remind = column_names.index('time_remind')
            col_id = column_names.index('id')
            for row in rows:
                content = row[col_content]
                user_id = row[col_userid]
                time_remind = row[col_time_remind]
                reminder_id = row[col_id]
                # send remind if user online
                self.send_message(user_id, content)
                # update is_remind
                print(f"Update reminder: {reminder_id}, user: {user_id} ")
                update_res = ReminderService.update_message_reminder(user_id,reminder_id)
                print(update_res)

    def send_message(self, userid, content):
        message_obj = MessageCreate(
            chatId = userid,
            content = content,
            role = TypeRoleChoices.BOT,
            courseId = -1
        )
        result = ReminderService.send_message(message_obj)
        print(result)
        print(f"send to user {userid}: {content}")

 
def main():
    time_action = datetime.now()
    time_remind = datetime.now() + timedelta(seconds=10) 
    reminder = Reminder()
    content = reminder.create_content_reminder('quiz', 1, 2, 'open', time_action, time_remind)

if __name__ =='__main__':
    main()