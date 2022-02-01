import pytest

from .shared_func import client, test_db


class TestMoneyStock:
    def test_create_money_stock(self, test_db):
        response = client.post(
            "/money-stock/",
            json={"title": 500, "type": "banknotes", "amount": 20},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == 500
        assert "title" in data
        title = data["title"]

        response = client.get(f"/money-stock/{title}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == title
        assert data["type"] == "banknotes"
        assert data["amount"] == 20

    def test_post_error_money_title_not_correct(self, test_db):
        response = client.post(
            "/money-stock/",
            json={"title": 99999, "type": "banknotes", "amount": 20},
        )

        assert response.status_code == 422

    def test_post_error_money_already_exist(self, test_db):
        response = client.post(
            "/money-stock/",
            json={"title": 100, "type": "banknotes", "amount": 10},
        )
        assert response.status_code == 200, response.text

        response = client.post(
            "/money-stock/",
            json={"title": 100, "type": "banknotes", "amount": 10},
        )
        assert response.status_code == 400

    def test_get_error_money_not_found(self, test_db):
        title = 100
        response = client.get(f"/money-stock/{title}")
        assert response.status_code == 404

    def test_get_all_money_stock(self, test_db):
        response1 = client.post(
            "/money-stock/",
            json={"title": 500, "type": "banknotes", "amount": 10},
        )

        assert response1.status_code == 200, response1.text
        data = response1.json()
        assert data["title"] == 500

        response2 = client.post(
            "/money-stock/",
            json={"title": 1, "type": "coins", "amount": 100},
        )

        assert response2.status_code == 200, response2.text
        data = response2.json()
        assert data["title"] == 1

        response = client.get(f"/money-stock/all")
        assert response.status_code == 200, response.text
        data = response.json()

        assert len(data) == 2

    def test_update_money_stock(self, test_db):
        response = client.post(
            "/money-stock/",
            json={"title": 100, "type": "banknotes", "amount": 20},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == 100
        assert data["amount"] == 20
        assert "title" in data
        title = data["title"]

        response_update = client.put(
            f"/money-stock/",
            json={"title": title, "amount": 10, "type": "banknotes"},
        )

        assert response_update.status_code == 200, response_update.text
        data_updated = response_update.json()

        assert data_updated["title"] == 100
        assert data_updated["amount"] == 10

    def test_update_error_money_not_found(self, test_db):
        title = 1000

        response_update = client.put(
            f"/money-stock/",
            json={"title": title, "type": "banknotes", "amount": 30},
        )

        assert response_update.status_code == 404
