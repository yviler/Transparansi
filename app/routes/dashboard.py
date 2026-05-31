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
    #TODO: not projectList, but personalProject (project where we are the supervisor/where we have tasks)
    assignedProjects = None
    
    return config.templates.TemplateResponse(
        context={
            "user": currentUser,
            "personalProjects": assignedProjects
        },
        request=request,
        name="dashboard.html",
    )