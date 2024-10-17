
import math

from langchain_text_splitters import  RecursiveCharacterTextSplitter
from app.core.config import  get_url_vector
from sqlalchemy import create_engine, MetaData, Table, text
from app.services.label_service import LabelService
from bs4 import BeautifulSoup
from pyvi.ViTokenizer import tokenize, spacy_tokenize
import dotenv
import psycopg2
import pgvector
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
from langchain_openai import OpenAIEmbeddings

import numpy as np

dotenv.load_dotenv()


class LoadData:
    def __init__(self):
        self.docs = None
        #self.index_name = "ragbot"
        #self.folder_id = '10ZN2ztM_WC00CyktKSZENS2LULbdJkNP'
        DATABASE_URL = get_url_vector()
        self.engine = create_engine(DATABASE_URL)
        self.conn = psycopg2.connect(DATABASE_URL)

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
        #self.embeddings = HuggingFaceEmbeddings(model_name=self.vietnamese_model)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=768)

        #self.embeddings = HuggingFaceEmbeddings(model_name=self.vietnamese_model)

    def load_data(self):
        res = LabelService.get_all_label()

        for row in res:
            content_soup = BeautifulSoup(row['intro'], 'html.parser')
            content_text = content_soup.get_text()
            row['intro'] = content_text
        return res  # return list of dict

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

    def get_embedding(self, document):
        data = self.embeddings.embed_query(document)
        return data

    def update_data(self, data):
        # print('data: ', data)
        clean_data = self.clean_data(data)
        print("clean: ", clean_data)
        # print('CLEAN DATA: ', clean_data)
        clean_data['intro'] = self.split_data(clean_data['intro'])
        #pc = PC(index= self.pc.Index(name=self.index_name), embedding=self.embeddings, text_key='text')

        #id_list = [f'doc{clean_data['id']}_chunk'+str(j) for j in range(len(clean_data['intro']))]
        data_list = [
            (
                clean_data['course'],
                clean_data['name'],  # Title
                f'doc{clean_data["id"]}_chunk{j}',  # URL (or document identifier for chunk)
                intro_chunk,  # Content
                len(intro_chunk.split()),  # Tokens (word count in the chunk)
                np.array(self.get_embedding(intro_chunk)),  # data type: vector
                clean_data['id']
            )
            for j, intro_chunk in enumerate(clean_data['intro'])
        ]
        embedding = np.array(self.get_embedding(clean_data['intro'][0]))
        print("Embedding shape:", embedding.shape)

        register_vector(self.conn)
        cur = self.conn.cursor()
        execute_values(cur, """INSERT INTO embeddings_v2 (courseid, title, url, content, tokens, embedding, labelid) VALUES %s ON CONFLICT (url) 
                                DO UPDATE SET 
                                courseid = excluded.courseId,
                                title = excluded.title,
                                content = excluded.content,
                                tokens = excluded.tokens,
                                embedding = excluded.embedding,
                                labelid = excluded.labelid
                                """, data_list)

        self.conn.commit()

    def upload_all_label(self):
        print("start load data")
        res = self.load_data()
        print("start update data")
        [self.update_data(row) for row in res]
        self.create_index_for_db()

    def create_index_for_db(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) as cnt FROM embeddings_v2;")
        num_records = cur.fetchone()[0]
        print("Number of vector records in table: ", num_records, "\n")
        # Correct output should be 129

        num_lists = num_records / 1000
        if num_lists < 10:
            num_lists = 10
        if num_records > 1000000:
            num_lists = math.sqrt(num_records)
        #use the cosine distance measure, which is what we'll later use for querying
        cur.execute(
            f'CREATE INDEX ON embeddings_v2 USING ivfflat (embedding vector_cosine_ops) WITH (lists = {num_lists});')

        self.conn.commit()


def main():
    def pretty_print_docs(docs):
        print(
            f"\n{'-' * 100}\n".join(
                [f"Document {i + 1}:\n\n" + d.page_content for i, d in enumerate(docs)]
            )
        )

    data = LoadData()
    data.upload_all_label()


if __name__ == "__main__":
    main()
