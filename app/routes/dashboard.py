from fastapi import APIRouter
from app.database import get_db, AsyncSession

router = APIRouter()

@router.get("/dashboard")
def dashboardPage():
    return {"message": "dashboard page WIP"}