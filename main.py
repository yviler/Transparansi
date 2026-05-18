from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.routes import login

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login.router)

@app.get("/")
def index():
    return RedirectResponse(url="/login")