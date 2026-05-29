from fastapi import APIRouter, Request, Depends, Form
import config
from app.utils.projects import createProjectList
from app.database import get_db, AsyncSession
import app.utils.auth as auth
from typing import Annotated
from app.models.users import Users

router = APIRouter()

@router.get("/dashboard")
async def dashboardPage(request: Request, 
                        currentUser: Annotated[Users, Depends(auth.currentUser)],
                        db:AsyncSession = Depends(get_db)):
    projectList = await createProjectList(db)
    return config.templates.TemplateResponse(
        context={
            "user": currentUser,
            "projects": projectList,
        },
        request=request,
        name="dashboard.html",
    )