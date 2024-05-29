from ast import Str
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

def get_url():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    server = os.getenv("POSTGRES_SERVER")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    return f"mysql+aiomysql://{user}:{password}@{server}/{db}"

def get_url_notsync():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    server = os.getenv("POSTGRES_SERVER")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    return f"mysql+mysqlconnector://{user}:{password}@{server}/{db}"
    # use port 
    #return f"mysql+mysqlconnector://{user}:{password}@{server}:{port}/{db}"
    #return f'postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}'
class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    #SECRET_KEY: str = os.getenv("SECRET_KEY")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    DATABASE_URL: str = get_url()
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # one week
    ALGORITHM: str= "HS256"
    LOGGING_CONFIG_FILE:str = os.path.join(BASE_DIR, "logging.ini")
settings = Settings()
