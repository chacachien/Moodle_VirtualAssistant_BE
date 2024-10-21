from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {"message": "I'm alive!", "Version": "1.0.0"}


