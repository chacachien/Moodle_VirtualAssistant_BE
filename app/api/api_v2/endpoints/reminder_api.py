from fastapi import Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app.chatbot.taskbot.reminder import Reminder
from app.models.reminder_model import RemiderContent

router = APIRouter()

reminderBot = Reminder()
@router.post("/reminder")
async def get_reminder(reminder: RemiderContent ):
    #user =auth_wrapper(3)  # Passing chatId to the auth wrapper
    # if user == 0:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    #### Create the message: Phat
    #message = reminderBot.create_content_reminder(reminder)

    ### end create message

    ### Template data
    user_id = 1
    content = "A quiz has been added for u."

    ### Send to user: DUY
        ### Set push event to user here


    ### End sen to user
    return message