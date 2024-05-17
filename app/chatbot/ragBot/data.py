from hmac import new
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import GoogleDriveLoader
from numpy import mat
from pinecone import PodSpec, Pinecone
from langchain_community.vectorstores import Pinecone as PC
from app.core.config import get_url_notsync
from sqlalchemy import create_engine, MetaData, Table, text
from app.services.label_service import LabelService
from bs4 import BeautifulSoup

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

        self.embeddings = HuggingFaceEmbeddings()
        self.docsearch = None
        self.PC = None

    def load_data(self):
        res = LabelService.get_all_label()
        data_clear = []
        for row in res:
            content_soup = BeautifulSoup( row['intro'], 'html.parser')
            content_text = content_soup.get_text()
            row['intro'] = content_text
        return res 
    
    def clean_data(self, data):
        
        data['intro'] = BeautifulSoup(data['intro'], 'html.parser').get_text()
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
        '''
        clean_data = self.clean_data(data)
        docs = [{'id': text['id'],'course':text['course'], 'name': text['name'],'intro': self.split_data(text['intro'])} for text in clean_data]
        pc = PC(index= self.pc.Index(name=self.index_name), embedding=self.embeddings, text_key='text')

        for i in docs:
            id_list = [f'doc{i['id']}_chunk'+str(j) for j in range(len(i['intro']))]
            print("LIST ID: ",id_list)
            # print id vs intro 
            [pc.add_texts(
                texts = [j[1]],
                ids = [j[0]],
                metadatas= [{'title': i['name'], 'course': i['course'], "text": j[1]}],
                batch_size=64,
                embedding_chunk_size=1000) for j in zip(id_list, i['intro'])]
        print('Data updated')


    def set_up(self):
        self.docs = self.load_data()
        self.docs = [{'id': text['id'],'course':text['course'], 'name': text['name'],'intro': self.split_data(text['intro'])} for text in self.docs]
        self.create_index()
        self.update_data(self.docs)


def main():
    def pretty_print_docs(docs):
        print(
            f"\n{'-' * 100}\n".join(
                [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
            )
        )

    # res = data.load_data()


    # for i in res:
    #     i['intro'] = data.split_data(i['intro'])

    # # upload data
    # data.update_data(res)


        
    # # #store into file txt
    # with open('data.txt', 'w') as file:
    #     file.write(str(res))
    
    # data.split_data()
    # search = data.embed_data()
    # data.update_data()


    # res = data.docsearch.similarity_search(
    #     query,  # our search query
    #     k=3,  # return 3 most relevant docs
    # )
    # res = data.docsearch.as_retriever(search_type='mmr')
    # mat = res.invoke(query)
    # pretty_print_docs(mat)
    # res = data.docsearch.max_marginal_relevance_search(query, k=3, fetch_k=10)
    # pretty_print_docs(res)

    # res = index.fetch(['c42951d4-f3fa-4893-9f22-ad9674ff50e2'])

    # #convert res to json
    # import json
    # res = json.loads(res)

    # # get the keys of this json
    # keys = res.keys()
    # print(keys)

    # update data
    # res = index.update(
    #     id = 'c42951d4-f3fa-4893-9f22-ad9674ff50e2',
    #     set_metadata= {'title': 'Tác giả', 'text':'(Hồ Xuân Hương, Bà Huyện Thanh Quan, Đoàn Thị Điểm, Ngọc Hân Công Chúa), có những đóng góp vô cùng quan trọng cho văn học chữ Nôm, có rất nhiều tác phẩm văn học chữ Nôm, có khá nhiều nghiên cứu về các tác phẩm văn học chữ Nôm khác, góp phần cho sự phát triển hưng thịnh của văn học chữ Nôm. Trong giai đoạn phát triển chữ Quốc Ngữ và chữ Nôm, chữ Nôm đã được sử dụng trong các tác phẩm thơ ca trào phúng khác nhau, thể hiện thói hóm hỉnh vốn có của người Việt.Lục Vân TiênLà tác phẩm nổi tiếng nhất của Nguyễ``n Đình Chiểu, Lục Vân Tiên không chỉ là một tác phẩm văn học chữ Nôm ca ngợi lòng trung hiếu của một đấng nam nhi, sự vận hành của âm-dương, cũng như câu nói \"qua cơn bỉ cực đến hồi thái lai\" cũng được thể hiện rõ nét trong tác phẩm. Lý tưởng tin tưởng vào sự vận hành của vũ trụ, của quy luật nhân quả đã được Nguyễn Đình Chiểu khéo léo thể hiện để cuộc đời chàng Lục Vân Tiên tuy thăng trầm nhưng cũng đến được bến bờ hạnh phúc.Tỳ Bà TruyệnĐược chuyển thể từ một vở kịch Trung Hoa là Tỳ Bà Ký, Tỳ Bà Truyện là một thể loại văn học chữ Nôm dạng truyện thơ, một thể loại khá nổi tiếng trong giới văn chương đương thời. Tỳ Bà Truyện là một câu chuyện ngụ ngôn mang tính giáo huấn, đề cao cái đẹp thủy chung, tận tâm của người con dâu tên Ngũ Nương. Trải qua bao thăng trầm bể dâu, cô nhất định làm tròn trách nhiệm người con dâu, cũng vì thế mà được người đời ngưỡng mộ vì đức hy sinh và sự tận tụy của mình.Quan Âm Thị KínhKhác với tác phẩm chèo cùng tên, truyện thơ Quan Âm Thị Kính vốn là một tác phẩm văn học chữ Nôm mang đề tài tôn giáo để kể về nguồn gốc của Phật Bà Quan Âm Nghìn Mắt Nghìn Tay. Trong tác phẩm truyện thơ Quan Âm Thị Kính, nhân vật chính là công chúa Diệu Thiên, vì lòng từ bi quyết chí tu hành, bà đã trở thành Quan Âm. Nhiều lần nàng chịu chết thay vì từ bỏ đức tin, lòng từ bi ấy đã bao trùm cả vong hồn dưới âm phủ. Cuối cùng, bà chấp nhận bị cắt đứt tay mình để cứu phụ thân, người luôn tìm cách hãm hại bà.'}
    # )
    # print(res)
    # des = data.pc.describe_index('langchain-demo1')
    # print(des)
    data = LoadData()
    # data.create_index()
    # texts = data.load_data()

    # texts = [{'id': text['id'],'course':text['course'], 'name': text['name'],'intro': data.split_data(text['intro'])} for text in texts]

    # data.update_data(texts)

    index = data.pc.Index(name=data.index_name)
    query = "tên các tác phẩm chữ nôm được nêu ra trong bài"
    query = 'tên các tác giả có các sáng tác thơ nôm'
    query = 'thời gian ra đời của chữ nôm'
    vectoreStore = PC(index = index, embedding= data.embeddings, text_key='text')
    res = vectoreStore.similarity_search(
        query = query,
        k = 4,
        filter={
            'course': 5,
        }
    )
    print(res)
    pretty_print_docs(res)
if __name__ == "__main__":
    main()