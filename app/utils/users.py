from pwdlib import PasswordHash
from app.database import get_db, AsyncSession
from fastapi import Depends
from app.models.users import Users

password_hash = PasswordHash.recommended()

async def getPasswordHash(password:str) -> str:
    return password_hash.hash(password)

async def verifyPasswordWithHash(password:str, hashed:str) -> bool:
    return password_hash.verify(password, hashed)

async def duplicateUsernames(username: str, db: AsyncSession) -> bool:
    #db.query is synchronous, change to select() later
    return db.query(Users).filter(Users.username == username).first()