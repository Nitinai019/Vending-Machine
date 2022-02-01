import pytest

from vending.schemas import MoneyStock, ProductStock
from .shared_func import client, test_db


@pytest.fixture(scope="class")
def money_init():
    money = [
        MoneyStock(title=1, type="coins", amount=20),
        MoneyStock(title=5, type="coins", amount=0),
        MoneyStock(title=10, type="coins", amount=10),
        MoneyStock(title=20, type="banknotes", amount=40),
        MoneyStock(title=100, type="banknotes", amount=500),
    ]
    for m in money:
        client.post(
            "/money-stock/",
            json={"title": m.title, "type": m.banknotes, "amount": m.amount},
        )

    return money


class TestVendingMachine:
    def test_sample_case(self, test_db):
        money = [
            MoneyStock(title=1, type="coins", amount=20),
            MoneyStock(title=5, type="coins", amount=0),
            MoneyStock(title=10, type="coins", amount=10),
            MoneyStock(title=20, type="banknotes", amount=40),
            MoneyStock(title=100, type="banknotes", amount=500),
        ]
        for m in money:
            client.post(
                "/money-stock/",
                json={"title": m.title, "type": m.type, "amount": m.amount},
            )

        products = [
            ProductStock(title="AA", price=15, amount=20),
        ]
        for p in products:
            client.post(
                "/product-stock/",
                json={"title": p.title, "price": p.price, "amount": p.amount},
            )

        response = client.post(
            "/vending-machine/",
            json={
                "money": [{"title": 100, "amount": 1, "type": "banknotes"}],
                "products": {"title": "AA", "amount": 1},
            },
        )

        assert response.status_code == 200, response.text
