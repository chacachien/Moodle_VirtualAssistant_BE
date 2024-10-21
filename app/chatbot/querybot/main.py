from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_SQL_ANSWER, PROMPT_STRUCTURE_TABLE, PROMPT_SQL_QUERY, PROMPT_FIX_BUG, PROMPT_CHAT, \
    PROMPT_SQL_QUERY_GPT
from langchain_core.output_parsers import StrOutputParser
from app.core.config import get_url_notsync
from app.core.config import BASE_DIR
from langchain.sql_database import SQLDatabase
import re

class QueryBot(RootBot):
    def __init__(self):
        super().__init__()
        self.structure_prompt = PROMPT_STRUCTURE_TABLE
        self.sql_answer_prompt = PROMPT_SQL_ANSWER
        self.sql_query_prompt = PROMPT_SQL_QUERY
        self.fix_bug_prompt = PROMPT_FIX_BUG
        DATABASE_URL = get_url_notsync()
        self.db =  SQLDatabase.from_uri(DATABASE_URL)
        self.table_info = ''

    def get_table_info(self):
        with open(f"{BASE_DIR}/app/chatbot/querybot/sql_improve.txt", 'r') as f:
            text = f.read()
        return text


    async def query(self, question: str, id: int):
        pattern = r"SELECT.*?;"
        structure_chain = (
            self.structure_prompt
            | self.model
            | StrOutputParser()
        )
        self.table_info = self.get_table_info() if self.table_info== '' else self.table_info
        threshold = 4
        flag = False
        query_result = ''
        r = 0
        list_remind = ['Bạn chịu khó đợi một tí nhé!', 'Thông tin đang được xử lý rồi!']
        yield "Tìm kiếm thông tin\n"
        for j in range(threshold):
            if flag: break
            database_structure = structure_chain.invoke({ "question": question, "database_structure": self.table_info})
            sql_code = ''
            err = ''
            for i in range(2):
                if err !='':
                    chain = (
                        PROMPT_SQL_QUERY_GPT
                        | self.model_openai
                        | StrOutputParser()
                    )
                    execute_query = chain.invoke({"id": id,"question": [question], "database_structure": database_structure })
                    try:
                        execute_query = re.findall(pattern, execute_query,re.DOTALL)[0]
                        sql_code = execute_query
                    # try the sql query
                        query_result  = self.db.run(execute_query)
                        flag = True
                        break
                    except Exception as e:
                        if r < 2:
                            yield list_remind[r]
                            r = r + 1
                        err = e
                else:
                    require_prompt = self.fix_bug_prompt
                    # call to get the sql
                    chain = (
                        require_prompt
                        | self.groq
                        | StrOutputParser()
                    )
                    execute_query = chain.invoke({"id": id, "question": question, "database_structure": database_structure, "SQL_code": sql_code, 'Error':{err}})

                    pattern = r"SELECT.*?;"
                    try:
                        execute_query = re.findall(pattern, execute_query,re.DOTALL)[0]
                        query_result  = self.db.run(execute_query)
                        flag = True
                        break
                    except Exception as e:
                        err = e
        yield "Nội dung sẳn sàng\n"
        answer_prompt = PROMPT_SQL_ANSWER
        chain = (
            answer_prompt
            | self.model1_5
            | StrOutputParser()
        )
        #final_result = chain.invoke({'id': id, "question": question, "result": query_result})
        full_bot_message = []
        yield "&start&"
        for chunk in chain.stream({'id': id, "question": question, "result": query_result}):
            yield chunk

    def test(self):
        while True:
            id = 2
            query = input("user: ")
            if query == "exit":
                break

            response = self.query(query, id)
            print("ai: ", response)
            print('/n')
            print("*"*100)
            print('/n')