from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_REMINDER, PROMPT_REMINDER_DAILY
from langchain_core.output_parsers import StrOutputParser

class ReminderBot(RootBot):
    def __init__(self):
        super().__init__()

    def reminder(self, message):
        chain = PROMPT_REMINDER| self.groq | StrOutputParser()
        response = chain.invoke({ "input": message})
        return response

    def reminder_daily(self, message):
        chain = PROMPT_REMINDER_DAILY | self.model | StrOutputParser()
        response = chain.invoke({"input": message})
        return response