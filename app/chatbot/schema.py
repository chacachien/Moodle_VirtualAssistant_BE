from langchain_core.pydantic_v1 import BaseModel, Field

class ToolSchema(BaseModel):
    name: str = Field(description="The name of the tool.")
    arguments: str = Field(description="The entire user input question message received.")

class Result(BaseModel):
    question: str = Field(description="question")
    answer: str = Field(description="answer")

# class Respon(BaseModel):
#     req: Optional[str] = Field(..., description = "The request from the user") 
#     Answer: Optional[str] = Field(..., description = "The answer from the model")
