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

router = APIRouter()


@router.get("/create_project")
def createProjectPage(request: Request, 
                      account: Annotated[Users, Depends(auth.verifySession)],
                      currentUser: Annotated[Users, Depends(auth.currentUser)],
                      requiredRoles: Annotated[Users, Depends(auth.roleRequired('admin'))]
                      ):
    return config.templates.TemplateResponse(
        context={
            "wallet": None,
            "user": currentUser,
        },
        request=request,
        name="create_wallet.html"
    )