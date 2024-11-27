from sqlalchemy import text, create_engine
from app.chatbot.querybot import table_info
from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_SQL_ANSWER, PROMPT_STRUCTURE_TABLE, PROMPT_SQL_QUERY, PROMPT_FIX_BUG, PROMPT_CHAT, \
    PROMPT_SQL_QUERY_GPT
from langchain_core.output_parsers import StrOutputParser
from app.core.config import get_url_notsync, get_url
from app.core.config import BASE_DIR

import re

class QueryBot(RootBot):
    def __init__(self):
        super().__init__()
        self.structure_prompt = PROMPT_STRUCTURE_TABLE
        self.sql_answer_prompt = PROMPT_SQL_ANSWER
        self.sql_query_prompt = PROMPT_SQL_QUERY
        self.fix_bug_prompt = PROMPT_FIX_BUG
        self.db = create_engine(get_url_notsync())
        self.table_info = ''

    def get_table_info(self):
        with open(f"{BASE_DIR}/app/chatbot/querybot/sql_improve.txt", 'r') as f:
            text = f.read()
        return text


    async def query(self, question: str, id: int):
        pattern = r"SELECT.*?;"
        structure_chain = (
            self.structure_prompt
            #| self.model
            |self.groq
            | StrOutputParser()
        )
        #self.table_info = self.get_table_info() if self.table_info== '' else self.table_info
        self.table_info = table_info
        threshold = 4
        flag = False
        query_result = ''
        r = 0
        list_remind = ['Bạn chịu khó đợi một tí nhé!\n', 'Thông tin đang được xử lý rồi!\n']
        yield "Tìm kiếm thông tin\n"
        for j in range(threshold):
            if flag: break
            #database_structure = structure_chain.invoke({ "question": question, "database_structure": self.table_info})
            database_structure = self.table_info
            sql_code = ''
            err = ''
            for i in range(2):
                if err =='':
                    chain = (
                        PROMPT_SQL_QUERY
                        #| self.model_openai4
                        | self.claude3_5
                        | StrOutputParser()
                    )
                    execute_query = chain.invoke({"id": id,"question": [question], "database_structure": database_structure })
                    try:
                        execute_query = re.findall(pattern, execute_query,re.DOTALL)[0]
                        print("SQL: ", execute_query)
                        # try the sql query
                        query_result = None
                        with self.db.connect() as connection:
                            # Execute the SQL query to fetch all users
                            query = text(execute_query)
                            result = connection.execute(query)
                            query_result = result.fetchall()
                            print("QUERY RESULT: ", query_result)
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
                        print("FIX BUG SQL: ", execute_query)
                        query_result = None
                        with self.db.connect() as connection:
                            # Execute the SQL query to fetch all users
                            query = text(execute_query)
                            result = connection.execute(query)
                            query_result = result.fetchall()
                            print("QUERY RESULT: ", query_result)
                        flag = True
                        break
                    except Exception as e:
                        err = e
        chain = (
            PROMPT_SQL_ANSWER
            #| self.model1_5
            | self.model_openai
            | StrOutputParser()
        )
        #final_result = chain.invoke({'id': id, "question": question, "result": query_result})
        full_bot_message = []
        yield "&start&\n"
        for chunk in chain.stream({'id': id, "question": question, "result": query_result}):
            yield chunk
