from fastapi import APIRouter
from .endpoints.api_healthcheck import router as health_check_router
from .endpoints.message_api import router as message_router
router = APIRouter()

router.include_router(health_check_router, tags=["health_check"])
router.include_router(message_router, tags=["message_chatbot"])