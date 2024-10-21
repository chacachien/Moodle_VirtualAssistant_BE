from enum import Enum
from app.models.base_model import TimestampModel
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


# class ReminderType(Enum):
#     QUIZ = 'quiz'
#     ASSIGNMENT = 'assignment'
#     CHAPTER = 'chapter'

class ReminderBase(SQLModel):
    type: str
    content: str
    chat_id: int
    time_remind: datetime = Field(default=None)
    is_remind: bool = Field(default=False)
    
class ReminderCreate(ReminderBase):
    pass

class Settime(SQLModel):
    status: int
    time: str
    user_id: int

class RemiderContent(SQLModel):
    name:str
    title:str
    user_id: int
    user: str
    course_id:int
    course: str
    type_action:str
    time_action: str
    time_reminder: str

class ReminderRead(SQLModel):
    chatId: int

class Reminder(ReminderBase, TimestampModel, table=True):
    __tablename__ = "messages_reminders_chatbot"
    id: Optional[int] = Field(default=None, primary_key=True)
    def __repr__(self):
        return f"Reminder {self.id} - {self.type} - {self.content} - {self.chatId} - {self.time_remind} - {self.is_remind}"
