from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

class RootBot:
    def __init__(self):
        load_dotenv(override=True)
        #self.model = ChatGoogleGenerativeAI(model="gemini-1.0-pro", temperature=0.3)
        self.model_gg_1 = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest")
        self.model1_5 = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
        # repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        # self.modelmi = HuggingFaceHub(
        #   repo_id=repo_id, 
        #   model_kwargs={"temperature": 0.2, "top_k": 50}, 
        #   huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY')
        # )
        self.model = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest")
        self.model_openai = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0,  api_key=os.getenv("OPENAI_API_KEY"), max_tokens=1000)
        self.groq = ChatGroq(
                    #model="mixtral-8x7b-32768",
                    #model = "llama3-groq-8b-8192-tool-use-preview",
                    #model ="llama3-70b-8192",
                    model = "gemma2-9b-it",
                    #model = ""
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                    )

def main():
    import time
    # bot = RootBot()
    # response = bot.model.invoke(message)
    # print(response)

    message = "What are some of the pros and cons of Python as a programming language?"
    bot = RootBot()
    s = time.time()
    t = 0
    while True:
        message = input("user: ")
        s = time.time()
        response = bot.groq.invoke(message)
        e = time.time()
        print("TIME: ", e-s)
        print(response.content)
    
    
if __name__ == "__main__":
    main()