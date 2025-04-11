from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.services.token_service import (
    create_token,
    get_tokens,
    get_token_by_symbol,
    update_token_price,
    delete_token
)
from app.services.price_service import get_token_price_history, safe_get_crypto_prices
from app.schemas.token import TokenCreate, TokenResponse, PriceHistoryResponse

router = APIRouter()


async def get_existing_token(symbol: str, db: AsyncSession):
    token = await get_token_by_symbol(db, symbol)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return token


@router.post("/tokens", response_model=TokenResponse)
async def create_new_token(token_data: TokenCreate, db: AsyncSession = Depends(get_db)):
    if await get_token_by_symbol(db, token_data.symbol):
        raise HTTPException(status_code=400, detail="Token with this symbol already exists")
    return await create_token(db, token_data.name, token_data.symbol, token_data.price)


@router.get("/tokens/", response_model=List[TokenResponse])
async def read_tokens(db: AsyncSession = Depends(get_db)):
    return await get_tokens(db)


@router.get("/tokens/{symbol}", response_model=TokenResponse)
async def read_token(symbol: str, db: AsyncSession = Depends(get_db)):
    return await get_existing_token(symbol, db)


@router.put("/tokens/{symbol}", response_model=TokenResponse)
async def update_token(symbol: str, new_price: float, db: AsyncSession = Depends(get_db)):
    return await update_token_price(db, symbol, new_price)


@router.delete("/tokens/{symbol}", response_model=TokenResponse)
async def delete_token_endpoint(symbol: str, db: AsyncSession = Depends(get_db)):
    token = await get_existing_token(symbol, db)
    return await delete_token(db, token.symbol)


@router.get("/tokens/{symbol}/price")
async def get_price(symbol: str):
    prices = await safe_get_crypto_prices([symbol])
    price = prices.get(symbol.upper())

    if price is None:
        raise HTTPException(status_code=404, detail="Price not found")

    return {"symbol": symbol, "price": price}


@router.get("/tokens/{symbol}/history", response_model=List[PriceHistoryResponse])
async def get_token_history(symbol: str, db: AsyncSession = Depends(get_db)):
    history = await get_token_price_history(db, symbol)
    if not history:
        raise HTTPException(status_code=404, detail="No price history found")
    return history
