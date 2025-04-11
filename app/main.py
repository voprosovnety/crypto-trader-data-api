import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.token_routes import router as token_router
from app.core.config import settings
from app.core.database import get_db, async_session
from app.services.price_service import safe_get_crypto_prices
from app.services.token_service import get_tokens, update_token_price, initialize_tokens


@asynccontextmanager
async def lifespan(_: FastAPI):
    async for db in get_db():
        try:
            await initialize_tokens(db)
        except Exception as e:
            print(f"Token initialization failed: {e}")
        tokens = await get_tokens(db)
        print(f"Found {len(tokens)} tokens in the database after initialization.")
        break

    task = asyncio.create_task(update_prices_loop())
    await asyncio.sleep(0.1)
    yield
    task.cancel()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(token_router, prefix="/api")


async def update_prices_loop():
    while True:
        print("Running update_prices_loop")

        db = None
        try:
            async for session in get_db():
                db = session
                break

            tokens = await get_tokens(db)
            if not tokens:
                print("No tokens found in the database!")
                await asyncio.sleep(60)
                continue

            symbols = [token.symbol for token in tokens]
            prices = await safe_get_crypto_prices(symbols)
            print(f"Prices fetched: {prices}")

            for token in tokens:
                new_price = prices.get(token.symbol)
                if new_price:
                    await update_token_price(db, token.symbol, new_price)
                    print(f"Updated {token.symbol}: {new_price}")
                else:
                    print(f"Failed to get price for {token.symbol}")
        except Exception as e:
            print(f"Error in update_prices_loop: {e}")

        await asyncio.sleep(60)


@app.get("/")
def root():
    return {"message": "Crypto Trader Data API is running!"}
