from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

async_engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


from app.models.token import Token
from app.models.price_history import PriceHistory


async def get_db():
    session: AsyncSession = async_session()
    try:
        yield session
    finally:
        await session.close()
