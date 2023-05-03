from typing import Any, List
from unittest.mock import patch

from django.test import TestCase

from accounting.ac.data_models import TransactionData
from accounting.ac.models import Transaction, TransactionDetail
from accounting.ac.services import (
    all_transactions,
    create_transaction,
    delete_transaction,
    get_transaction_by_id,
    update_transaction,
)


class MockQuerySet:
    objs: List[Any]

    def __init__(self, objs):
        self.objs = objs
        self.idx = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx < len(self.objs) - 1:
            self.idx += 1
            return self.objs[self.idx]
        else:
            raise StopIteration

    def exists(self):
        return True


class TestAccountingServices(TestCase):
    @patch(
        "accounting.ac.services.all_objects",
        return_value=MockQuerySet(
            [
                TransactionDetail(
                    transaction=Transaction(id=1, order_id=1),
                    sum=1000.0,
                    date="02/05/2023, 14:00:16",
                )
            ]
        ),
    )
    def test_get_all_transactions(self, func_mock):
        # when
        result = all_transactions()

        # then
        func_mock.assert_called_once()
        self.assertEqual(
            [
                TransactionData(
                    id=1,
                    order_id=1,
                    sum=1000.0,
                    date="02/05/2023, 14:00:16",
                )
            ],
            result,
        )

    @patch(
        "accounting.ac.services.get_object_by_id_safe",
        return_value=Transaction(id=1, order_id=1),
    )
    @patch(
        "accounting.ac.services.TransactionDetail.objects.get",
        return_value=TransactionDetail(
            transaction_id=1, sum=1000.0, date="02/05/2023, 14:00:16"
        ),
    )
    def test_get_transaction_by_id(self, tr_get_mock, func_mock):
        # when
        result = get_transaction_by_id(1)
        # then
        func_mock.assert_called_once()
        tr_get_mock.assert_called_once()
        self.assertEqual(
            TransactionData(
                id=1,
                order_id=1,
                sum=1000.0,
                date="02/05/2023, 14:00:16",
            ),
            result,
        )

    @patch(
        "accounting.ac.services.Transaction.objects.create",
        return_value=Transaction(id=10, order_id=1),
    )
    @patch(
        "accounting.ac.services.TransactionDetail.objects.create",
        return_value=TransactionDetail(
            transaction_id=10, sum=1000.0, date="02/05/2023, 14:00:16"
        ),
    )
    def test_create_transaction(self, tr_create_mock, tr_d_create_mock):
        # when
        result = create_transaction(order_id=1, order_sum=10000.00)
        # then
        tr_create_mock.assert_called_once()
        tr_d_create_mock.assert_called_once()
        self.assertEqual(10, result)

    @patch(
        "accounting.ac.services.get_object_by_id_safe",
        return_value=Transaction(id=10, order_id=1),
    )
    @patch("accounting.ac.services.Transaction.save")
    def test_update_transaction(self, save_mock, funck_mock):
        # when
        update_transaction(pk=1, order_id=10000)
        # then
        funck_mock.assert_called_once()
        save_mock.assert_called_once()
        self.assertEqual(10000, funck_mock.return_value.order_id)

    @patch(
        "accounting.ac.services.get_object_by_id_safe",
        return_value=Transaction(id=1, order_id=1),
    )
    @patch("accounting.ac.services.Transaction.delete")
    def test_delete_transaction(self, delete_mock, func_mock):
        # when
        delete_transaction(
            pk=1,
        )
        # then
        func_mock.assert_called_once()
        delete_mock.assert_called_once()
