from pwdlib import PasswordHash
from app.database import get_db, AsyncSession
from fastapi import Depends
from app.models.users import Users
from sqlalchemy import select

password_hash = PasswordHash.recommended()

async def getPasswordHash(password:str) -> str:
    return password_hash.hash(password)

async def findUserHash(username:str, db: AsyncSession) -> str:
    return 

async def verifyPasswordWithHash(password:str, hashed:str) -> bool:
    return password_hash.verify(password, hashed)

async def duplicateUsernames(username: str, db: AsyncSession) -> bool:
    return (await db.execute(select(Users).where(Users.username == username))).scalars().first()