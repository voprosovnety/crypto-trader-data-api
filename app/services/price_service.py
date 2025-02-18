import asyncio
from datetime import datetime, timezone

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.price_history import PriceHistory

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
SUPPORTED_CURRENCIES = ["usd"]
MAX_TOKENS = 30


async def get_top_tokens():
    url = f"{COINGECKO_API_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": MAX_TOKENS,
        "page": 1
    }

    async with httpx.AsyncClient() as client:
        await asyncio.sleep(2)
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Fetched {len(data)} tokens from API.")
            return data
        print(f"API Error: {response.status_code} - {response.text}")
        return None


async def get_crypto_prices(symbols: list[str]) -> dict[str, float]:
    url = f"{COINGECKO_API_URL}/simple/price"
    ids = ",".join(symbol.lower() for symbol in symbols)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"ids": ids, "vs_currencies": "usd"})
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return {}

        data = response.json()
    prices = {symbol.upper(): data.get(symbol.lower(), {}).get("usd") for symbol in symbols}
    return {symbol: price for symbol, price in prices.items() if price is not None}


async def save_price_history(db: AsyncSession, token_symbol: str, price: float):
    price_record = PriceHistory(token_symbol=token_symbol, price=price, timestamp=datetime.now(timezone.utc))
    db.add(price_record)
    await db.commit()


async def get_token_price_history(db: AsyncSession, symbol: str):
    result = await db.execute(select(PriceHistory).where(PriceHistory.token_symbol == symbol))
    return result.scalars().all()
