from typing import List, Union

import pytest
from pydantic import BaseModel, ValidationError

from vending.main import CustomException

from vending.core_func import (
    calculate_user_money,
    product_price,
    usage_money_stock,
    calculate_change,
)
from vending.schemas import MoneyStock, ProductStock, MONEY_TYPE, MONEY_LIST


@pytest.fixture(scope="class")
def product_stock_init():
    products = [
        ProductStock(title="AA", price=15, amount=20),
        ProductStock(title="BB", price=12, amount=0),
        ProductStock(title="CC", price=17, amount=10),
    ]
    return products


@pytest.fixture(scope="class")
def money_title_init():
    money_title = {
        1: "coins",
        5: "coins",
        10: "coins",
        20: "banknotes",
        50: "banknotes",
        100: "banknotes",
        500: "banknotes",
        10000: "banknotes",
    }
    return money_title


@pytest.fixture(scope="class")
def money_init():
    money = [
        MoneyStock(title=1, type="coins", amount=20),
        MoneyStock(title=5, type="coins", amount=0),
        MoneyStock(title=10, type="coins", amount=10),
        MoneyStock(title=20, type="banknotes", amount=40),
        MoneyStock(title=50, type="banknotes", amount=0),
        MoneyStock(title=100, type="banknotes", amount=500),
        MoneyStock(title=500, type="banknotes", amount=30),
        MoneyStock(title=1000, type="banknotes", amount=20),
    ]
    return money


class TestCalculateUserMoney:
    def test_sample_case(self):
        user_money = [
            MoneyStock(title=5, type="coins", amount=2),
            MoneyStock(title=20, type="banknotes", amount=2),
        ]
        expect_data = 0

        for c in user_money:
            expect_data += c.title * c.amount

        actual = calculate_user_money(user_money)

        assert actual == expect_data

    def test_money_title_error(self):
        with pytest.raises(ValueError) as excinfo:
            user_money = [
                MoneyStock(title=5, type="coins", amount=2),
                MoneyStock(title=99, type="banknotes", amount=2),
            ]
            calculate_user_money(user_money)

    def test_money_type_error(self):
        with pytest.raises(ValidationError):
            user_money = [
                MoneyStock(title=5, type="card", amount=2),
            ]
            calculate_user_money(user_money)


class TestProductPrice:
    def test_sample_case(self, product_stock_init):
        product = "AA"
        n_product = 2

        actual = product_price(product, product_stock_init, n_product)
        item_data = get_item_detail(product_stock_init, product, "price")

        assert actual == item_data * n_product

    def test_out_of_stock_error(self, product_stock_init):
        product = "BB"
        n_product = 1

        with pytest.raises(CustomException) as excinfo:
            product_price(product, product_stock_init, n_product)

        assert excinfo.value.message == "Product out of stock."
        assert excinfo.value.status_code == 404

    def test_product_not_found_error(self, product_stock_init):
        product = "ZZ"
        n_product = 1

        with pytest.raises(CustomException) as excinfo:
            product_price(product, product_stock_init, n_product)

        assert excinfo.value.message == "Product not found."
        assert excinfo.value.status_code == 404


class TestMoneyStock:
    def test_sample_case(self, money_init):
        money = 250
        actual = usage_money_stock(money, money_init)

        assert actual == [(100, 2), (20, 2), (10, 1)]

    def test_money_type_error(self, money_init):
        money = 99.9
        with pytest.raises(CustomException) as excinfo:
            usage_money_stock(money, money_init)

        assert excinfo.value.message == "Money must be integer."
        assert excinfo.value.status_code == 404

    def test_money_value_error(self, money_init):
        money = -1
        with pytest.raises(CustomException) as excinfo:
            usage_money_stock(money, money_init)

        assert excinfo.value.message == "Money value must be greater than 0."
        assert excinfo.value.status_code == 404

    def test_money_stock_not_enough_error(self, money_init):
        money = 99999999999999999

        with pytest.raises(CustomException) as excinfo:
            usage_money_stock(money, money_init)

        assert excinfo.value.message == "Money stock not enough for change."
        assert excinfo.value.status_code == 404


class CalculateChange:
    def test_sample_case(self):
        money = 50
        p_price = 17

        expected = money - p_price
        actual = calculate_change(money, p_price)

        assert actual == expected

    def test_money_not_enough_error(self):
        money = -1
        p_price = 21
        with pytest.raises(CustomException) as excinfo:
            calculate_change(money, p_price)

        assert (
            excinfo.value.message
            == f"Money not enough to buy product: Your total money ({money}) must be equal or greate than price ({product_price})."
        )
        assert excinfo.value.status_code == 404


def get_item_detail(
    items: List[BaseModel], item_name: Union[int, str], value: Union[int, str]
):
    for i in items:
        item = i.dict()
        if item["title"] == item_name:
            return item[value]
