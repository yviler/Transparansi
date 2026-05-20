from fastapi import Request
import typing

def flash(request: Request, message: typing.Any, category:str="") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})
    
def getFlashedMessages(request: Request):
    return request.session.pop("_messages") if "_messages" in request.session else []