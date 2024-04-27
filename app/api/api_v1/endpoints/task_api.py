# from fastapi import APIRouter, Depends, HTTPException, Query, Path
# from starlette.responses import JSONResponse
# from starlette import status
# from app.db.db import get_session
# from sqlalchemy.ext.asyncio.session import AsyncSession
# from app.api.api_v1.services.chat_service import ChatService
# from typing import Annotated
# import logging
# from app.models.message_model import *

# logger = logging.getLogger()
# router = APIRouter()
# from fastapi import FastAPI

# from app.api.api_v1.services.schedule import app as app_rocketry

# app = FastAPI()
# session = app_rocketry.session
# # Create some routes:

# @app.get("/my-route")
# async def get_tasks():
#     # We can modify/read the Rocketry's runtime session
#     return session.tasks

# @app.post("/my-route")
# async def manipulate_session():
#     for task in session.tasks:
#         task["status"] = "completed"
#     return session.tasks


