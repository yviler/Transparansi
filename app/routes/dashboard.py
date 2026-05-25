from fastapi import APIRouter, Request, Depends, Form
import config
from fastapi.responses import RedirectResponse
from app.utils.projects import createProjectList
from app.database import get_db, AsyncSession
from decimal import Decimal
from app.models.projects import Projects
import app.utils.flash as flash
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
    
@router.get("/create_project")
def createProjectPage(request: Request, 
                      account: Annotated[Users, Depends(auth.verifySession)],
                      requiredRoles: Annotated[Users, Depends(auth.roleRequired('admin'))]
                      ):
    return config.templates.TemplateResponse(
        context={
            "project": None,
        },
        request=request,
        name="create_project.html"
    )
    
@router.post("/create_project")
def createProject(request: Request,
                  account: Annotated[Users, Depends(auth.verifySession)],
                  requiredRoles: Annotated[Users, Depends(auth.roleRequired('admin'))],
                  project_name: str=Form(...),
                  description: str=Form(""),
                  expected_budget: Decimal=Form(...)
                  ):
    #TODO: implement checks first (if name is taken), and actual use proper values
    '''
    project = Projects(
        id = 1,
        name = project_name,
        description = description,
        expected_budget = expected_budget,
        status = "pending",
        supervisor_id = None, #TODO: set to user.id or user.employeeid (need to get user from dependency)
        finished_at = None,     
    )
    '''
    #flash successfully created and redirectResponse to dashboard
    flash.flash(request, "Successfully created project", "success")
    return RedirectResponse(url='/dashboard', status_code=303)