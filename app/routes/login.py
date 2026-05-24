from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
import config
import app.utils.flash as flash
from app.database import get_db, AsyncSession
import app.utils.users as users
from datetime import date
from app.models.users import Users
import secrets
import app.utils.auth as auth


router = APIRouter()

@router.get("/login")
def loginPage(request: Request):
    return config.templates.TemplateResponse(
                context={
                    "username": None
                },
                request=request,
                name="login.html",
            )
    
@router.post("/login")
async def login(request: Request, 
                response: Response,
                username:str= Form(...), 
                password:str= Form(...), 
                db:AsyncSession = Depends(get_db),
            ):
    user = await users.doesUserExist(username, db)
    if not user:
        flash.flash(request, "username does not exist", "error")
        return config.templates.TemplateResponse(
            context={
                "username": username
            },
            request=request,
            name="login.html",
        )
    
    userPassHash = user.password_hash
    if users.verifyPasswordWithHash(password, userPassHash):
        token = secrets.token_hex(32)
        await auth.insertSessionToken(user, token, db)
        redirect = RedirectResponse(url="/dashboard", status_code=303)
        redirect.set_cookie(key="session_id", value=token, httponly=True)
        return redirect
    else:
        flash.flash(request, "incorrect password", "error")
        return config.templates.TemplateResponse(
            context={
                "username": username
            },
            request=request,
            name="login.html",
        )
    
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
        flash.flash(request, "passwords do not match", "error")
        return config.templates.TemplateResponse(
            request=request,
            name="create_account.html",
            context={
                "data": {"username": username,
                         "full_name": full_name,
                         "date_of_birth":date_of_birth
                         }
            },
        )
            
    hashedPassword = users.getPasswordHash(password)

    new_user = Users(
            username = username,
            password_hash=hashedPassword,
            full_name=full_name,
            date_of_birth=date_of_birth,
            employee_id=secrets.token_hex(4).upper()
        )
    

    if await users.doesUsernameExist(username, db):
        flash.flash(request, "username already exists", "error")
        return config.templates.TemplateResponse(
            request=request,
            name="create_account.html",
            context={
                "data": new_user
            },
        )
    try:
        await users.createNewUser(new_user, db)
    except Exception:
        return config.templates.TemplateResponse(
                    request=request,
                    name="error.html",
                    )
    flash.flash(request, f"user {username} successfully created", "success")
    return config.templates.TemplateResponse(
        context={
            "username": None,
        },
        request=request,
        name="login.html",
    )