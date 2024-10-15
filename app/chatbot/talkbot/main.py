from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_NORMAL_TALK
from langchain_core.output_parsers import StrOutputParser


class TalkBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_NORMAL_TALK
       # self.prompt_history = PROMPT_NORMAL_TALK_HISTORY


    async def talk(self, message, history):
        chain = self.prompt | self.model | StrOutputParser()
        # response = chain.invoke({"context":history, "input":message})
        # return response

        for chunk in chain.stream({"context":history, "input":message}):
            yield chunk


# import human message and ai message 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def main():
    # bot = TalkBot()
    # bot_message = HumanMessage("Hello")
    # ai_message = AIMessage("Hello")
    # history = [bot_message, ai_message]

    # response = bot.talk("Hello", history)
    # print(response)
    from langchain_google_vertexai import VertexAI

# To use model
    model = VertexAI(model_name="gemini-pro")
    message = "What are some of the pros and cons of Python as a programming language?"
    model.invoke(message)
if __name__ == "__main__":
    main()