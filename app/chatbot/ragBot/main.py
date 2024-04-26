from app.chatbot.root import RootBot
from app.chatbot.prompt import PROMPT_RAG
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from app.chatbot.ragBot.data import LoadData


class RagBot(RootBot):
    def __init__(self):
        super().__init__()
        self.prompt = PROMPT_RAG
        self.data = LoadData()


    def load_data(self):
        self.data.embed_data()

        
    def rag(self, user_message):

        self.load_data()
        def format_docs(docs):
            print(docs)
            return "\n\n".join(doc.page_content for doc in docs)
        context = self.data.docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        context_max = self.data.docsearch.as_retriever(search_type='mmr', search_kwargs={"k": 3})
        context_max_search = self.data.docsearch.max_marginal_relevance_search(user_message, k=3, fetch_k=10)
        print("CONTEXT: ", context_max_search)

        chain = (
            {"context": context , "question": RunnablePassthrough()}|
            self.prompt|
            self.model|
            StrOutputParser()
        )

        res = chain.invoke(user_message)
        return res
    
def main():
    chat = RagBot()
    chat.load_data()
    res = chat.rag("Cuộc chiến tranh nhà Ngô chống lại quân đội nước nào")
    print(res)

if __name__ == '__main__':
    main()