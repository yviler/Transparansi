from app.database import AsyncSession
from app.models.wallets import Wallets
from app.models.projects import Projects
from sqlalchemy import select

async def getWalletByName(db:AsyncSession, wallet_name:str)-> Wallets:
    return (await db.execute(select(Wallets).where(Wallets.wallet_name == wallet_name))).scalars().first()

async def getWalletList(db:AsyncSession) -> list:
    return (await db.execute(select(Wallets))).scalars().all()

async def getActiveWalletList(db:AsyncSession) -> list:
    return (await db.execute(select(Wallets).where(Wallets.is_active == True))).scalars().all()

async def getActiveUnusedWalletList(db:AsyncSession) -> list:
    return (await db.execute(select(Wallets).where(Wallets.is_active == True, ~Wallets.id.in_(select(Projects.wallet_id))))).scalars().all()

async def insertWalletObj(db:AsyncSession, new_wallet: Wallets) -> None:
    db.add(new_wallet)
    await db.commit()