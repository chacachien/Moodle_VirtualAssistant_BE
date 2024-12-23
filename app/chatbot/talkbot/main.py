from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_NORMAL_TALK
from langchain_core.output_parsers import StrOutputParser

class TalkBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_NORMAL_TALK
       # self.prompt_history = PROMPT_NORMAL_TALK_HISTORY


    async def talk(self, message):
        chain = self.prompt | self.groq | StrOutputParser()
        # response = chain.invoke({"context":history, "input":message})
        # return response
        print("Talk", chain)
        for chunk in chain.stream({"input":message}):
            print("CHUNK INSIDE: ", chunk)
            yield chunk
