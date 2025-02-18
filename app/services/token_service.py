from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.price_history import PriceHistory
from app.models.token import Token


async def create_token(db: AsyncSession, name: str, symbol: str, price: float):
    token = Token(name=name, symbol=symbol, price=price)
    db.add(token)
    await db.commit()
    await db.refresh(token)
    return token


async def get_tokens(db: AsyncSession):
    result = await db.execute(select(Token))
    return result.scalars().all()


async def get_token_by_symbol(db: AsyncSession, symbol: str):
    result = await db.execute(select(Token).where(Token.symbol == symbol))
    return result.scalar_one_or_none()


async def update_token_price(db: AsyncSession, symbol: str, new_price: float):
    token = await get_token_by_symbol(db, symbol)
    if token and token.price != new_price:
        token.price = new_price
        price_history = PriceHistory(token_symbol=symbol, price=new_price)
        db.add(price_history)
        await db.commit()
        await db.refresh(token)
    return token


async def delete_token(db: AsyncSession, symbol: str):
    token = await get_token_by_symbol(db, symbol)
    if token:
        await db.delete(token)
        await db.commit()
    return token


async def get_token_price_history(db: AsyncSession, symbol: str):
    result = await db.execute(select(PriceHistory).where(PriceHistory.token_symbol == symbol))
    return result.scalars().all()
