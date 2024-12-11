from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

from openai import api_key

from langchain_google_genai import GoogleGenerativeAI
class RootBot:
    def __init__(self):
        load_dotenv(override=True)
        #self.model = ChatGoogleGenerativeAI(model="gemini-1.0-pro", temperature=0.3)
        #self.model_gg_1 = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest")
        self.model_gemini_1_5 = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
        # repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        # self.modelmi = HuggingFaceHub(
        #   repo_id=repo_id, 
        #   model_kwargs={"temperature": 0.2, "top_k": 50}, 
        #   huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY')
        # )
        #self.model = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest")

        self.model_openai = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0,  api_key=os.getenv("OPENAI_API_KEY"), max_tokens=1000)
        self.model_openai4 = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"), max_tokens=1000)
        self.groq = ChatGroq(
                    #model="mixtral-8x7b-32768",
                    #model = "llama3-groq-8b-8192-tool-use-preview",
                    #model ="llama3-70b-8192",
                    model = "gemma2-9b-it",
                    #model = "llama3-8b-8192",
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                    api_key=os.getenv("GROQ_API_KEY"),
                    streaming=True
        )
        self.claude3_5 = ChatAnthropic(model='claude-3-5-sonnet-20241022', api_key=os.getenv("CLAUDE_API_KEY"))
        
def main():
    import time
    from langchain_core.tools import Tool
    from langchain_google_community import GoogleSearchAPIWrapper
    message = "What are some of the pros and cons of Python as a programming language?"
    bot = RootBot()
    
    search = GoogleSearchAPIWrapper()

    def top5_results(query):
        return search.results(query, 5)


    tool = Tool(
        name="Google Search Snippets",
        description="Search Google for recent results.",
        func=top5_results,
    )
    s = time.time()
    t = 0
    while True:
        message = input("user: ")
        s = time.time()
        response = tool.run(message)
        e = time.time()
        print("TIME: ", e-s)
        print(response)

    # import os
    # import time
    # from groq import Groq
    # load_dotenv(override=True)
    #
    # client = Groq(
    #     api_key=os.getenv("GROQ_API_KEY"),
    # )
    # s = time.time()
    # t = 0
    # while True:
    #     message = input("user: ")
    #     s = time.time()
    #
    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": message,
    #             }
    #         ],
    #         model="llama3-8b-8192",
    #     )
    #
    #     print(chat_completion.choices[0].message.content)
    #     e = time.time()
    #     print("TIME: ", e-s)

    
if __name__ == "__main__":
    main()