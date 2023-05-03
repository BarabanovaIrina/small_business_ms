from datetime import datetime
from typing import Any, List
from unittest.mock import patch

from django.test import TestCase

from sales.sls.data_models import OrderData, OrderedItemData
from sales.sls.models import Order, OrderDetail
from sales.sls.services import (
    all_orders,
    create_order,
    delete_order,
    get_order_by_id,
    update_order,
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


class TestSalesServices(TestCase):
    @patch(
        "sales.sls.services.all_objects",
        return_value=MockQuerySet(
            [Order(id=1, customer_id=1, date=datetime(2023, 5, 2))]
        ),
    )
    @patch(
        "sales.sls.services.filter_objects",
        return_value=MockQuerySet(
            [
                OrderDetail(
                    order=Order(id=1, customer_id=1, date=datetime(2023, 5, 2)),
                    item_id=1,
                    unit_price=10.00,
                    quantity=5,
                )
            ]
        ),
    )
    def test_all_products(self, filter_objects_mock, all_objects_mock):
        # when
        result = all_orders()

        # then
        all_objects_mock.assert_called_once()
        filter_objects_mock.assert_called_once()
        self.assertEqual(
            [
                OrderData(
                    id=1,
                    customer_id=1,
                    date=datetime(2023, 5, 2),
                    items=[OrderedItemData(id=1, price=10.0, quantity=5)],
                )
            ],
            result,
        )

    @patch(
        "sales.sls.services.get_object_by_id_safe",
        return_value=Order(id=1, customer_id=1, date=datetime(2023, 5, 2)),
    )
    @patch(
        "sales.sls.services.filter_objects",
        return_value=MockQuerySet(
            [
                OrderDetail(
                    order=Order(id=1, customer_id=1, date=datetime(2023, 5, 2)),
                    item_id=1,
                    unit_price=10.00,
                    quantity=5,
                )
            ]
        ),
    )
    def test_get_order_by_id_ok(self, filter_objects_mock, all_objects_mock):
        # when
        result = get_order_by_id(1)
        # then
        all_objects_mock.assert_called_once()
        filter_objects_mock.assert_called_once()
        self.assertEqual(
            OrderData(
                id=1,
                customer_id=1,
                date=datetime(2023, 5, 2),
                items=[OrderedItemData(id=1, price=10.0, quantity=5)],
            ),
            result,
        )

    @patch("sales.sls.services.get_object_by_id_safe", return_value=None)
    def test_get_order_by_id_not_found(self, func_mock):
        # when
        result = get_order_by_id(1)
        # then
        func_mock.assert_called_once()
        self.assertEqual(result, None)

    @patch(
        "sales.sls.services.Order.objects.create",
        return_value=Order(id=327, customer_id=1, date=datetime(2023, 5, 2)),
    )
    @patch(
        "sales.sls.services.OrderDetail.objects.create",
        return_value=OrderDetail(order_id=1, item_id=1, unit_price=10.00, quantity=5),
    )
    def test_create_order(self, detail_create_mock, order_create_mock):
        # when
        result = create_order(
            customer_id=1,
            items=[
                {
                    "id": 1,
                    "price": 4000.0,
                    "quantity": 10,
                }
            ],
        )
        # then
        order_create_mock.assert_called_once()
        detail_create_mock.assert_called_once()
        self.assertEqual(327, result)

    @patch(
        "sales.sls.services.get_object_by_id_safe",
        return_value=Order(id=1, customer_id=1, date=datetime(2023, 5, 2)),
    )
    def test_update_order(self, func_mock):
        # when
        update_order(pk=1, customer_id=327)

        # then
        func_mock.assert_called_once()
        self.assertEqual(func_mock.return_value.customer_id, 327)

    @patch(
        "sales.sls.services.get_object_by_id_safe",
        return_value=Order(id=1, customer_id=1, date=datetime(2023, 5, 2)),
    )
    @patch("sales.sls.services.Order.delete")
    def test_delete_order(self, delete_mock, func_mock):
        # when
        delete_order(pk=1)
        # then
        func_mock.assert_called_once()
        delete_mock.assert_called_once()
