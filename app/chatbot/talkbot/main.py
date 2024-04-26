from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_NORMAL_TALK
from langchain_core.output_parsers import StrOutputParser

class TalkBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_NORMAL_TALK

    def talk(self, message, history):
        chain = self.prompt | self.model | StrOutputParser()
        response = chain.invoke({"context":history, "input":message})
        return response
