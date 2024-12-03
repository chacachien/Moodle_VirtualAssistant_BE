from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_REMINDER, PROMPT_REMINDER_DAILY,PROMPT_REMINDER_ASSIGN, PROMPT_REMINDER_QUIZ
from langchain_core.output_parsers import StrOutputParser

class ReminderBot(RootBot):
    def __init__(self):
        super().__init__()

    def reminder(self, message, type, mod_id):
        prompt = PROMPT_REMINDER
        if type == 'quiz':
            prompt = PROMPT_REMINDER_QUIZ
        elif type =='assign':
            prompt = PROMPT_REMINDER_ASSIGN
        chain = prompt| self.groq | StrOutputParser()
        response = chain.invoke({ "input": message, "mod_id": mod_id})
        return response

    def reminder_daily(self, message):
        chain = PROMPT_REMINDER_DAILY | self.model | StrOutputParser()
        response = chain.invoke({"input": message})
        return response