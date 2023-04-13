import json
from unittest.mock import patch

from django.test import TestCase


class TestWarehouseItemsListView(TestCase):
    @patch("warehouse.wh.views.all_products", return_value={"dummy": "dummy"})
    def test_get_warehouse_items_returns_200(self, all_products_mock):
        response = self.client.get("/warehouse/items")
        all_products_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"dummy": "dummy"})

    @patch("warehouse.wh.views.create_product")
    def test_create_warehouse_item_returns_200(self, create_product_mock):
        response = self.client.post(
            "/warehouse/items",
            data={"product_name": "new_name", "quantity": 1, "price": 100.00},
        )
        create_product_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Product created")


class TestWarehouseItemDetailView(TestCase):
    @patch(
        "warehouse.wh.views.get_product_by_id",
        return_value={"product_name": "name_1", "quantity": 1, "price": 10},
    )
    def test_get_warehouse_item_by_id_returns_200(self, create_product_mock):
        response = self.client.get("/warehouse/items/1")
        create_product_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"product_name": "name_1", "quantity": 1, "price": 10},
        )

    @patch("warehouse.wh.views.update_product")
    def test_edit_warehouse_item_by_id_returns_200(self, update_product_mock):
        response = self.client.post("/warehouse/items/1", data={"name": "new_name"})
        update_product_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Item 1 updated")


class TestWarehouseItemDeleteView(TestCase):
    @patch("warehouse.wh.views.delete_product")
    def test_delete_warehouse_item_by_id_returns_200(self, delete_product_mock):
        response = self.client.post("/warehouse/delete/2")
        delete_product_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Item 2 deleted")
