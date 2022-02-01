from .database import Base, engine
from sqlalchemy import Column, String, Integer


class MoneyStock(Base):
    __tablename__ = "moneystock"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Integer, unique=True, index=True, nullable=False)
    type = Column(String)
    amount = Column(Integer)


class ProductStock(Base):
    __tablename__ = "productstock"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, index=True, nullable=False)
    price = Column(Integer)
    amount = Column(Integer)


Base.metadata.create_all(bind=engine)