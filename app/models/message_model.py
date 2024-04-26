from enum import Enum
from app.models.base_model import TimestampModel
from sqlmodel import SQLModel, Field
from typing import Optional


class TypeRoleChoices(Enum):
    BOT = 0
    USER = 1

class MessageBase(SQLModel):
    content: str = Field(max_length=255)
    chatId: int
    role: TypeRoleChoices

class MessageCreate(MessageBase):
    pass

class MessageRead(SQLModel):
    chatId: int

class Message(MessageBase, TimestampModel, table=True):
    __tablename__ = "messages_chatbot"
    id: Optional[int] = Field(default=None, primary_key=True)
    #user: Optional[User] = Relationship(back_populates="messages", link_model=User)
    def __repr__(self):
        return f"Message {self.id} - {self.content} - {self.chatId} - {self.role}"
    
class MessageDeleted(MessageBase, TimestampModel, table=True):
    __tablename__ = "messages_chatbot_deleted"
    id: Optional[int] = Field(default=None, primary_key=True)
    #user: Optional[User] = Relationship(back_populates="messages", link_model=User)
    def __repr__(self):
        return f"Message is deleted: {self.id} - {self.content} - {self.chatId} - {self.role}"

