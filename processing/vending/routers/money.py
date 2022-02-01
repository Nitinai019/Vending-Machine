from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from vending import crud
from vending.shared_function import get_db
from vending.schemas import MoneyStock


router = APIRouter(prefix="/money-stock", tags=["money"])


@router.post("/", response_model=MoneyStock)
def create_money(money: MoneyStock, db: Session = Depends(get_db)):
    a_money = crud.get_money(db, title=money.title)
    if a_money:
        raise HTTPException(status_code=400, detail="Money value already exist.")
    return crud.create_money(db=db, money=money)


@router.get("/all", response_model=List[MoneyStock], tags=["money"])
def get_all_money(db: Session = Depends(get_db)):
    all_money = crud.get_all_money(db)
    return all_money


@router.get("/{title}", response_model=MoneyStock, tags=["money"])
def get_money(title: int, db: Session = Depends(get_db)):
    a_money = crud.get_money(db, title=title)
    if a_money is None:
        raise HTTPException(status_code=404, detail="Money value not found.")
    return a_money


@router.put(
    "/",
    response_model=MoneyStock,
    description="Money type: [coins, banknotes].",
    tags=["money"],
)
def update_money(money: MoneyStock, db: Session = Depends(get_db)):
    a_money = crud.get_money(db, title=money.title)
    if a_money is None:
        raise HTTPException(status_code=404, detail="Money value not found.")

    return crud.update_money(db, money=money)
