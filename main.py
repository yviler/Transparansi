from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.routes import login, dashboard, projects
from starlette.middleware.sessions import SessionMiddleware
import config
from app.utils.handlers import httpExceptionHandler

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login.router)
app.include_router(dashboard.router)
app.include_router(projects.router)

app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)
app.add_exception_handler(HTTPException, httpExceptionHandler)

@app.get("/")
def index():
    return RedirectResponse(url="/login")