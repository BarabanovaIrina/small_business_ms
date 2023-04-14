import json
from unittest.mock import MagicMock, patch

from django.test import TestCase


class TestSalesOrdersListView(TestCase):
    @patch("sales.sls.views.all_orders", return_value={"dummy": "dummy"})
    def test_all_orders_returns_200(self, all_orders_mock):
        response = self.client.get("/sales/orders")
        all_orders_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"dummy": "dummy"})


class TestOrderDetailView(TestCase):
    @patch(
        "sales.sls.views.get_order",
        return_value={"transaction_id": "transaction_1", "user_id": "user_1"},
    )
    def test_get_order_returns_200(self, get_order_mock):
        response = self.client.get("/sales/orders/1")
        get_order_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)


class TestSoldItemsView(TestCase):
    @patch("sales.sls.views.requests")
    def test(self, request_mock):
        # given
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "product_name": "name_1",
            "quantity": 1,
            "price": 10,
        }
        request_mock.get.return_value = response_mock

        # when
        response = self.client.get("/sales/sold_items")

        # then
        request_mock.get.assert_called_once()
        self.assertEqual(response.status_code, 200)
