import uvicorn

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import router

from app.helpers.exception_handler import CustomException, http_exception_handler

import logging
from app.chatbot.taskbot.main import TaskHandle


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
    import asyncio
    import time
    import schedule
    from datetime import datetime
    from threading import Thread

    taskBot = TaskHandle()
    async def scheduled_job():
        print('start checking')
        taskBot.run()

    async def daily_job():
        print("DAILY START")
        taskBot.daily_check()

    def schedule_checker():
        while True:
            schedule.run_pending()
            time.sleep(1)


    def run_async_function_sync( func):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func())
    

    #schedule.every(41).minutes.do(lambda: run_async_function_sync(scheduled_job))
    import pytz
    from datetime import datetime
    timezone = 'Asia/Ho_Chi_Minh'  
    scheduled_time = '16:55'

    schedule.every().day.at(scheduled_time, timezone).do(
        lambda: run_async_function_sync(daily_job))

    schedule.every(1).minutes.do(
        lambda: run_async_function_sync(scheduled_job)
    )

    Thread(target=schedule_checker).start()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    while True:
        schedule.run_pending()
