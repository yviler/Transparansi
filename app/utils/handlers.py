from fastapi import Request, HTTPException
import app.utils.flash as flash

async def httpExceptionHandler(request: Request, exception: HTTPException):
    return exception.status_code