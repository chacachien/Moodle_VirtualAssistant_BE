from fastapi import Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app.chatbot.taskbot.reminder import Reminder
from app.models.reminder_model import RemiderContent

import pusher

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

    # Template data
    user_id = 1
    content = "A quiz has been added for u."

    # Send to user: DUY
    # Set push event to user here
    pusher_client.trigger('moodle-remind', f"{user_id}", {'message': f"{message}"})

    # End sen to user
    return message
