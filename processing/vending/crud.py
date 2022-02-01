from sqlalchemy.orm import Session
from . import schemas, models


def get_money(db: Session, title: int):
    return db.query(models.MoneyStock).filter(models.MoneyStock.title == title).first()


def get_all_money(db: Session):
    return db.query(models.MoneyStock).all()


def create_money(db: Session, money: schemas.MoneyStock):
    a_money = models.MoneyStock(**money.dict())
    db.add(a_money)
    db.commit()
    db.refresh(a_money)
    return a_money


def update_money(db: Session, money: schemas.MoneyStock):
    a_money = (
        db.query(models.MoneyStock)
        .filter(models.MoneyStock.title == money.title)
        .first()
    )
    a_money.amount = money.amount
    a_money.type = money.type

    db.commit()
    db.refresh(a_money)
    return a_money


def update_money_amount(db: Session, title: int, amount: int):
    a_money = (
        db.query(models.MoneyStock).filter(models.MoneyStock.title == title).first()
    )
    a_money.amount = amount
    db.commit()
    db.refresh(a_money)
    return a_money


def get_product(db: Session, title: str):
    return (
        db.query(models.ProductStock).filter(models.ProductStock.title == title).first()
    )


def get_products(db: Session):
    return db.query(models.ProductStock).all()


def create_product(db: Session, product: schemas.ProductStock):
    a_product = models.ProductStock(**product.dict())
    db.add(a_product)
    db.commit()
    db.refresh(a_product)
    return a_product


def update_product(db: Session, product: schemas.ProductStock):
    a_product = (
        db.query(models.ProductStock)
        .filter(models.ProductStock.title == product.title)
        .first()
    )
    a_product.amount = product.amount
    a_product.price = product.price

    db.commit()
    db.refresh(a_product)
    return a_product
