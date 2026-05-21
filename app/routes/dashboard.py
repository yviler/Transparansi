from fastapi import APIRouter, Request, Depends
import config
from app.models.users import Users
from app.utils.projects import createProjectList
from app.database import get_db, AsyncSession

router = APIRouter()

@router.get("/dashboard")
def dashboardPage(request: Request, db:AsyncSession = Depends(get_db)):
    projectList = createProjectList(db)
    return config.templates.TemplateResponse(
        context={
            "projects": projectList,
        },
        request=request,
        name="dashboard.html",
    )