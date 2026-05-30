from app.database import AsyncSession
from app.models.wallets import Wallets

async def getWalletId(db:AsyncSession, wallet_name:str)-> Wallets:
    return (await db.execute(select(Wallets).where(Wallets.wallet_name == wallet_name))).scalars().first()

async def getWalletList(db:AsyncSession) -> list:
    return (await db.execute(select(Wallets))).scalars().all()

async def insertWalletObj(db:AsyncSession, new_wallet: Wallets) -> None:
    db.add(new_wallet)
    await db.commit()