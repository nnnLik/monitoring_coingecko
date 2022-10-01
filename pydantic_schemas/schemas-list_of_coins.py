from pydantic import BaseModel
from typing import List


class ListOfCoins(BaseModel):
    id: str
    symbol: str
    name: str


class ListOfCoinsModel(BaseModel):
    __root__: List[ListOfCoins]
