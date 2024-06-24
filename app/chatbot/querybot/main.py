from asyncio import get_event_loop
from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_SQL_ANSWER, PROMPT_STRUCTURE_TABLE, PROMPT_SQL_QUERY, PROMPT_FIX_BUG, PROMPT_CHAT
from langchain_core.output_parsers import StrOutputParser
from app.core.config import get_url_notsync
from app.core.config import BASE_DIR
from langchain.sql_database import SQLDatabase


class QueryBot(RootBot):
    def __init__(self):
        super().__init__()
        self.structure_prompt = PROMPT_STRUCTURE_TABLE
        self.sql_answer_prompt = PROMPT_SQL_ANSWER
        self.sql_query_prompt = PROMPT_SQL_QUERY
        self.fix_bug_prompt = PROMPT_FIX_BUG
        DATABASE_URL = get_url_notsync()
        self.db = SQLDatabase.from_uri(DATABASE_URL)
        self.table_info = ''

    def get_table_info(self):
        with open(f"{BASE_DIR}/app/chatbot/querybot/sql_improve.txt", encoding="utf8") as f:
            text = f.read()
        return text

    def query(self, question: str, id: int):
        structure_chain = (
            self.structure_prompt
            | self.model
            | StrOutputParser()
        )
        self.table_info = self.get_table_info() if self.table_info == '' else self.table_info
        database_structure = structure_chain.invoke(
            {"question": question, "database_structure": self.table_info})
        print('PROMPT: ', self.structure_prompt)
        print("----------")
        print("DATABASE STRUCTURE: ", database_structure)
        print("----------")
        sql_code = ''
        err = ''
        query_result = ''
        for i in range(3):
            try:
                if err != '':
                    require_prompt = self.sql_query_prompt
                    chain = (
                        require_prompt
                        | self.model
                        | StrOutputParser()
                    )
                    execute_query = chain.invoke(
                        {"id": id, "question": question, "database_structure": database_structure})

                    import re
                    pattern = r"SELECT.*?;"
                    execute_query = re.findall(
                        pattern, execute_query, re.DOTALL)[0]
                    print("EXECUTE QUERY: ", execute_query)
                    print("----------")
                    sql_code = execute_query
                    # try the sql query
                    query_result = self.db.run(execute_query)
                    break
                else:
                    require_prompt = self.fix_bug_prompt
                    # call to get the sql
                    chain = (
                        require_prompt
                        | self.model
                        | StrOutputParser()
                    )
                    execute_query = chain.invoke(
                        {"id": id, "question": question, "database_structure": database_structure, "SQL_code": sql_code, 'Error': {err}})
                    import re
                    pattern = r"SELECT.*?;"
                    execute_query = re.findall(
                        pattern, execute_query, re.DOTALL)[0]
                    print("EXECUTE QUERY: ", execute_query)
                    print("----------")
                    # try the sql query
                    query_result = self.db.run(execute_query)
            except Exception as e:
                print(e)
                err = e
                continue
        print("query_result: ", query_result)
        print("----------")

        answer_prompt = PROMPT_SQL_ANSWER
        chain = (
            answer_prompt
            | self.model
            | StrOutputParser()
        )
        final_result = chain.invoke(
            {'id': id, "question": question, "result": query_result})
        return final_result

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


if __name__ == "__main__":
    bot = QueryBot()
    loop = get_event_loop()
    loop.run_until_complete(bot.test())
