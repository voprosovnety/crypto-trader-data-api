import httpx

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"


async def get_crypto_price(symbol: str) -> float:
    """Получает текущую цену криптовалюты с CoinGecko API"""
    crypto_id_map = {"BTC": "bitcoin", "ETH": "ethereum"}
    crypto_id = crypto_id_map.get(symbol.upper())

    if not crypto_id:
        return None

    async with httpx.AsyncClient() as client:
        response = await client.get(COINGECKO_API_URL, params={"ids": crypto_id, "vs_currencies": "usd"})
        data = response.json()

    return data.get(crypto_id, {}).get("usd")
