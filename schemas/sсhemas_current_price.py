from pydantic import BaseModel


class CurrentPrice(BaseModel):
    usd: float
    eur: float
    rub: float


class MarketData(BaseModel):
    current_price: CurrentPrice


class MarketDataModel(BaseModel):
    market_data: MarketData
