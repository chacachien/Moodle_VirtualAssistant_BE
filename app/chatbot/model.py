from asyncio import get_event_loop
from chunk import Chunk
import collections

from sympy import fu
from app.chatbot.prompt import PROMPT_CHOOSE_TOOLS, PROMPT_CHOOSE_TOOLS_V1, PROMPT_REWRITE_QUESTION, PROMPT_CHOOSE_TOOLS_V2
from app.chatbot.tools import Tool
from app.chatbot.root import RootBot
from app.chatbot.querybot.main import QueryBot
from app.chatbot.talkbot.main import TalkBot
from app.chatbot.ragBot.main import RagBot
from app.chatbot.schema import ToolSchema

from langchain.tools.render import render_text_description
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from operator import itemgetter
import json
from langchain.schema import HumanMessage, AIMessage

class ChatBot(RootBot):
    def __init__(self):
        super().__init__()
        self.__chat_history_buffer = collections.deque([], maxlen=10)
        self.queryBot = QueryBot()
        self.talkBot = TalkBot()
        self.ragBot = RagBot()

    def get_history(self):
        # if not relevant_message: return None
        # non_dup_mes = []
        # for m in relevant_message:
        #     if m not in self.__chat_history_buffer:
        #         non_dup_mes.append(m)
        messages = []
        # messages.append(self.system_prompt)
        # for message in non_dup_mes:
        #     message_doc = json.loads(message)
        #     messages.append(HumanMessage(content=message_doc["user"]))
        #     messages.append(AIMessage(content=message_doc["ai"]))

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
        chain = self.prompt | self.model | parser | tool_chain 

        res = chain.invoke({"rendered_tools":rendered_tools, "input": user_message })
        return res , user_message
    
    def chose_tool(self, user_message):
        chain = PROMPT_CHOOSE_TOOLS_V2 | self.groq | StrOutputParser()
        res = chain.invoke({"input": user_message})
        return res

    def improve_message(self, user_message):
        prompt = PROMPT_REWRITE_QUESTION
        chain = prompt | self.groq | StrOutputParser()
        res = chain.invoke({"history": self.__chat_history_buffer, "input": user_message })
        print(f"MESSAGE AFTER IMPROVE: {res}")
        return res


    async def get_response(self, user_message, chatId, courseId, role):

        full_bot_response = []
        user_message = self.improve_message(user_message)
        if role == 0:
            role = self.chat_with_tool(user_message)


        if role == 1:
            async for chunk in self.ragBot.rag(user_message, courseId):
                full_bot_response.append(chunk)
                yield chunk
        # if role ==0:
        #     tool, new_user_message  = self.chat_with_tool(user_message)




        elif role == 10:
            async for chunk in self.queryBot.query(user_message, courseId):
                full_bot_response.append(chunk)
                yield chunk

        # elif role ==2:
        #     pass
        # elif role == 3:
        #     pass
        # else:
        #     pass
        # import time
        # s = time.time()
        # tool, new_user_message  = self.chat_with_tool(user_message)
        # res = None

        # if tool == 'talk':
        #     print('TOOL TALK')
        #     #res = self.talkBot.talk(user_message, self.__chat_history_buffer)
        #     #res = self.talkBot.talk_stream(user_message, self.__chat_history_buffer)

        #     chain = self.talkBot.prompt | self.talkBot.model | StrOutputParser()
        #     async for chunk in chain.stream({"context":history, "input":user_message}):
        #         yield(chunk)
            
        # if tool == 'rag':
        #     print('TOOL RAG')
        #     res = self.ragBot.rag(user_message, courseId)

        # if tool == 'query':
        #     print('TOOL QUERY')
        #     res = self.queryBot.query(new_user_message, chatId)

        bot_message = ''.join(full_bot_response)
        self.__chat_history_buffer.append({"user": user_message, "ai": bot_message})
        print("HISTORY: ", self.__chat_history_buffer)
        # e = time.time()
        # print("TIME: ", e-s)
        #return res


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

if __name__ == "__main__":
    bot = ChatBot()
    # loop = get_event_loop()
    # loop.run_until_complete(bot.test_chatbot_with_tools())
    import time
    s = time.time()
    history = [
        {"user": "hi", 'ai': 'hello, how can i assist you today'},
        {"user": "what is course of me", 'ai': 'you have 2 courses: image processing course and mobile app course'}
    ]
    user_message = "Khóa học nào nhiều bài tập hơn"
    res = bot.improve_message(history, user_message)

    ans = bot.get_response(user_message, 1, 1)
    print(res)
    print(ans)
    e = time.time()
    print("TIME: ", e-s)

