from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
import config
from app.database import get_db
import app.utils.users as users
from datetime import date

router = APIRouter()

@router.get("/login")
def loginPage(request: Request):
    return config.templates.TemplateResponse(
                request=request,
                name="login.html",
            )
    
@router.post("/login")
async def login(request: Request, username:str= Form(...), password:str= Form(...)):
    return {username, password}

@router.get("/create_user")
def createUserPage(request:Request):
    return config.templates.TemplateResponse(
                request=request,
                name="create_account.html"
            )

@router.post("/create_user")
async def createUser(request:Request, 
               username:str= Form(...), 
               full_name:str= Form(...), 
               password:str= Form(...), 
               password_confirm:str= Form(...), 
               date_of_birth:date= Form(...)
               ):
    
    if password != password_confirm:
        return {"error": "passwords do not match"}
    
    hashedPassword = users.getPasswordHash(password)
