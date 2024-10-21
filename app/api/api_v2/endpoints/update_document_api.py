from fastapi import APIRouter, Depends, HTTPException, Query, Path


import logging

from app.chatbot.ragBot.pgData import LoadData as LoadDataPostgre


logger = logging.getLogger()
router = APIRouter()



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








