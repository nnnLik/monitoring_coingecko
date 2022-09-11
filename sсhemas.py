from pydantic import BaseModel
from coins import all_coins


class MonitoringCoin(BaseModel):
    name: str
    categories: list
    links: dict