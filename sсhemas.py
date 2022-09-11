from pydantic import BaseModel
from coins import all_coins


class MonitoringCoin:
    usd: float
