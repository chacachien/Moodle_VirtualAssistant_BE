from langchain.schema import HumanMessage, AIMessage
import collections
import json
from app.chatbot.prompt import *
from app.chatbot.root import RootBot
from app.chatbot.querybot.main import QueryBot

class SubChatBot(RootBot):
    def __init__(self):
        super().__init__()
        # Define the repo ID and connect to Mixtral model on Huggingface
        self.__chat_history_buffer = collections.deque([], maxlen=5)
        self.__self_reminder_prompt = PROMPT_REMINDER
        self.current_task = 'talk'
        self.queryBot = QueryBot()


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
    
    def get_response(self, context, messages, id):
        if self.current_task == 'talk':
            prompt = PROMPT_NORMAL_TALK
            chain = prompt| self.groq
                #StrOutputParser()
            res = chain.invoke({"context": context, "question": messages})
            print("TOOL TALK")
            return res.content
        
        elif self.current_task == 'help':
            prompt = PROMPT_RAG
            chain = prompt| self.groq
                #StrOutputParser()
            res = chain.invoke({"context": context, "question": messages} )
            print("TOOL HELP")
            return res.content
        
        else:
            
            res = self.queryBot.query(messages, id, context)
            print("TOOL QUERY")
            return res
      
    def chat(self, user_message, id, history):
        # messages = []
        # if self.__chat_history_buffer:
        #     messages.append(self.get_history())
        #     print("HISTORY: ", messages)
        # query_with_remider_prompt = f"{self.__self_reminder_prompt} \n query: {user_message}"

        #messages.append(HumanMessage(content=query_with_remider_prompt))

        response_message = self.get_response(messages, user_message, id)
        print("RESPONSE MESS: ", response_message)

        output = "".join(response_message)
        memory_data = {"user": user_message, "ai": output}
        data_string = json.dumps(memory_data)

        self.__chat_history_buffer.append(data_string)
        return output
    
    
    def convert_to_another(self, type_of_tool):
        if type_of_tool == self.current_task:
            return
        self.current_task = type_of_tool

