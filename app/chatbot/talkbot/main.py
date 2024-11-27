from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_NORMAL_TALK
from langchain_core.output_parsers import StrOutputParser

class TalkBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_NORMAL_TALK
       # self.prompt_history = PROMPT_NORMAL_TALK_HISTORY


    async def talk(self, message, history):
        chain = self.prompt | self.groq | StrOutputParser()
        # response = chain.invoke({"context":history, "input":message})
        # return response

        for chunk in chain.stream({"context":history, "input":message}):
            yield chunk
