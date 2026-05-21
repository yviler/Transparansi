from pwdlib import PasswordHash
from app.database import get_db, AsyncSession
from fastapi import Depends
from app.models.users import Users
from sqlalchemy import select

password_hash = PasswordHash.recommended()

def getPasswordHash(password:str) -> str:
    return password_hash.hash(password)

async def findUserHash(username:str, db: AsyncSession) -> str:
    return (await db.execute(select(Users.password_hash).where(Users.username == username))).scalars().first()

def verifyPasswordWithHash(password:str, hashed:str) -> bool:
    return password_hash.verify(password, hashed)

async def doesUsernameExist(username: str, db: AsyncSession) -> bool:
    return (await db.execute(select(1).where(Users.username == username))).scalars().first()

async def doesUserExist(username: str, db:AsyncSession) -> Users:
    return (await db.execute(select(Users).where(Users.username == username))).scalars().first()

async def createNewUser(user: Users, db:AsyncSession) -> None:
    db.add(user)
    await db.commit()