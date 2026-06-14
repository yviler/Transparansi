from app.database import AsyncSession
from app.models.wallets import Wallets, WalletTransactions, Bills
from app.models.projects import Projects
from sqlalchemy import select
from decimal import Decimal

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

async def getWalletInfo(db:AsyncSession, wallet_id: str) -> Wallets:
    return (await db.execute(select(Wallets).where(Wallets.id == wallet_id))).scalars().first()

async def getWalletLedger(db:AsyncSession, wallet_id: str) -> any:
    expenses = (await db.execute(select(WalletTransactions).where(WalletTransactions.from_wallet_id == wallet_id))).scalars().all()
    incomes = (await db.execute(select(WalletTransactions).where(WalletTransactions.to_wallet_id == wallet_id))).scalars().all()
    return expenses, incomes

async def transferFund(db:AsyncSession, transaction: WalletTransactions):
    db.add(transaction)
    await db.commit()
    
def calculateCurrentFunds(expenses: tuple, incomes: tuple) -> tuple[Decimal, Decimal]:
    final_income = 0
    final_expense = 0
    
    for income in incomes:
        value = 0
        if income.is_cancelled:
            final_income += value
        else:
            value = Decimal(income.amount)
            final_income += value
            
    for expense in expenses:
        value = 0
        if expense.is_cancelled:
            final_expense += value
        else:
            value = Decimal(expense.amount)
            final_expense += value
            
    return Decimal(final_income), Decimal(final_expense)