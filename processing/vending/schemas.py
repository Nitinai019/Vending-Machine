from enum import Enum
from typing import List

from pydantic import BaseModel, validator


# class MoneyType(str, Enum):
#     coins = "coins"
#     banknotes = "banknotes"



MONEY_TYPE = ["coins", "banknotes"]

MONEY_LIST = {
    1: "coins",
    5: "coins",
    10: "coins",
    20: "banknotes",
    50: "banknotes",
    100: "banknotes",
    500: "banknotes",
    1000: "banknotes",
}
class MoneyBase(BaseModel):
    title: int
    amount: int
    type: str

    @validator("title")
    def validate_title_format(cls, v):
        if v not in MONEY_LIST.keys():
            raise ValueError(f'Money title must be in {MONEY_LIST.keys()}')
        return v

    @validator("type")
    def validate_type_format(cls, v):
        if v not in MONEY_TYPE:
            raise ValueError(f'Money type must be in {MONEY_TYPE}')
        return v


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
