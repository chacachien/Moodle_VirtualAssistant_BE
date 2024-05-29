from fastapi import APIRouter
from app.api.api_v0.endpoints.api_healthcheck import router as health_check_router
from app.api.api_v0.endpoints.message_api import router as message_router
#from app.api.api_v1.endpoints.task_api import router as task_router
router = APIRouter()

router.include_router(health_check_router,prefix='/v0', tags=["health_check"])
router.include_router(message_router,prefix='/v0',  tags=["message_chatbot"])
#router.include_router(task_router, tags=["task"])