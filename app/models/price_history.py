from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    token_symbol = Column(String, ForeignKey("tokens.symbol"), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

    token = relationship("Token", back_populates="history")
