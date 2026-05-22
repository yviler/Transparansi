from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import app.utils.flash as flash
from jinja2 import Environment


load_dotenv()
templates = Jinja2Templates(directory="templates")
templates.env.globals['getFlashedMessages'] = flash.getFlashedMessages

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")