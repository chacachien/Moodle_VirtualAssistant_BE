import groq
from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_RAG, PROMPT_RAG_IMPROVE, PROMPT_REMIND_TO_COURSE
from langchain.schema.output_parser import StrOutputParser

from app.chatbot.ragBot.pgData import LoadData as LoadDataPg
from app.services.schedule import ReminderService

import numpy as np
import pgvector.psycopg2

from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector

class RagBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_RAG_IMPROVE
        self.prompt_remind_to_couse = PROMPT_REMIND_TO_COURSE
        self.data = LoadDataPg()
        self.number_content = 4


# Helper function: Get top 3 most similar documents from the database
    def get_top3_similar_docs(self, query_embedding):
        embedding_array = np.array(query_embedding)
        # Register pgvector extension
        register_vector(self.data.conn)
        cur = self.data.conn.cursor()
        # Get the top 3 most similar documents using the KNN <=> operator
        cur.execute("SELECT content, courseid FROM embeddings_v2 ORDER BY embedding <=> %s LIMIT %s",(embedding_array, self.number_content))
        top3_docs = cur.fetchall()
        print("TOP 3: ", top3_docs)
        return top3_docs


    async def rag(self, user_message, courseId):
        content = self.get_top3_similar_docs(self.data.get_embedding(user_message))
        # res = chain.invoke(user_message)
        #print(f"{len(content)} must in LIST COURSE: {type(content[0][1])}, {content[1][1]}, {content[2][1]}")
        list_course = [content[c][1] for c in range(0,len(content))]
        if courseId != -1 and (courseId in list_course):
            context_str = " \n ".join([content[i][0] if i < len(content) else "" for i in range(3)])
            chain = (
                self.prompt|
                self.model_gemini_1_5|
                #self.groq|
                #self.model|
                StrOutputParser()
            )
            for chunk in chain.stream({"question": user_message, "context": context_str}):
                yield chunk  # Yield each chunk as it's generated
        else:
            import statistics
            mode = statistics.mode(list_course)
            print("MODE: ", mode)
            course_name = ReminderService.get_coursename(mode)
            chain = (
                self.prompt_remind_to_couse|
                #self.model1_5|
                #self.groq|
                self.model_gemini_1_5|
                StrOutputParser()
            )
            context = {
                "course_id": mode,
                "course_name": course_name
            }
            for chunk in chain.stream({"input": user_message, "context": context}):
                yield chunk