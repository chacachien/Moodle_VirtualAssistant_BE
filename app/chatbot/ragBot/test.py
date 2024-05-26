# from sentence_transformers import SentenceTransformer
# from pyvi.ViTokenizer import tokenize

# sentences = ["Hà Nội là thủ đô của Việt Nam", "Đà Nẵng là thành phố du lịch"]
# tokenizer_sent = [tokenize(sent) for sent in sentences]
# print(tokenizer_sent)
# model = SentenceTransformer('dangvantuan/vietnamese-embedding')
# embeddings = model.encode(tokenizer_sent)
# print(embeddings)
# import json

# # Your JSON list (replace with your actual data)
# json_list = [
#     {'name': 'Computer vision', 'summary': 'Học về máy tính nhìn nhận...'},
#     {'name': 'Test Sort Test', 'summary': 'Test course 1...\nLorem ipsum...'}
# ]

# # Convert the list to a JSON string
# json_string = json.dumps(json_list)

# Print the JSON string
# print(type(json_string))

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI






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
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)