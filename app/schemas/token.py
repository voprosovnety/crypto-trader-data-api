from datetime import datetime

from pydantic import BaseModel


class TokenBase(BaseModel):
    name: str
    symbol: str
    price: float


class TokenCreate(TokenBase):
    pass


class TokenResponse(TokenBase):
    id: int

    class Config:
        from_attributes = True


class PriceHistoryResponse(BaseModel):
    token_symbol: str
    price: float
    timestamp: datetime

    class Config:
        from_attributes = True
