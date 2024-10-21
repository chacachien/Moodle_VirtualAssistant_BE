import uvicorn

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.api.api_v2.api import router

from app.helpers.exception_handler import CustomException, http_exception_handler

import logging
from app.chatbot.taskbot.main import TaskHandle


#from fastapi_utils.timing import add_timing_middleware, record_timing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)



logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
def get_application() -> FastAPI:

    app = FastAPI(
        title= settings.PROJECT_NAME,
        description='''
        This is a backend service for the FastAPI project.
        The service is a virtual assistant that can help you with your daily tasks.
        It's actually a chat bot.
        '''
    )


    # origins = [
    #     "http://localhost:3000",
    #     "http://localhost:8000",
    #     "http://localhost:5000",
    #     # Add any other origins you want to allow
    # ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix=settings.API_V2_STR)
    app.add_exception_handler(CustomException, http_exception_handler)

    return app

app = get_application()