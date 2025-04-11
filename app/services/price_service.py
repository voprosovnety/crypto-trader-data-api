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


async def get_token_ids(symbols: list[str]) -> dict[str, str]:
    url = f"{COINGECKO_API_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return {}

        data = response.json()

    symbol_to_id = {token["symbol"].upper(): token["id"] for token in data}

    print(f"Token mapping: {symbol_to_id}")
    return symbol_to_id


async def get_crypto_prices(symbols: list[str]) -> dict[str, float]:
    symbol_to_id = await get_token_ids(symbols)
    token_ids = [symbol_to_id[symbol] for symbol in symbols if symbol in symbol_to_id]

    if not token_ids:
        print(f"No valid CoinGecko IDs for tokens: {symbols}")
        return {}

    url = f"{COINGECKO_API_URL}/simple/price"
    params = {
        "vs_currencies": "usd",
        "ids": ",".join(token_ids)
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        try:
            data = response.json()
            print(f"Raw API response: {data}")
        except Exception as e:
            print(f"Failed to parse JSON response: {e}")
            return {}

    prices = {symbol: data.get(symbol_to_id[symbol], {}).get("usd") for symbol in symbols if symbol in symbol_to_id}
    print(f"Parsed prices: {prices}")
    return prices


async def save_price_history(db: AsyncSession, token_symbol: str, price: float):
    timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
    price_record = PriceHistory(token_symbol=token_symbol, price=price, timestamp=timestamp)
    db.add(price_record)
    await db.commit()


async def get_token_price_history(db: AsyncSession, symbol: str):
    result = await db.execute(select(PriceHistory).where(PriceHistory.token_symbol == symbol))
    return result.scalars().all()
