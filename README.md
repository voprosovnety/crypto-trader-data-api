# Crypto Trader Data API

An asynchronous RESTful API built with FastAPI to manage and track cryptocurrency token data, including real-time price
fetching and historical price recording.

---

## 🚀 Features

- Manage custom tokens (create, read, update, delete)
- Fetch real-time prices via CoinGecko API
- Store and retrieve historical price data
- Auto-update token prices every 60 seconds
- Async-ready using `httpx` and `SQLAlchemy`

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** – API Framework
- **SQLAlchemy** – Async ORM
- **PostgreSQL** – Database
- **Alembic** – Migrations
- **httpx** – Async HTTP client

---

## 🧾 API Endpoints

Base URL: `/api`

### Tokens

- `POST /tokens` – Add a new token
- `GET /tokens/` – Get all tokens
- `GET /tokens/{symbol}` – Get token by symbol
- `PUT /tokens/{symbol}` – Update token price
- `DELETE /tokens/{symbol}` – Remove a token
- `GET /tokens/{symbol}/price` – Get current price from CoinGecko
- `GET /tokens/{symbol}/history` – Get historical price records

---

## 📦 Setup

```bash
# Clone repo
$ git clone <your-repo-url>
$ cd <your-project-dir>

# Create virtual env
$ python -m venv .venv
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Set up environment variables
$ cp .env.example .env
# Fill in DATABASE_URL and DATABASE_URL_SYNC

# Apply migrations
$ alembic upgrade head

# Run the API (option 1)
$ uvicorn main:app --reload

# Or just run the script (option 2)
$ python run.py
```

---

## 🧪 Development Notes

- Project uses async everywhere – don't mix sync DB calls
- Docstrings and inline comments are in Russian and may be updated for production
- CoinGecko rate limits apply. Retry logic is implemented in `safe_get_crypto_prices`
- Default token list is populated on app startup

---

## 📁 Project Structure

```
app/
├── api/
│   └── token_routes.py         # API routes
├── core/
│   ├── config.py               # Env settings
│   └── database.py            # DB and session setup
├── models/
│   ├── token.py               # Token model
│   └── price_history.py       # Price history model
├── schemas/
│   └── token.py               # Pydantic schemas
├── services/
│   ├── token_service.py       # Token logic
│   └── price_service.py       # Price fetching, saving
└── main.py                    # Entry point
```

---

## 🧪 Example Usage

Want to test the API locally? Here’s a simple curl command to check if it’s working:

```bash
curl http://localhost:8000/api/tokens/BTC/price
```

(Replace `BTC` with your token symbol of choice.)

---

## 🧙‍♂️ Disclaimer

This project is not responsible for your trading decisions, your token moonshots, or any financial heartbreak. CoinGecko
may also rate-limit you into oblivion. Use wisely.

