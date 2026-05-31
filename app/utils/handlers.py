from fastapi import Request, HTTPException
import app.utils.flash as flash
import config

async def httpExceptionHandler(request: Request, exception: HTTPException):
    return config.templates.TemplateResponse(
        request=request,
        context={
            "error": exception,
        },
        name="error.html"
    )