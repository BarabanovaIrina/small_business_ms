from typing import Any, List
from unittest.mock import patch

from django.test import TestCase

from warehouse.wh.data_models import ProductData
from warehouse.wh.models import Item, Price, Quantity
from warehouse.wh.services import (
    all_products,
    create_product,
    delete_product,
    get_product_by_id,
    get_product_by_name,
    update_product,
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

    def only(self):
        pass


class TestWarehouseServices(TestCase):
    @patch(
        "warehouse.wh.services.Item.objects.all",
        return_value=MockQuerySet(
            [Item(id=1, name="A", description="B", country_of_origin="C")]
        ),
    )
    @patch(
        "warehouse.wh.services.Price.objects.all",
        return_value=MockQuerySet([Price(item_id=1, price=1.0)]),
    )
    @patch(
        "warehouse.wh.services.Quantity.objects.all",
        return_value=MockQuerySet([Quantity(item_id=1, quantity=10000)]),
    )
    def test_all_products(self, q_mock, price_mock, item_mock):
        # when
        result = all_products()

        # then
        item_mock.assert_called_once()
        price_mock.assert_called_once()
        q_mock.assert_called_once()
        self.assertEqual(
            [
                ProductData(
                    id=1,
                    name="A",
                    description="B",
                    country_of_origin="C",
                    price=1.0,
                    quantity=10000,
                )
            ],
            result,
        )

    @patch(
        "warehouse.wh.services.get_object_by_id_safe",
        return_value=Item(id=1, name="name", description="desc", country_of_origin="c"),
    )
    @patch(
        "warehouse.wh.services.Price.objects.get",
        return_value=Price(item_id=1, price=1.0),
    )
    @patch(
        "warehouse.wh.services.Quantity.objects.get",
        return_value=Quantity(item_id=1, quantity=10000),
    )
    def test_get_product_by_id_ok(self, quantity_mock, price_mock, func_mock):
        # when
        result = get_product_by_id(1)
        # then
        func_mock.assert_called_once()
        price_mock.assert_called_once()
        quantity_mock.assert_called_once()
        self.assertEqual(
            ProductData(
                id=1,
                name="name",
                description="desc",
                country_of_origin="c",
                price=1.0,
                quantity=10000,
            ),
            result,
        )

    @patch("warehouse.wh.services.get_object_by_id_safe", return_value=None)
    def test_get_product_by_id_not_found(self, func_mock):
        # when
        result = get_product_by_id(1)
        # then
        func_mock.assert_called_once()
        self.assertEqual(None, result)

    @patch(
        "warehouse.wh.services.filter_objects",
        return_value=Item(
            id=1, name="name_1", description="desc", country_of_origin="c"
        ),
    )
    @patch(
        "warehouse.wh.services.Price.objects.get",
        return_value=Price(item_id=1, price=1.0),
    )
    @patch(
        "warehouse.wh.services.Quantity.objects.get",
        return_value=Quantity(item_id=1, quantity=10000),
    )
    def test_get_product_by_name_ok(self, quantity_mock, price_mock, func_mock):
        # when
        result = get_product_by_name("name_1")
        # then
        func_mock.assert_called_once()
        price_mock.assert_called_once()
        quantity_mock.assert_called_once()
        self.assertEqual(
            ProductData(
                id=1,
                name="name_1",
                description="desc",
                country_of_origin="c",
                price=1.0,
                quantity=10000,
            ),
            result,
        )

    @patch("warehouse.wh.services.filter_objects", return_value=None)
    def test_get_product_by_name_not_found(self, func_mock):
        # when
        result = get_product_by_name("name_1")
        # then
        func_mock.assert_called_once()
        self.assertEqual(None, result)

    @patch(
        "warehouse.wh.services.Item.objects.create",
        return_value=Item(
            id=1000, name="name", description="desc", country_of_origin="c"
        ),
    )
    @patch(
        "warehouse.wh.services.Price.objects.create",
        return_value=Price(id=1000, price=0.0),
    )
    @patch(
        "warehouse.wh.services.Quantity.objects.create",
        return_value=Quantity(id=1000, quantity=0),
    )
    def test_create_product(
        self, item_create_mock, price_create_mock, quantity_create_mock
    ):
        # when
        result = create_product(
            name="new_product",
            description="Description",
            country_of_origin="Country",
            quantity=0,
            price=0,
        )
        # then
        item_create_mock.assert_called_once()
        price_create_mock.assert_called_once()
        quantity_create_mock.assert_called_once()
        self.assertEqual(1000, result)

    @patch(
        "warehouse.wh.services.get_object_by_id_safe",
        return_value=Item(id=1, name="name", description="desc", country_of_origin="c"),
    )
    @patch("warehouse.wh.services.Item.save")
    def test_update_item_ok(self, item_save_mock, func_mock):
        # when
        update_product(
            pk=1,
            name="updated_name",
            description="updated_descr",
            country_of_origin="updated_country",
        )
        # then
        func_mock.assert_called_once()
        item_save_mock.assert_called_once()
        self.assertEqual(func_mock.return_value.name, "updated_name")
        self.assertEqual(func_mock.return_value.description, "updated_descr")
        self.assertEqual(func_mock.return_value.country_of_origin, "updated_country")

    @patch(
        "warehouse.wh.services.get_object_by_id_safe",
        return_value=Item(id=1, name="name", description="desc", country_of_origin="c"),
    )
    @patch("warehouse.wh.services.Item.save")
    @patch(
        "warehouse.wh.services.Quantity.objects.get",
        return_value=Quantity(item_id=1, quantity=10000),
    )
    @patch("warehouse.wh.services.Quantity.save")
    def test_update_product_quantity(
        self, quantity_save_mock, q_get_mock, item_save_mock, func_mock
    ):
        # when
        update_product(pk=1, quantity=2)
        # then
        func_mock.assert_called_once()
        item_save_mock.assert_called_once()
        q_get_mock.assert_called_once()
        quantity_save_mock.assert_called_once()
        self.assertEqual(q_get_mock.return_value.quantity, 2)

    @patch(
        "warehouse.wh.services.get_object_by_id_safe",
        return_value=Item(id=1, name="name", description="desc", country_of_origin="c"),
    )
    @patch("warehouse.wh.services.Item.save")
    @patch(
        "warehouse.wh.services.Price.objects.get",
        return_value=Price(item_id=1, price=10000),
    )
    @patch("warehouse.wh.services.Price.save")
    def test_update_product_price(
        self, price_save_mock, price_get_mock, item_save_mock, func_mock
    ):
        # when
        update_product(pk=2, price=2.0)
        # then
        func_mock.assert_called_once()
        item_save_mock.assert_called_once()
        price_get_mock.assert_called_once()
        price_save_mock.assert_called_once()
        self.assertEqual(price_get_mock.return_value.price, 2.0)

    @patch(
        "warehouse.wh.services.get_object_by_id_safe",
        return_value=Item(id=1, name="name", description="desc", country_of_origin="c"),
    )
    @patch("warehouse.wh.services.Item.delete")
    def test_delete_product(self, item_delete_mock, func_mock):
        # when
        delete_product(3)
        # then
        func_mock.assert_called_once()
        item_delete_mock.assert_called_once()
