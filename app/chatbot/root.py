from langchain_community.llms import HuggingFaceHub
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

class RootBot:
    def __init__(self):
        load_dotenv()
        #self.model = ChatGoogleGenerativeAI(model="gemini-1.0-pro", temperature=0.3)
        self.model = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest", temperature=0)
        self.model1_5 = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
        # repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        # self.modelmi = HuggingFaceHub(
        #   repo_id=repo_id, 
        #   model_kwargs={"temperature": 0.2, "top_k": 50}, 
        #   huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY')
        # )
        #self.model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)