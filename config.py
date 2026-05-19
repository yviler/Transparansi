from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import app.utils.sys as sys

load_dotenv()
templates = Jinja2Templates(directory="templates")
templates.env.globals['get_flashed_messages'] = sys.get_flashed_messages

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")