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


