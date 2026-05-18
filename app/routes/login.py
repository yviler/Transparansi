from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import config

router = APIRouter()

@router.get("/login")
def loginPage(request: Request):
    return config.templates.TemplateResponse(
                request=request,
                name="login.html",
            )
    
@router.post("/login")
async def login(request: Request, username:str= Form(...), password:str= Form(...)):
    return {username, password, config.DATABASE_URL}