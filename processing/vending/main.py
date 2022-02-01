from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud, schemas
from .shared_function import get_db
from .routers import product, money
from .core_func import (
    calculate_change,
    calculate_user_money,
    product_price,
    usage_money_stock,
)

app = FastAPI()

app.include_router(product.router)
app.include_router(money.router)


@app.post(
    "/vending-machine/",
    description="Money type: [coins, banknotes].",
    tags=["vending-machine"],
)
def buy_product(payload: schemas.UserUsage, db: Session = Depends(get_db)) -> int:
    all_products = product_list(db)
    all_money = money_list(db)

    all_money_title = {i.title: i.type for i in all_money}

    u_cash = calculate_user_money(payload.money, all_money_title)

    p_price = product_price(
        payload.products.title, all_products, payload.products.amount
    )
    change = calculate_change(u_cash, p_price)
    total_cash_stock_used = usage_money_stock(u_cash, all_money)

    for i in total_cash_stock_used:
        title, amount = i
        a_money = crud.get_money(db, title=title)
        money_stock_update = a_money.amount - amount

        crud.update_money_amount(db, title=title, amount=money_stock_update)

    return f"Total change: {change}"


def product_list(db: Session = Depends(get_db)):
    return crud.get_products(db)


def money_list(db: Session = Depends(get_db)):
    return crud.get_all_money(db)


class CustomException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


@app.exception_handler(CustomException)
async def value_error_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.message)},
    )
