from fastapi import Request, HTTPException, status, Depends
from app.models.users import Users
from app.database import get_db, AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

async def insertSessionToken(user: Users, token: str, db: AsyncSession) -> None:
    user.session_token = token
    user.session_token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    db.add(user)
    
    await db.commit()

# dependency for token verification
async def verifySession(request: Request, db: AsyncSession = Depends(get_db)) -> Users:
    session_id = request.cookies.get("session_id")

    #if session_id is None, it will return user where session_token is Null
    user = (await db.execute(select(Users).where(Users.session_token == session_id))).scalars().first()

    #check if session is expired, and later, check if correct user is using this session
    
    if not session_id or not user or session_id != user.session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please login"
        )
    
    return user

