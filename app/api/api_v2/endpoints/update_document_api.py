from sre_constants import SUCCESS
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from starlette.responses import JSONResponse
from starlette import status
from app.db.db import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
#from app.services.chat_service import ChatService
from typing import Annotated
import logging
from app.models.message_model import *
from app.services.auth_service import auth_wrapper
from starlette.requests import Request
from fastapi.responses import StreamingResponse

from app.chatbot.ragBot.data import LoadData
from app.chatbot.ragBot.pgData import LoadData as LoadDataPostgre


logger = logging.getLogger()
router = APIRouter()


@router.get("/document/all")
async def update_all_document(
                    # chatid: Annotated[int | None, Query()]=None,
                    # chat_service: ChatService = Depends(), 
                    # session:AsyncSession=Depends(get_session),
                    #user=Depends(auth_wrapper)
                    ):
    # if user == 'fail':
    #     raise HTTPException(status_code=401, detail="Invalid token")
    data = LoadData()
    data.upload_all_label()
    return "update success!"


@router.get("/documentpostgre/all")
async def update_all_document(
                    # chatid: Annotated[int | None, Query()]=None,
                    # chat_service: ChatService = Depends(), 
                    # session:AsyncSession=Depends(get_session),
                    #user=Depends(auth_wrapper)
                    ):
    # if user == 'fail':
    #     raise HTTPException(status_code=401, detail="Invalid token")
    data = LoadDataPostgre()
    data.upload_all_label()
    return "update into postgre success!"








