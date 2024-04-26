from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import GoogleDriveLoader
from numpy import mat
from pinecone import PodSpec, Pinecone
from langchain_community.vectorstores import Pinecone as PC
from app.core.config import get_url_notsync
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine, MetaData, Table
from langchain_core.documents import Document




import pinecone
import sys
import os
import dotenv
import ast


dotenv.load_dotenv()

class LoadData:
    def __init__(self):
        self.docs = None
        self.pc= Pinecone(
            api_key= os.getenv("PINECONE_API_KEY"),
            environment='gcp-starter'
        )
        self.index_name = "langchain-demo1"
        self.folder_id = '10ZN2ztM_WC00CyktKSZENS2LULbdJkNP'
        DATABASE_URL = get_url_notsync()
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData()
        self.embeddings = HuggingFaceEmbeddings()
        self.docsearch = None
        self.PC = None



    def load_data(self):
        # loader = GoogleDriveLoader(
        #     folder_id = self.folder_id,
        #     token_path = 'token.json',
        #     recusive = False,
        # )
        # self.docs = loader.load()

        # data = self.db.run('SELECT name, intro, content FROM mdl_page where course=4')
        # print("DATA: ", data)

        data_clear = []
        from bs4 import BeautifulSoup

        with self.engine.connect() as connection:
            # Execute the query
            from sqlalchemy import text
            query = text('SELECT name, intro FROM mdl_label')
            result = connection.execute(query)
            # Fetch all rows
            rows = result.fetchall()
            for row in rows:
                new_row = ''
                for i in range(2):
                    if i%2==0:
                        new_row +=row[i]
                        new_row += '\n'
                    else:
                        content_soup = BeautifulSoup(row[i], 'html.parser')
                        content_text = content_soup.get_text()
                        new_row += content_text
                        new_row += '\n\n'
                data_clear.append((new_row))

        merged_string = ''.join(data_clear)
        self.docs = merged_string
        return merged_string

    def split_data(self):

        text_splitter = CharacterTextSplitter(
                separator="\n\n",
                chunk_size=100,
                chunk_overlap=20,
                length_function=len,
                is_separator_regex=False,
        )

        self.docs = text_splitter.split_text(self.docs)
    
    def embed_data(self):

        # Checking Index
        docsearch = None
        if self.index_name not in self.pc.list_indexes().names():
        # Create new Index
            self.pc.create_index(name=self.index_name, metric="cosine", dimension=768, spec=PodSpec(environment="gcp-starter"))
            docsearch = PC.from_texts(self.docs, self.embeddings, index_name=self.index_name)
            
        else:
        # Link to the existing index
            print('Index already exists')
            docsearch = PC.from_existing_index(self.index_name, self.embeddings)
        self.docsearch = docsearch
        return docsearch
    
    def update_data(self):
        with open('app/chatbot/ragBot/new.txt', 'r') as text:
            new_data = text.read()
            pc = PC(index= self.pc.Index(name=self.index_name), embedding=self.embeddings, text_key='text')
            pc.add_texts(texts = [new_data])
            print('Data updated')

def main():
    def pretty_print_docs(docs):
        print(
            f"\n{'-' * 100}\n".join(
                [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
            )
        )

    data = LoadData()
    # res = data.load_data()
    # # #store into file txt
    # with open('data.txt', 'w') as file:
    #     file.write(str(res))
    
    # data.split_data()
    search = data.embed_data()
    # data.update_data()
    query = "Cuộc chiến tranh nhà Ngô"

    # res = data.docsearch.similarity_search(
    #     query,  # our search query
    #     k=3,  # return 3 most relevant docs
    # )
    # res = data.docsearch.as_retriever(search_type='mmr')
    # mat = res.invoke(query)
    # pretty_print_docs(mat)
    res = data.docsearch.max_marginal_relevance_search(query, k=3, fetch_k=10)
    pretty_print_docs(res)
if __name__ == "__main__":
    main()