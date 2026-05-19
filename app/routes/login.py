from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
import config
import app.utils.sys as sys
from app.database import get_db, AsyncSession
import app.utils.users as users
from datetime import date
from app.models.users import Users
import secrets

router = APIRouter()

@router.get("/login")
def loginPage(request: Request):
    return config.templates.TemplateResponse(
                request=request,
                name="login.html",
            )
    
@router.post("/login")
async def login(request: Request, username:str= Form(...), password:str= Form(...)):

    await users.verifyPasswordWithHash()

    
@router.get("/create_user")
def createUserPage(request:Request):
    return config.templates.TemplateResponse(
                request=request,
                name="create_account.html",
                context={
                    "data": None,
                },
            )

@router.post("/create_user")
async def createUser(request:Request, 
                    username:str= Form(...), 
                    full_name:str= Form(...), 
                    password:str= Form(...), 
                    password_confirm:str= Form(...), 
                    date_of_birth:date= Form(...),
                    db: AsyncSession = Depends(get_db),
                    ):
            
    if password != password_confirm:
        return {"error": "passwords do not match"}
    
    hashedPassword = await users.getPasswordHash(password)

    new_user = Users(
        username = username,
        password_hash=hashedPassword,
        full_name=full_name,
        date_of_birth=date_of_birth,
        employee_id=secrets.token_hex(4).upper()
    )

    if await users.duplicateUsernames(username, db):
        sys.flash(request, "username already exists", "error")
        return config.templates.TemplateResponse(
            request=request,
            name="create_account.html",
            context={
                "data": new_user
            },
        )
    try:
        db.add(new_user)
        await db.commit()
    except Exception:
        return config.templates.TemplateResponse(
                    request=request,
                    name="error.html",
                    )
        
    return {"success": f"user {username} successfully created"}