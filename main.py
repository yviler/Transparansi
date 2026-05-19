from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.routes import login
from starlette.middleware.sessions import SessionMiddleware
import config

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login.router)
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

@app.get("/")
def index():
    return RedirectResponse(url="/login")