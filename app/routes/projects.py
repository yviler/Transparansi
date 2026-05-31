from fastapi import APIRouter, Request, Depends, Form
import config
from fastapi.responses import RedirectResponse
from decimal import Decimal
from app.models.projects import Projects
from app.database import get_db, AsyncSession
import app.utils.flash as flash
import app.utils.auth as auth
import app.utils.projects as projects
from typing import Annotated
from app.models.users import Users
from sqlalchemy.exc import SQLAlchemyError
import app.utils.wallets as wallet

router = APIRouter()


@router.get("/create_project")
async def createProjectPage(request: Request, 
                      account: Annotated[Users, Depends(auth.verifySession)],
                      currentUser: Annotated[Users, Depends(auth.currentUser)],
                      requiredRoles: Annotated[Users, Depends(auth.roleRequired('admin'))],
                      db:AsyncSession = Depends(get_db)
                      ):
    
    walletList = await wallet.getActiveUnusedWalletList(db)

    if not walletList:
        flash.flash(request,
                    "No unused wallets available, please create a wallet first",
                    "error")
        return RedirectResponse(url='/dashboard', status_code=303)

    return config.templates.TemplateResponse(
        context={
            "project": None,
            "user": currentUser,
            "wallets": walletList
        },
        request=request,
        name="create_project.html"
    )
    
@router.post("/create_project")
async def createProject(request: Request,
                        account: Annotated[Users, Depends(auth.verifySession)],
                        currentUser: Annotated[Users, Depends(auth.currentUser)],
                        requiredRoles: Annotated[Users, Depends(auth.roleRequired('admin'))],
                        project_name: str=Form(...),
                        description: str=Form(""),
                        wallet_id: str=Form(...),
                        expected_budget: Decimal=Form(...),
                        db:AsyncSession = Depends(get_db)
                        ):


    if await projects.getProjectByName(db, project_name):
        flash.flash(request,f"Project {project_name} already exists", "error")
        return config.templates.TemplateResponse(
            context={
                "project": {
                    "description": description,
                    "expected_budget": expected_budget,
                }
            },
            request=request,
            name="create_project.html"
        )
    
    new_project = Projects(
        project_name = project_name,
        description = description,
        expected_budget = expected_budget,
        status = "pending",
        wallet_id=wallet_id,
        supervisor_id = currentUser.id,
        finished_at = None,     
    )

    try:
        await projects.insertProject(db, new_project)
        flash.flash(request, f"Successfully created project: {project_name}", "success")
        return RedirectResponse(url='/dashboard', status_code=303)
    except SQLAlchemyError as e:
        flash.flash(request, f"Error creating project: {e}", "error")
        return config.templates.TemplateResponse(
            context={
                "project": {
                    "project_name": project_name,
                    "description": description,
                    "expected_budget": expected_budget,
                }
            },
            request=request,
            name="create_project.html"
        )
    
@router.get("/projects")
async def projectDashboard(request: Request,
                            currentUser: Annotated[Users, Depends(auth.currentUser)],
                            db:AsyncSession = Depends(get_db)):
    
    projectList= await projects.createProjectList(db)

    return config.templates.TemplateResponse(
        context={
            "projects": projectList
        },
        request=request,
        name="project_dashboard.html",
    )