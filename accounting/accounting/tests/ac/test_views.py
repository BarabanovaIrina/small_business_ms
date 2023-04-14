import json
from unittest.mock import patch

from django.test import TestCase


class TestTransactionsView(TestCase):
    @patch("accounting.ac.views.all_transactions", return_value={"dummy": "dummy"})
    def test_all_orders_returns_200(self, all_transactions_mock):
        response = self.client.get("/accounting/transactions")
        all_transactions_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"dummy": "dummy"})


class TestTransactionDetailView(TestCase):
    @patch(
        "accounting.ac.views.get_transaction",
        return_value={
            "user_id": "user_1",
            "transaction_id": 1,
            "timestamp": "2023-04-13 14:53:47.479374",
            "total": 10,
        },
    )
    def test_get_order_returns_200(self, get_transaction_mock):
        response = self.client.get("/accounting/transactions/1")
        get_transaction_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
