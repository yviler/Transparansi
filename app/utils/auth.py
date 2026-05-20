from fastapi import Request, HTTPException, status, Depends
from app.models.users import Users
from app.database import get_db, AsyncSession
from sqlalchemy import select

async def insertSessionToken(request: Request, token: str, db: AsyncSession = Depends(get_db)):
    #TODO: insert to database
    return 1
async def verifySession(request: Request, db: AsyncSession = Depends(get_db)):
    session_id = request.cookies.get("session_id")

    #TODO: set Users.session Token to the proper user
    if not session_id or session_id != (await db.execute(select(Users.session_token).where(Users.session_token == session_id))).scalars().first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please login"
        )
        
    return {"success"}