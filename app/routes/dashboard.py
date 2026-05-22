from fastapi import APIRouter, Request, Depends, Form
import config
from app.utils.projects import createProjectList
from app.database import get_db, AsyncSession
from decimal import Decimal
from app.models.projects import Projects

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
    
#protected route only admin use the dependency
@router.get("/create_project")
def createProjectPage(request: Request):
    return config.templates.TemplateResponse(
        context={
            "project": None,
        },
        request=request,
        name="create_project.html"
    )
    
#protected route only admin use the dependency
@router.post("/create_project")
def createProject(request: Request, 
                  project_name: str=Form(...),
                  description: str=Form(""),
                  expected_budget: Decimal=Form(...)):
    #TODO: implement checks first (if name is taken), and actual use proper values
    project = Projects(
        id = 1,
        name = project_name,
        description = description,
        expected_budget = expected_budget,
        status = "pending",
        supervisor_id = None, #TODO: set to user.id or user.employeeid (need to get user from dependency)
        finished_at = None,     
    )
    return 1