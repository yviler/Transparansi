from fastapi import APIRouter, Request, Depends
import config
from app.utils.projects import createProjectList
from app.database import get_db, AsyncSession

router = APIRouter()

@router.get("/dashboard")
async def dashboardPage(request: Request, db:AsyncSession = Depends(get_db)):
    projectList = await createProjectList(db)
    return config.templates.TemplateResponse(
        context={
            "projects": projectList,
        },
        request=request,
        name="dashboard.html",
    )