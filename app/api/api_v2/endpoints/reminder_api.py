from fastapi import Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app.chatbot.taskbot.reminder import Reminder
from app.models.reminder_model import RemiderContent

import pusher

from app.services.chat_service import ChatServiceV2

pusher_client = pusher.Pusher(
    app_id='1879635',
    key='9de03240cc8a5c22c658',
    secret='b82363250a9736265d17',
    cluster='ap1',
    ssl=True
)

router = APIRouter()

reminderBot = Reminder()


@router.post("/reminder")
async def get_reminder(reminder: RemiderContent):
    # user =auth_wrapper(3)  # Passing chatId to the auth wrapper
    # if user == 0:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    # Create the message: Phat
    message = reminderBot.create_content_reminder(reminder)
    # end create message
    user_id = reminder.user_id
    pusher_client.trigger('moodle-remind', f"{user_id}", {'message': f"{message}"})

    reminderBot.create_reminder_database(reminder.name, reminder.user_id, reminder.time_reminder, message);
    await ChatServiceV2.insert_message("",message, 4, user_id)

    return message
