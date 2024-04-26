from langchain_core.tools import tool

class Tool:

    def __init__(self):
        pass

    @tool
    def talk(question: str) -> str:
        "This tool is designed to respond to casual conversation. When a user engages in informal chat, the chatbot will use this tool to generate responses that maintain a friendly and conversational tone."
        return 'talk'
    # @tool
    # def rag(question: str) -> str:
    #     "RAG (Retrieval Augmented Generation) is a tool designed to assist users with inquiries related to course content or complex topics. When users have questions that require detailed explanations or need guidance on specific subjects within a course, they can use this tool. The chatbot utilizes data retrieval mechanisms to find relevant information and provides comprehensive support by addressing the user's inquiries and offering helpful guidance."
    #     return 'rag'

    @tool
    def query(question: str) -> str:
        "The Query tool is used to retrieve specific information from the database based on user input. It is suitable for inquiries related to a user's schedule, assignments, quizzes, courses or any other pertinent information."
        return 'query'
    
    @tool
    def rag(question: str) -> str:
        "RAG (Retrieval Augmented Generation) is a tool designed to assist users with inquiries related to find information about ours source information."
        return 'rag'


