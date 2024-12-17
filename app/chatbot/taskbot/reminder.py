from app.core.config import get_url_notsync

from app.models.reminder_model import ReminderCreate, RemiderContent
from app.services.schedule import ReminderService, ReminderServiceV2

from app.chatbot.taskbot.bot import ReminderBot
from app.models.message_model import MessageCreate, TypeRoleChoices


class Reminder:
    def __init__(self):
        self.bot_reminder = ReminderBot()
    
    def create_reminder_database(self, name, user, time_reminder_str, content):
        from datetime import datetime

        # Convert string to datetime
        time_reminder = datetime.strptime(time_reminder_str, "%Y-%m-%d %H:%M:%S")

        reminder_create = ReminderCreate(
                type= name,
                content = content,
                chat_id = user,
                time_remind = time_reminder,
        )

        result = ReminderService.store_reminder(reminder_create)

    async def create_content_reminder(self, reminder: RemiderContent):
        # get user name, get course name
        # username = ReminderService.get_username(user)
        # coursename = ReminderService.get_coursename(course)

        # find the right mod_id
        module = 0
        type = reminder.name
        if reminder.name == "quiz":
            module = 18
            mod_id = await ReminderServiceV2.get_mod_id(reminder.course_id, module, reminder.mod_id)

        elif reminder.name == "assign":
            module = 1
            mod_id = await ReminderServiceV2.get_mod_id(reminder.course_id, module, reminder.mod_id)

        else:
            module =14
            mod_id = reminder.course_id
            type = "chapter"

        #end
        reminder_content =f'''
            User: {reminder.user}
            Type: {type}
            Title: {reminder.title}
            Action: {reminder.type_action}
            Course: {reminder.course}
            At: {str(reminder.time_action)}
        '''
        #reminder_content = "User " + username + " have "+ name+ " " +type_action + " in course "+coursename +" at "+str(time_action)  # Converting time_action to string
        print("reminder content: ", reminder_content)

        reminder_ai = self.bot_reminder.reminder(reminder_content, reminder.name, mod_id)
        print("reminder ai: ", reminder_ai)

        self.create_reminder_database(reminder.name, reminder.user_id, reminder.time_reminder, reminder_ai)
        return reminder_ai

    def daily_reminder(self, reminder: RemiderContent):
        full_content = f"User: {reminder.user}\n" + reminder.title
        print("full_content: ", full_content)
        reminder_ai = self.bot_reminder.reminder_daily(full_content)
        print("remind list", reminder_ai)
        # for m in messages:
        self.create_reminder_database('daily', reminder.user_id, reminder.time_reminder, reminder_ai)
        return reminder_ai


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