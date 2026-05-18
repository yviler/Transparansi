from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

load_dotenv()
templates = Jinja2Templates(directory="templates")

DATABASE_URL = os.getenv("DATABASE_URL")
