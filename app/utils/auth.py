from fastapi import Request, HTTPException, status, Depends
from app.models.users import Users
from app.database import get_db, AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

from app.utils import flash

async def insertSessionToken(user: Users,
                             token: str, 
                             db: AsyncSession) -> None:
    user.session_token = token
    user.session_token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    db.add(user)
    
    await db.commit()

# dependency for token verification
async def verifySession(request: Request, 
                        db: AsyncSession = Depends(get_db)) -> Users:
    session_id = request.cookies.get("session_id")

    user = (await db.execute(select(Users).where(Users.session_token == session_id))).scalars().first()

    
    #create HTTPException handler for template response
    if not session_id or not user or user.session_token_expires_at < datetime.now(timezone.utc):
        # delete session_token and session_token_expires_at and logout
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please login"
        )
    
    return user

# dependancy to get user
async def currentUser(request: Request,
                  db: AsyncSession = Depends(get_db)) -> Users:
    session_id = request.cookies.get("session_id") or None
    
    if not session_id:
        return None

    user = (await db.execute(select(Users).where(Users.session_token == session_id))).scalars().first()

    if user is None:
        return None
    
    elif user.session_token_expires_at < datetime.now(timezone.utc):
        user.session_token = None
        user.session_token_expires_at = None
        db.add(user)
        await db.commit()
        flash.flash(request, "session token has expired, please log in", "error")
        return None

    return user
        
# dependency for role checking
def roleRequired(*role_required):
    async def roleCheck(user:Users = Depends(verifySession)) -> Users:
        if not user or user.clearance_level not in role_required:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Clearance level: {role_required} is needed for this action"
            )  
        return user
    return roleCheck

