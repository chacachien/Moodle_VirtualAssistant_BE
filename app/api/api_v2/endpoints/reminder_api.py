from fastapi import Query, APIRouter
from app.chatbot.taskbot.reminder import Reminder
from app.models.reminder_model import RemiderContent, Settime

import pusher

from app.services.chat_service import ChatServiceV2
from app.services.schedule import ReminderService, ReminderServiceV2

pusher_client = pusher.Pusher(
    app_id='1879635',
    key='9de03240cc8a5c22c658',
    secret='b82363250a9736265d17',
    cluster='ap1',
    ssl=True,
)

router = APIRouter()
reminderBot = Reminder()

@router.post("/reminder")
async def get_reminder(reminder: RemiderContent):
    message = ""
    if reminder.name == "daily":
        message = reminderBot.daily_reminder(reminder)
    else:
        message = reminderBot.create_content_reminder(reminder)
    # end create message
    user_id = reminder.user_id
    pusher_client.trigger('moodle-remind', f"{user_id}", {'message': f"{message}"})
    print("Message sent:", message)
    reminderBot.create_reminder_database(reminder.name, reminder.user_id, reminder.time_reminder, message);
    await ChatServiceV2.insert_message("",message, 4, user_id)
    return message


@router.post("/settime")
async def set_time(time: Settime):
    if time.user_id == 2:
        result = await ReminderServiceV2.set_time(time)
    else:
        result = await ReminderServiceV2.set_status_reminder_user(time)
    return result

