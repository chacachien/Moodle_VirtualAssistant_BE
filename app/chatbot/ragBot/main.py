from calendar import c
from re import search
from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_RAG, PROMPT_RAG_IMPROVE, PROMPT_REMIND_TO_COURSE
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from app.chatbot.ragBot.data import LoadData
from app.services.context_service import SystemService

class RagBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_RAG_IMPROVE
        self.prompt_remind_to_couse = PROMPT_REMIND_TO_COURSE
        self.data = LoadData()

    def rag(self, user_message, courseId):
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
        self.data.embed_data()
        context = self.data.docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        context_max = self.data.docsearch.as_retriever(search_type='mmr', search_kwargs={"k": 3})
        context_max_search = self.data.docsearch.max_marginal_relevance_search(user_message, k=3, fetch_k=10)

        search_kwargs = {
            "k": 4,
        } if courseId == -1 else {
             "k": 4,
            'filter': {
                'course': courseId,
            }
        }
        print("KWARGS: ", search_kwargs)
        context_with_course = self.data.docsearch.as_retriever(
                                    search_type = 'mmr',
                                    search_kwargs = search_kwargs
                                )
        
        print("content: ", context_with_course.invoke(user_message))


        # prompt need "context", "question" and "course_id"
        chain = (
            {"context": context_with_course , "question": RunnablePassthrough()}|
            self.prompt|
            self.model|
            StrOutputParser()
        )
        # chain = (
        #     {"context": context_with_course , "question": RunnablePassthrough()}|
        #     self.prompt|
        #     self.model|
        #     StrOutputParser()
        # )

        res = chain.invoke(user_message)

        if courseId != -1:
            return res
        

        chain = (
            self.prompt_remind_to_couse|
            self.model|
            StrOutputParser()
        )
        context = SystemService.get_all_course()

        return  res + "\n" + chain.invoke({"input": user_message, "context": context})
    
def main():
    chat = RagBot()
    question = "Cuộc chiến tranh nhà Ngô chống lại quân đội nước nào"
    question = 'vì sao có chữ nôm'
    question = 'đặc điểm tiếng việt'
    question = 'kể tên các tác phẩm chữ nôm'
    question = 'tác phẩm lục vân tiên nói về điều gì'
    question = 'tóm tắt toàn bộ nội dung khoá học'
    question = 'các loại việt phục được nêu ra trong bài'

    res = chat.rag(question, -1)
    print(res)

if __name__ == '__main__':
    main()