import collections
from app.chatbot.prompt import PROMPT_CHOOSE_TOOLS, PROMPT_CHOOSE_TOOLS_V1, PROMPT_REWRITE_QUESTION, PROMPT_CHOOSE_TOOLS_V2
from app.chatbot.root import RootBot
from app.chatbot.querybot.main import QueryBot
from app.chatbot.talkbot.main import TalkBot
from app.chatbot.ragBot.main import RagBot

from langchain.tools.render import render_text_description
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from operator import itemgetter
import json
from langchain.schema import HumanMessage, AIMessage
import re

class ChatBot(RootBot):
    def __init__(self):
        super().__init__()
        self.__chat_history_buffer = collections.deque([], maxlen=10)
        self.queryBot = QueryBot()
        self.talkBot = TalkBot()
        self.ragBot = RagBot()

    def get_history(self):
        messages = []

        for message in self.__chat_history_buffer:
            message_doc = json.loads(message) if isinstance(message, str) else message
            messages.append(HumanMessage(content=message_doc["user"]))
            messages.append(AIMessage(content=message_doc["ai"]))
        return messages

    def chat_with_tool(self, user_message):

        user_message = self.improve_message(user_message)
        
        print('NEW USER MESSAGE: ',user_message)
        
        tools = [Tool.talk, Tool.rag, Tool.query]

        def tool_chain(model_output):
            tool_map = {tool.name: tool for tool in tools}
            chosen_tool = tool_map[model_output["name"]]
            print("CHOSEN TOOL: ", chosen_tool)
            return itemgetter("arguments") | chosen_tool
        rendered_tools = render_text_description(tools)
        parser = JsonOutputParser(pydantic_object=ToolSchema)
        chain = self.prompt | self.groq | parser | tool_chain

        res = chain.invoke({"rendered_tools":rendered_tools, "input": user_message })
        return res , user_message
    
    def chose_tool(self, user_message):
        chain = PROMPT_CHOOSE_TOOLS_V2 | self.groq | StrOutputParser()
        res = chain.invoke({"input": user_message})

        match = re.search(r'\d+', res)

        if match:
            return int(match.group())
        else:
            return 1

    def improve_message(self, user_message):
        chain = PROMPT_REWRITE_QUESTION | self.groq | StrOutputParser()
        res = chain.invoke({"history": self.__chat_history_buffer, "input": user_message })
        print(f"MESSAGE AFTER IMPROVE: {res}")
        return res


    async def get_response(self, user_message, chatId, courseId, role, user_role):
        print("start at get response")
        full_bot_response = []
        user_message = self.improve_message(user_message)
        if role == 0:
            role = self.chose_tool(user_message)
            if user_role == 0:
                if role ==2:
                    role = 3
        print("ROLE BOT: ", role)
        if role == 1:
            async for chunk in self.ragBot.rag(user_message, courseId):
                full_bot_response.append(chunk)
                yield chunk
        elif role == 2:
            async for chunk in self.queryBot.query(user_message, chatId):
                full_bot_response.append(chunk)
                yield chunk
        elif role == 3:
            async for chunk in self.talkBot.talk(user_message):
                full_bot_response.append(chunk)
                yield chunk
        elif role == 4:
            async for chunk in self.adviceBot.run():
                full_bot_response.append(chunk)
                yield chunk
        bot_message = ''.join(full_bot_response)
        if bot_message:
            match = re.search(r"&start&\n(.*)", bot_message, re.DOTALL)
            if match:
                bot_message = match.group(1)
        self.__chat_history_buffer.append({"user": user_message, "ai": bot_message})
        print("HISTRY: ", self.__chat_history_buffer)
    def test_chatbot_with_tools(self):
        while True:
            query = input("user: ")
            if query == "exit":
                break
            response = self.chat_with_tool(user_message=query)
            print("ai: ", response)
            print('/n')
            print("*"*100)
            print('/n')