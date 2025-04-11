from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.token import Token
from app.services.price_service import save_price_history, get_top_tokens, safe_get_crypto_prices


async def initialize_tokens(db: AsyncSession):
    """Добавляет топ-50 криптовалют в БД, если их там нет."""
    print("Initializing tokens...")

    top_tokens = await get_top_tokens()
    if not top_tokens:
        print("Failed to fetch top tokens from API.")
        return

    existing_tokens = await db.execute(select(Token.symbol))
    existing_symbols = {row[0] for row in existing_tokens.fetchall()}

    new_symbols = [token["symbol"].upper() for token in top_tokens if token["symbol"].upper() not in existing_symbols]

    if not new_symbols:
        print("No new tokens to add.")
        return

    prices = await safe_get_crypto_prices(new_symbols)

    missing_prices = [symbol for symbol in new_symbols if symbol not in prices or prices[symbol] is None]
    if missing_prices:
        print(f"Missing prices for tokens: {missing_prices}")

    new_tokens = [
        Token(name=token["name"], symbol=token["symbol"].upper(), price=prices.get(token["symbol"].upper(), 0))
        for token in top_tokens
        if token["symbol"].upper() in prices and prices[token["symbol"].upper()] is not None
    ]

    if new_tokens:
        db.add_all(new_tokens)
        await db.commit()
        print(f"Added {len(new_tokens)} new tokens to the database.")
    else:
        print("No valid tokens to add (all had missing prices).")


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
        await save_price_history(db, token.symbol, token.price)
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
