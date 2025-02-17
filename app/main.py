import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.token_routes import router as token_router
from app.core.config import settings
from app.core.database import get_db
from app.services.price_service import get_crypto_price
from app.services.token_service import get_tokens, update_token_price


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(update_prices_loop())
    await asyncio.sleep(0.1)
    yield
    task.cancel()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(token_router, prefix="/api")


async def update_prices_loop():
    """Фоновая задача для обновления цен каждые 60 секунд."""
    while True:
        async for db in get_db():
            tokens = await get_tokens(db)
            if not tokens:
                print("No tokens found in the database!")
            for token in tokens:
                new_price = await get_crypto_price(token.symbol)
                if new_price:
                    await update_token_price(db, token.symbol, new_price)
                    print(f"Updated {token.symbol}: {new_price}")
                else:
                    print(f"Failed to get price for {token.symbol}")
        await asyncio.sleep(60)


@app.get("/")
def root():
    return {"message": "Crypto Trader Data API is running!"}
