import datetime
import json
from unittest.mock import patch

from django.test import TestCase

from accounting.ac.data_models import TransactionData


class TestTransactionsView(TestCase):
    @patch(
        "accounting.ac.views.all_transactions",
        return_value=[
            TransactionData(
                id=1,
                order_id=1,
                sum=1000.0,
                date=datetime.datetime(2023, 5, 2),
            )
        ],
    )
    def test_all_orders_returns_200(self, all_transactions_mock):
        response = self.client.get("/accounting/transactions")
        all_transactions_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            [{"id": 1, "order_id": 1, "sum": 1000.0, "date": "02/05/2023, 00:00:00"}],
        )

    @patch("accounting.ac.views.create_transaction", return_value=1)
    def test_create_transaction_returns_200(self, create_product_mock):
        response = self.client.post(
            "/accounting/transactions",
            data={"order_id": 1, "order_sum": 10000.00},
            content_type="application/json",
        )
        create_product_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Transaction with id=1 created")


class TestTransactionDetailView(TestCase):
    @patch(
        "accounting.ac.views.get_transaction_by_id",
        return_value=TransactionData(
            id=1,
            order_id=1,
            sum=1000.0,
            date=datetime.datetime(2023, 5, 2),
        ),
    )
    def test_get_transaction_returns_200(self, get_transaction_mock):
        response = self.client.get("/accounting/transactions/1")
        get_transaction_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)

    @patch("accounting.ac.views.get_transaction_by_id", return_value=None)
    def test_get_transaction_returns_404(self, get_transaction_mock):
        response = self.client.get("/accounting/transactions/1")
        get_transaction_mock.assert_called_once()
        self.assertEqual(response.status_code, 404)

    @patch("accounting.ac.views.update_transaction")
    def test_update_transaction(self, update_transaction_mock):
        response = self.client.put(
            "/accounting/transactions/1", data=b'{"order_id": "327"}'
        )
        update_transaction_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Transaction 1 updated")

    @patch("accounting.ac.views.delete_transaction")
    def test_delete_transaction(self, delete_transaction_mock):
        response = self.client.delete("/accounting/transactions/2")
        delete_transaction_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Transaction 2 deleted")
