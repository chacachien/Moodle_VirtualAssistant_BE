from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import GoogleDriveLoader
from numpy import mat
from pinecone import PodSpec, Pinecone
from langchain_community.vectorstores import Pinecone as PC
from app.core.config import get_url_notsync
from sqlalchemy import create_engine, MetaData, Table, text


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

        data_clear = []
        from bs4 import BeautifulSoup

        with self.engine.connect() as connection:
            # Execute the query
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
        # store into file txt
        with open('app/chatbot/ragBot/new.txt', 'w') as file:
            file.write(str(merged_string))
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
    # search = data.embed_data()
    # data.update_data()
    query = "Cuộc chiến tranh nhà Ngô"

    # res = data.docsearch.similarity_search(
    #     query,  # our search query
    #     k=3,  # return 3 most relevant docs
    # )
    # res = data.docsearch.as_retriever(search_type='mmr')
    # mat = res.invoke(query)
    # pretty_print_docs(mat)
    # res = data.docsearch.max_marginal_relevance_search(query, k=3, fetch_k=10)
    # pretty_print_docs(res)

    index = data.pc.Index(name=data.index_name)
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

    res = index.query(
            vector=[0.1]*768,
        filter = {
            'course': 1
        },
        top_k=1,
        include_metadata=True
    )
    print(res)

if __name__ == "__main__":
    main()