import json
from unittest.mock import patch

from django.test import TestCase

from warehouse.wh.data_models import ProductData


class TestWarehouseItemsListView(TestCase):
    @patch(
        "warehouse.wh.views.all_products",
        return_value=[
            ProductData(
                id=1,
                name="A",
                description="B",
                country_of_origin="C",
                price=1.0,
                quantity=0,
            )
        ],
    )
    def test_get_warehouse_items_returns_200(self, all_products_mock):
        response = self.client.get("/warehouse/items")
        all_products_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "id": 1,
                    "name": "A",
                    "description": "B",
                    "country_of_origin": "C",
                    "price": 1.0,
                    "quantity": 0,
                }
            ],
        )

    @patch("warehouse.wh.views.create_product", return_value=1)
    def test_create_warehouse_item_returns_200(self, create_product_mock):
        response = self.client.post(
            "/warehouse/items",
            data={"product_name": "new_name", "quantity": 1, "price": 100.00},
            content_type="application/json",
        )
        create_product_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Product with id=1 created")


class TestWarehouseItemDetailView(TestCase):
    @patch(
        "warehouse.wh.views.get_product_by_id",
        return_value=ProductData(
            id=1,
            name="name_1",
            description="desc",
            country_of_origin="c",
            price=10,
            quantity=1,
        ),
    )
    def test_get_warehouse_item_by_id_returns_200(self, get_product_by_id_mock):
        response = self.client.get("/warehouse/items/1")
        get_product_by_id_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "name": "name_1",
                "description": "desc",
                "country_of_origin": "c",
                "price": 10,
                "quantity": 1,
            },
        )

    @patch(
        "warehouse.wh.views.get_product_by_id",
        return_value=None,
    )
    def test_get_warehouse_item_by_id_returns_404(self, get_product_by_id_mock):
        response = self.client.get("/warehouse/items/100")
        get_product_by_id_mock.assert_called_once()
        self.assertEqual(response.status_code, 404)

    @patch("warehouse.wh.views.update_product")
    def test_update_warehouse_item_by_id_returns_200(self, update_product_mock):
        response = self.client.put("/warehouse/items/1", data=b'{"name": "new_name"}')
        update_product_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Item 1 updated")

    @patch("warehouse.wh.views.delete_product")
    def test_delete_warehouse_item_by_id_returns_200(self, delete_product_mock):
        response = self.client.delete("/warehouse/items/2")
        delete_product_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Item 2 deleted")
