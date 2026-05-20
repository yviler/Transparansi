from fastapi import APIRouter, Request
import config
from app.models.users import Users

router = APIRouter()

@router.get("/dashboard")
def dashboardPage(request: Request):
    return config.templates.TemplateResponse(
        context={
            
        },
        request=request,
        name="dashboard.html"
    )