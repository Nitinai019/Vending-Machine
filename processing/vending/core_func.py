from typing import Dict, List, Tuple

from . import schemas, main


def product_price(
    product: str, all_products: List[schemas.ProductStock], n_product: int = 1
) -> int:
    """
    Check product stock available and product price then return total of produce price.
    """

    for p in all_products:
        if p.title == product:
            if p.amount >= n_product:
                return p.price * n_product

            raise main.CustomException(status_code=404, message="Product out of stock.")

    raise main.CustomException(status_code=404, message="Product not found.")


def usage_money_stock(
    money: int, money_list: List[schemas.MoneyStock]
) -> List[Tuple[int, int]]:
    """
    This function use for calculate cash usage from change and then response
    list of cash value and number of cash that are used and return list of cash usage.
    """

    stock_used = []
    balance = money

    money_list = sorted(money_list, key=lambda item: item.title, reverse=True)

    if not isinstance(money, int):
        raise main.CustomException(status_code=404, message="Money must be integer.")

    if balance <= 0:
        raise main.CustomException(
            status_code=404, message="Money value must be greater than 0."
        )

    for i in money_list:
        title = i.title
        amount = i.amount

        if balance < title or i.amount <= 0:
            continue

        amount_needed = balance // title
        stock_amount = amount
        amount_used = amount_needed

        if amount_needed > stock_amount:
            amount_used = stock_amount

        stock_used.append((title, amount_used))
        money_used = abs(amount_used) * title

        balance -= money_used

    if balance > 0:
        raise main.CustomException(
            status_code=404, message="Money stock not enough for change."
        )

    return stock_used


def calculate_change(u_money: int, p_price: int) -> int:
    """
    calculate change from user money and product price then return change

    """

    change = u_money - p_price
    if change < 0:
        raise main.CustomException(
            status_code=404,
            message=f"Money not enough to buy product: Your total money ({u_money}) must be equal or greate than price ({p_price}).",
        )

    return change


def calculate_user_money(
    cash: List[schemas.MoneyStock], all_money_details: Dict
) -> int:
    """
    calculate total of user money and return it.
    """

    result = 0
    money_title = list(all_money_details.values())
    money_type = list(schemas.MoneyType._member_map_)

    for c in cash:
        if c.title not in all_money_details:
            raise main.CustomException(
                status_code=404, message=f"The money title must be in {money_title}"
            )

        if c.type != all_money_details[c.title]:
            raise main.CustomException(
                status_code=400,
                message=f"The money type is not correct. should be {money_type}",
            )

        result += c.title * c.amount

    return result
