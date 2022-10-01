from typing import List

from pydantic import BaseModel


class ListOfCoins(BaseModel):
    id: str
    symbol: str
    name: str


class ListOfCoinsModel(BaseModel):
    __root__: List[ListOfCoins]
