from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from vending import crud
from vending.shared_function import get_db
from vending.schemas import ProductStock

router = APIRouter(
    prefix="/product-stock",
    tags=["product"],
)

@router.post("/", response_model=ProductStock)
def create_product(product: ProductStock, db: Session = Depends(get_db)):
    a_product = crud.get_product(db, title=product.title)
    if a_product:
        raise HTTPException(status_code=400, detail="Product already exist.")
    return crud.create_product(db=db, product=product)


@router.get("/all", response_model=List[ProductStock])
def get_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products


@router.get("/{title}", response_model=ProductStock)
def get_product(title: str, db: Session = Depends(get_db)):
    a_product = crud.get_product(db, title=title)
    if a_product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return a_product


@router.put("/", response_model=ProductStock)
def update_produut(
    product: ProductStock,
    db: Session = Depends(get_db),
):
    a_product = crud.get_product(db, title=product.title)
    if a_product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    return crud.update_product(db, product=product)
