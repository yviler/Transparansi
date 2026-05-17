from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def dashboardPage():
    return {"message": "nah"}