from enum import Enum
from typing import List

from pydantic import BaseModel


class MoneyType(str, Enum):
    coins = "coins"
    banknotes = "banknotes"


class MoneyBase(BaseModel):
    title: int
    amount: int
    type: MoneyType


class MoneyStock(MoneyBase):
    pass

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    title: str
    amount: int


class ProductStock(ProductBase):
    price: int

    class Config:
        orm_mode = True


class UserUsage(BaseModel):
    money: List[MoneyBase]
    products: ProductBase
