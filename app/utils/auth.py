from fastapi import Request, HTTPException, status, Depends
from app.models.users import Users
from app.database import get_db, AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

async def insertSessionToken(user: Users, token: str, db: AsyncSession):
    user.session_token = token
    user.session_token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    db.add()
    await db.commit()

async def verifySession(request: Request, db: AsyncSession = Depends(get_db)):
    session_id = request.cookies.get("session_id")
    #TODO: set Users.session Token to the proper user, also filter if token expires
    if not session_id or session_id != (await db.execute(select(Users).where(Users.session_token == session_id))).scalars().first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please login"
        )
    return Users