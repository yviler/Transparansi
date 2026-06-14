from fastapi import APIRouter, Request, Depends, Form
import config
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError
import app.utils.auth as auth
from typing import Annotated
from app.models.users import Users
from app.models.wallets import Wallets, WalletTransactions
from datetime import datetime, timezone
import app.utils.wallets as wallet
from app.database import get_db, AsyncSession
import app.utils.flash as flash
from decimal import Decimal

router = APIRouter()

@router.get("/wallets")
async def walletDashboard(request: Request,
                          db: AsyncSession = Depends(get_db)
                        ):
    walletList = await wallet.getWalletList(db)
    
    return config.templates.TemplateResponse(
        context={
            "wallets": walletList
        },
        request=request,
        name="wallet_dashboard.html"
    )

@router.get("/wallet/{wallet_id:str}")
async def walletInfoPage(request: Request, 
                      wallet_id:str,
                      db: AsyncSession = Depends(get_db)
                    ):
    
    walletInfo = await wallet.getWalletInfo(db, wallet_id)

    expenses, incomes = await wallet.getWalletLedger(db, wallet_id)
    
    total_income, total_expense = wallet.calculateCurrentFunds(expenses, incomes)
    
    return config.templates.TemplateResponse(
        context = {
            "wallet" :  walletInfo,
            "expenses": expenses,
            "incomes": incomes,
            "ledger": expenses + incomes, # sort by created_at later
            "total_income": total_income,
            "total_expense": total_expense,
        },
        request = request,
        name="wallet_info.html",
    )

@router.get("/create_wallet")
def createWalletPage(request: Request, 
                      account: Annotated[Users, Depends(auth.verifySession)],
                      currentUser: Annotated[Users, Depends(auth.currentUser)],
                      requiredRoles: Annotated[Users, Depends(auth.roleRequired('admin'))]
                      ):
    return config.templates.TemplateResponse(
        context={
            "wallet": None,
        },
        request=request,
        name="create_wallet.html"
    )

@router.post("/create_wallet")
async def createWallet(request: Request,
                       account: Annotated[Users, Depends(auth.verifySession)],
                       currentUser: Annotated[Users, Depends(auth.currentUser)],
                       requiredRoles: Annotated[Users, Depends(auth.roleRequired('admin'))],
                       wallet_name: str = Form(...),
                       description: str = Form(""),
                       wallet_type: str = Form(...),
                       db:AsyncSession = Depends(get_db)
                       ):
    
    if await wallet.getWalletByName(db, wallet_name):
        flash.flash(request, "Wallet name already exists", "error")
        return config.templates.TemplateResponse(
            context={
                "wallet":{
                    "description":description,
                }
            },
            request=request,
            name="create_wallet.html"
        )

    new_wallet = Wallets(
        wallet_name=wallet_name,
        description=description,
        wallet_type=wallet_type,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        created_by=currentUser.id,
    )

    try:
        await wallet.insertWalletObj(db, new_wallet)
        flash.flash(request, f"Successfully created wallet: {wallet_name}", "success")
        return RedirectResponse(url='/dashboard', status_code=303)
    except SQLAlchemyError as e:
        flash.flash(request, f"Error creating wallet: {e}", "error")
        return config.templates.TemplateResponse(
            context={
                "wallet": {
                    "wallet_name": wallet_name,
                    "description": description
                }
            },
            request=request,
            name="create_wallet.html"
        )
      
@router.get("/test/{wallet_id}")
async def test(wallet_id:str, db:AsyncSession = Depends(get_db)):
    expenses, incomes = await wallet.getWalletLedger(db, wallet_id)
    print(wallet.calculateCurrentFunds(expenses, incomes))
    
#TODO: still boilerplate, dont use
@router.post("/transfer/{from_wallet_id:str}/{to_wallet_id:str}")
async def transferFunds(from_wallet_id:str, 
                        to_wallet_id:str, 
                        #amount: str = Form(...),
                        db:AsyncSession = Depends(get_db)):
    
    new_transaction = WalletTransactions(
        tx_name = "test deposit",
        amount = Decimal(1000000),
        tx_type = "allocation",
        from_wallet_id = from_wallet_id,
        to_wallet_id = to_wallet_id,
    )
    
    try:
        await wallet.transferFund(db, new_transaction)
        print("success")
    except SQLAlchemyError as e:
        print("error", e)