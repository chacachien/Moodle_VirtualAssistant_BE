import uvicorn

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import router

from app.helpers.exception_handler import CustomException, http_exception_handler

import logging


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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    #app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    app.include_router(router, prefix=settings.API_V1_STR)
    app.add_exception_handler(CustomException, http_exception_handler)
    return app

app = get_application()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
