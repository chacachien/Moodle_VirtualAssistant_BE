from fastapi import APIRouter
from app.api.api_v2.endpoints.api_healthcheck import router as health_check_router
from app.api.api_v2.endpoints.message_api import router as message_router
from app.api.api_v2.endpoints.update_document_api import router as update_document_router
from app.api.api_v2.endpoints.reminder_api import router as reminder_router

router = APIRouter()

router.include_router(health_check_router, tags=["health_check"])
router.include_router(message_router, tags=["message_chatbot"])
router.include_router(update_document_router, tags=["update_document"])

router.include_router(reminder_router, tags=["reminder"])