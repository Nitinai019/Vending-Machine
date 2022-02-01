from .shared_func import client, test_db


class TestProductStock:
    def test_create_product_stock(self, test_db):
        response = client.post(
            "/product-stock/",
            json={"title": "AA", "price": 15, "amount": 20},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "AA"
        assert "title" in data
        title = data["title"]

        response = client.get(f"/product-stock/{title}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == title
        assert data["price"] == 15
        assert data["amount"] == 20

    def test_post_eror_product_already_exist(self, test_db):
        response = client.post(
            "/product-stock/",
            json={"title": "AA", "price": 15, "amount": 20},
        )
        assert response.status_code == 200, response.text

        response = client.post(
            "/product-stock/",
            json={"title": "AA", "price": 15, "amount": 20},
        )
        assert response.status_code == 400

    def test_get_error_product_not_found(self, test_db):
        title = "@!@$!%@"
        response = client.get(f"/product-stock/{title}")
        assert response.status_code == 404

    def test_get_all_product_stock(self, test_db):
        response1 = client.post(
            "/product-stock/",
            json={"title": "BB", "price": 12, "amount": 10},
        )

        assert response1.status_code == 200, response1.text
        data = response1.json()
        assert data["title"] == "BB"

        response2 = client.post(
            "/product-stock/",
            json={"title": "XX", "price": 10, "amount": 20},
        )

        assert response2.status_code == 200, response2.text
        data = response2.json()
        assert data["title"] == "XX"

        response = client.get(f"/product-stock/all")
        assert response.status_code == 200, response.text
        data = response.json()

        assert len(data) == 2

    def test_update_product_stock(self, test_db):
        response = client.post(
            "/product-stock/",
            json={"title": "CC", "price": 12, "amount": 20},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "CC"
        assert data["amount"] == 20
        assert data["price"] == 12
        assert "title" in data
        title = data["title"]

        response_update = client.put(
            f"/product-stock/",
            json={"title": title, "price": 17, "amount": 30},
        )

        assert response_update.status_code == 200, response_update.text
        data_updated = response_update.json()

        assert data_updated["title"] == "CC"
        assert data_updated["amount"] == 30
        assert data_updated["price"] == 17

    def test_update_error_product_not_found(self, test_db):
        title = "NOT_FOUND"
        response_update = client.put(
            f"/product-stock/",
            json={"title": title, "price": 17, "amount": 30},
        )

        assert response_update.status_code == 404
