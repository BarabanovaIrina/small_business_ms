import json
from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from sales.sls.data_models import OrderData, OrderedItemData


class TestSalesOrdersListView(TestCase):
    @patch(
        "sales.sls.views.all_orders",
        return_value=[
            OrderData(
                id=1,
                customer_id=1,
                date=datetime(2023, 5, 2),
                items=[OrderedItemData(id=1, price=10.0, quantity=5)],
            )
        ],
    )
    def test_all_orders_returns_200(self, all_orders_mock):
        response = self.client.get("/sales/orders")
        all_orders_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "id": 1,
                    "customer_id": 1,
                    "date": "02/05/2023, 00:00:00",
                    "items": [{"id": 1, "price": 10.0, "quantity": 5}],
                }
            ],
        )

    @patch("sales.sls.views.create_order", return_value=1)
    def test_create_order(self, create_order_mock):
        response = self.client.post(
            "/sales/orders",
            data={
                "customer_id": 1,
                "items": [{"id": 1, "price": 10.0, "quantity": 10}],
            },
            content_type="application/json",
        )
        create_order_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Order with id=1 created")


class TestOrderDetailView(TestCase):
    @patch(
        "sales.sls.views.get_order_by_id",
        return_value=OrderData(
            id=1,
            customer_id=1,
            date=datetime(2023, 5, 2),
            items=[OrderedItemData(id=1, price=10.0, quantity=5)],
        ),
    )
    def test_get_order_returns_200(self, get_order_mock):
        response = self.client.get("/sales/orders/1")
        get_order_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)

    @patch("sales.sls.views.get_order_by_id", return_value=None)
    def test_get_transaction_returns_404(self, get_transaction_mock):
        response = self.client.get("/sales/orders/1")
        get_transaction_mock.assert_called_once()
        self.assertEqual(response.status_code, 404)

    @patch("sales.sls.views.update_order")
    def test_update_order(self, update_order_mock):
        response = self.client.put("/sales/orders/1", data=b'{"customer_id": "327"}')
        update_order_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Order 1 updated")

    @patch("sales.sls.views.delete_order")
    def test_delete_order(self, delete_mock):
        response = self.client.delete("/sales/orders/1")
        delete_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Order 1 deleted")


# class TestSoldItemsView(TestCase):
#     @patch("sales.sls.views.requests")
#     def test(self, request_mock):
#         # given
#         response_mock = MagicMock()
#         response_mock.status_code = 200
#         response_mock.json.return_value = {
#             "product_name": "name_1",
#             "quantity": 1,
#             "price": 10,
#         }
#         request_mock.get.return_value = response_mock
#
#         # when
#         response = self.client.get("/sales/sold_items")
#
#         # then
#         request_mock.get.assert_called_once()
#         self.assertEqual(response.status_code, 200)
