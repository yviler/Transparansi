from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating  import Jinja2Templates
from app.routes import dashboard

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))
templates = Jinja2Templates(directory="templates")

app.include_router(dashboard.router)

@app.get("/")
def index():
    return RedirectResponse(url="/dashboardPage")