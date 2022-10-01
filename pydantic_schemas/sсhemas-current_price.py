from pydantic import BaseModel
from typing import List


class CurrentPrice(BaseModel):
    usd: float
    eur: float
    rub: float


class MarketData(BaseModel):
    current_price: CurrentPrice


class MarketDataModel(BaseModel):
    market_data: MarketData

