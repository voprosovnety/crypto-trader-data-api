from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
    if token:
        token.price = new_price
        await db.commit()
        await db.refresh(token)
    return token


async def delete_token(db: AsyncSession, symbol: str):
    token = await get_token_by_symbol(db, symbol)
    if token:
        await db.delete(token)
        await db.commit()
    return token


