from hmac import new
import token

from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import GoogleDriveLoader
from numpy import mat
from pinecone import PodSpec, Pinecone
from langchain_community.vectorstores import Pinecone as PC
from sympy import Q
from app.core.config import get_url_notsync
from sqlalchemy import create_engine, MetaData, Table, text
from app.services.label_service import LabelService
from bs4 import BeautifulSoup
from pyvi.ViTokenizer import tokenize, spacy_tokenize
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
        self.index_name = "ragbot"
        self.folder_id = '10ZN2ztM_WC00CyktKSZENS2LULbdJkNP'
        DATABASE_URL = get_url_notsync()
        self.engine = create_engine(DATABASE_URL)


###
            # from langchain_community.embeddings import HuggingFaceEmbeddings

            # model_name = "sentence-transformers/all-mpnet-base-v2"
            # model_kwargs = {'device': 'cpu'}
            # encode_kwargs = {'normalize_embeddings': False}
            # hf = HuggingFaceEmbeddings(
            #     model_name=model_name,
            #     model_kwargs=model_kwargs,
            #     encode_kwargs=encode_kwargs
            # )
###
        self.vietnamese_model = 'dangvantuan/vietnamese-embedding'
        ## use tokenize vietnamese-embedding from pyvi.vitokenizer
        self.embeddings = HuggingFaceEmbeddings(model_name=self.vietnamese_model)

        #self.embeddings = HuggingFaceEmbeddings(model_name=self.vietnamese_model)
        self.docsearch = None
        self.PC = None

    def load_data(self):
        res = LabelService.get_all_label()

        for row in res:
            content_soup = BeautifulSoup( row['intro'], 'html.parser')
            content_text = content_soup.get_text()
            row['intro'] = content_text
        return res # return list of dict
    
    def clean_data(self, data):
        try: 
            data['intro'] = BeautifulSoup(data['intro'], 'html.parser').get_text()
            
        except:
            print('Cannot convert this data to text')
        data['intro'] = str(tokenize(data['intro']))
        return data


    def split_data(self, data: str):

        # text_splitter = CharacterTextSplitter(
        #         # separator="\n\n",
        #         chunk_size=100,
        #         chunk_overlap=2,
        #         length_function=len,
        #         is_separator_regex=False,
        # )
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[
                "\n\n",
                "\n",
                " ",
                ".",
                ",",
                "\u200b",  # Zero-width space
                "\uff0c",  # Fullwidth comma
                "\u3001",  # Ideographic comma
                "\uff0e",  # Fullwidth full stop
                "\u3002",  # Ideographic full stop
                "",
            ],
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
        docs = text_splitter.split_text(data)
        return docs

    def create_index(self):

        if self.index_name not in self.pc.list_indexes().names():
        # Create new Index
            self.pc.create_index(name=self.index_name, metric="euclidean", dimension=768, spec=PodSpec(environment="gcp-starter"))
            # docsearch = PC.from_texts(self.docs, self.embeddings, index_name=self.index_name)
            
    def embed_data(self):

        docsearch = PC.from_existing_index(self.index_name, self.embeddings)
        self.docsearch = docsearch
        return docsearch
    

    def update_data(self, data):
        '''
            texts: Iterable[str],
            metadatas: Optional[List[dict]] = None,
            ids: Optional[List[str]] = None,
            namespace: Optional[str] = None,
            batch_size: int = 32,
            embedding_chunk_size: int = 1000,
            ------
            data =  {
                'id':,
                'course':,
                'name':,
                'intro': string
            }
        '''
        # print('data: ', data)
        clean_data = self.clean_data(data)

        # print('CLEAN DATA: ', clean_data)
        clean_data['intro'] = self.split_data(clean_data['intro']) 
        pc = PC(index= self.pc.Index(name=self.index_name), embedding=self.embeddings, text_key='text')


        id_list = [f'doc{clean_data['id']}_chunk'+str(j) for j in range(len(clean_data['intro']))]
        
        pc.add_texts(
            texts = clean_data['intro'],
            ids = id_list,
            metadatas= [{'title': clean_data['name'], 'course': clean_data['course'], "text":i } for i in clean_data['intro']],
            batch_size=1,
            embedding_chunk_size=1)
        
    def upload_all_label(self):
        self.create_index()
        res = self.load_data()
        [self.update_data(row) for row in res]

def main():
    def pretty_print_docs(docs):
        print(
            f"\n{'-' * 100}\n".join(
                [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
            )
        )

    data = LoadData()
    data.upload_all_label()

if __name__ == "__main__":
    main()
    