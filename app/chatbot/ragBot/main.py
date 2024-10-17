

import groq
from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_RAG, PROMPT_RAG_IMPROVE, PROMPT_REMIND_TO_COURSE
from langchain.schema.output_parser import StrOutputParser

from app.chatbot.ragBot.pgData import LoadData as LoadDataPg
from app.services.schedule import ReminderService

import numpy as np
import pgvector.psycopg2

# class RagBot(RootBot):
#     def __init__(self):
#         super().__init__()
#         self.prompt = PROMPT_RAG_IMPROVE
#         self.prompt_remind_to_couse = PROMPT_REMIND_TO_COURSE
#         self.data = LoadData()


#     async def rag(self, user_message, courseId):
#         """
#             def as_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
#         Return VectorStoreRetriever initialized from this VectorStore.

#         Args:
#             search_type (Optional[str]): Defines the type of search that
#                 the Retriever should perform.
#                 Can be "similarity" (default), "mmr", or
#                 "similarity_score_threshold".
#             search_kwargs (Optional[Dict]): Keyword arguments to pass to the
#                 search function. Can include things like:
#                     k: Amount of documents to return (Default: 4)
#                     score_threshold: Minimum relevance threshold
#                         for similarity_score_threshold
#                     fetch_k: Amount of documents to pass to MMR algorithm (Default: 20)
#                     lambda_mult: Diversity of results returned by MMR;
#                         1 for minimum diversity and 0 for maximum. (Default: 0.5)
#                     filter: Filter by document metadata
#         """

#         yield "Tìm kiếm thông tin\n"

#         self.data.embed_data()
#         # context = self.data.docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
#         # context_max = self.data.docsearch.as_retriever(search_type='mmr', search_kwargs={"k": 3})
#         # context_max_search = self.data.docsearch.max_marginal_relevance_search(user_message, k=3, fetch_k=10)

#         search_kwargs = {
#             "k": 2,
        
#         } if courseId == -1 else {
#              "k": 4,
#             'filter': {
#                 'course': courseId,
#             }
#         }
#         yield "Phân tích tài liệu\n"

#         # print("KWARGS: ", search_kwargs)
#         # context_with_course = self.data.docsearch.as_retriever(
#         #                             search_type = 'similarity_score_threshold',
#         #                             search_kwargs = search_kwargs
#         #                         )
#         # print("KWARGS: ", search_kwargs)
#         context_with_course = self.data.docsearch.as_retriever(
#                                     search_type = 'mmr',
#                                     search_kwargs = search_kwargs
#                                 )
#         content =  context_with_course.invoke(user_message)[0].metadata

#         yield "Nội dung sẳn sàng\n"
#         #await asyncio.sleep(0.1)  # Small delay to ensure this message is sent first

#         # prompt need "context", "question" and "course_id"

#         # chain = (
#         #     {"context": context_with_course , "question": RunnablePassthrough()}|
#         #     self.prompt|
#         #     self.model|
#         #     StrOutputParser()
#         # )
        

#         # res = chain.invoke(user_message)
#         yield "&start&\n"
#         if courseId != -1:
#             chain = (
#                 {"context": context_with_course, "question":RunnablePassthrough() }|
#                 self.prompt|
#                 self.model|
#                 StrOutputParser()
#             )

#             for chunk in chain.stream(user_message):

#                 yield chunk  # Yield each chunk as it's generated
#         else:
#             chain = (
#                 self.prompt_remind_to_couse|
#                 self.model1_5|
#                 StrOutputParser()
#             )
#             course_name = ReminderService.get_coursename(int(content['course']))
#             context = {
#                 "course_id": int(content['course']),
#                 "course_name": course_name
#             }
#             for chunk in chain.stream({"input": user_message, "context": context}):

#                 yield chunk 


from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector

class RagBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_RAG_IMPROVE
        self.prompt_remind_to_couse = PROMPT_REMIND_TO_COURSE
        self.data = LoadDataPg()



# Helper function: Get top 3 most similar documents from the database
    def get_top3_similar_docs(self, query_embedding):
        embedding_array = np.array(query_embedding)
        # Register pgvector extension
        register_vector(self.data.conn)
        cur = self.data.conn.cursor()
        # Get the top 3 most similar documents using the KNN <=> operator
        cur.execute("SELECT content, courseid FROM embeddings_v2 ORDER BY embedding <=> %s LIMIT 3", (embedding_array,))
        top3_docs = cur.fetchall()
        return top3_docs



    async def rag(self, user_message, courseId):
        """
            def as_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
        Return VectorStoreRetriever initialized from this VectorStore.

        Args:
            search_type (Optional[str]): Defines the type of search that
                the Retriever should perform.
                Can be "similarity" (default), "mmr", or
                "similarity_score_threshold".
            search_kwargs (Optional[Dict]): Keyword arguments to pass to the
                search function. Can include things like:
                    k: Amount of documents to return (Default: 4)
                    score_threshold: Minimum relevance threshold
                        for similarity_score_threshold
                    fetch_k: Amount of documents to pass to MMR algorithm (Default: 20)
                    lambda_mult: Diversity of results returned by MMR;
                        1 for minimum diversity and 0 for maximum. (Default: 0.5)
                    filter: Filter by document metadata
        """

        yield "Tìm kiếm thông tin\n"

        # context = self.data.docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        # context_max = self.data.docsearch.as_retriever(search_type='mmr', search_kwargs={"k": 3})
        # context_max_search = self.data.docsearch.max_marginal_relevance_search(user_message, k=3, fetch_k=10)

        # search_kwargs = {
        #     "k": 2,
        
        # } if courseId == -1 else {
        #      "k": 4,
        #     'filter': {
        #         'course': courseId,
        #     }
        # }

        # print("KWARGS: ", search_kwargs)
        # context_with_course = self.data.docsearch.as_retriever(
        #                             search_type = 'similarity_score_threshold',
        #                             search_kwargs = search_kwargs
        #                         )
        # print("KWARGS: ", search_kwargs)
        # context_with_course = self.data.docsearch.as_retriever(
        #                             search_type = 'mmr',
        #                             search_kwargs = search_kwargs
        #                         )
        # content =  context_with_course.invoke(user_message)[0].metadata

        content = self.get_top3_similar_docs(self.data.get_embedding(user_message))
        #print(f"Whole content: {content}")
        # print(f"Content 1: {content[0][0]}")
        # print(f"Content 2: {content[1][0]}")
        # print(f"Content 3: {content[2][0]}")
        #await asyncio.sleep(0.1)  # Small delay to ensure this message is sent first

        # prompt need "context", "question" and "course_id"

        # chain = (
        #     {"context": context_with_course , "question": RunnablePassthrough()}|
        #     self.prompt|
        #     self.model|
        #     StrOutputParser()
        # )


        # res = chain.invoke(user_message)
        #print(f"{len(content)} must in LIST COURSE: {type(content[0][1])}, {content[1][1]}, {content[2][1]}")

        list_course = [content[0][1], content[1][1], content[2][1]]
        if courseId != -1 and (courseId in list_course):
            context_str = " \n ".join([content[i][0] if i < len(content) else "" for i in range(3)])
            chain = (
                self.prompt|
                #self.model_openai|
                #self.groq|
                self.model|
                StrOutputParser()
            )
            yield "Nội dung sẳn sàng\n"
            yield "&start&\n"
            for chunk in chain.stream({"question": user_message, "context": context_str}):
                yield chunk  # Yield each chunk as it's generated
        else:
            import statistics
            mode = statistics.mode(list_course)
            course_name = ReminderService.get_coursename(mode)
            chain = (
                self.prompt_remind_to_couse|
                self.model1_5|
                #self.groq|
                StrOutputParser()
            )
            context = {
                "course_id": mode,
                "course_name": course_name
            }
            yield "Nội dung sẳn sàng\n"
            yield "&start&\n"
            for chunk in chain.stream({"input": user_message, "context": context}):
                yield chunk

def main():
    chat = RagBot()
    
    question = "Cuộc chiến tranh nhà Ngô chống lại quân đội nước nào"
    question = 'vì sao có chữ nôm'
    question = 'đặc điểm tiếng việt'
    question = 'kể tên các tác phẩm chữ nôm'
    question = 'tác phẩm lục vân tiên nói về điều gì'
    question = 'tóm tắt toàn bộ nội dung khoá học'
    question = 'ML là gì'
    question = 'tác giả của cánh đồng bất tận'
    question = 'các loại việt phục được nêu ra trong bài'
    chat.model = chat.model1_5
    res = chat.rag(question, -1)
    print(res)
    return
    from langchain.chains import create_history_aware_retriever
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    llm = chat.model1_5
    chat.data.embed_data()
    retriever = chat.data.docsearch.as_retriever()
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain

    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )


    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    from langchain_core.messages import HumanMessage

    chat_history = []

    store = {}

    from langchain_core.chat_history import BaseChatMessageHistory
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory


    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]


    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    import time
    while True:
        user_message = input("User: ")
        chat_history.append(HumanMessage(user_message))
        s = time.time()
        res = conversational_rag_chain.invoke({"input": user_message},
                                config={
                                    "configurable": {"session_id": "abc123"}
                                }, )['answer']
        e = time.time()
        print("TIME: ", e-s)
        print("Bot: ", res)

if __name__ == '__main__':
    main()


