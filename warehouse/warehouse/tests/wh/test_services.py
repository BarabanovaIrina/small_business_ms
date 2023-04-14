from django.test import TestCase

from warehouse.wh.services import (
    all_products,
    create_product,
    delete_product,
    get_product_by_id,
    get_product_by_name,
    update_product,
)


class TestWarehouseServices(TestCase):
    def test_all_products(self):
        # when
        result = all_products()

        # then
        self.assertEqual(
            {
                1: {"product_name": "name_1", "quantity": 1, "price": 10},
                2: {"product_name": "name_2", "quantity": 2, "price": 20},
                3: {"product_name": "name_3", "quantity": 3, "price": 30},
                4: {"product_name": "name_4", "quantity": 4, "price": 40},
                5: {"product_name": "name_5", "quantity": 5, "price": 50},
                6: {"product_name": "name_6", "quantity": 6, "price": 60},
                7: {"product_name": "name_7", "quantity": 7, "price": 70},
                8: {"product_name": "name_8", "quantity": 8, "price": 80},
                9: {"product_name": "name_9", "quantity": 9, "price": 90},
                10: {"product_name": "name_10", "quantity": 10, "price": 100},
            },
            result,
        )

    def test_get_product(self):
        # when
        result = get_product_by_id(1)
        # then
        self.assertEqual({"product_name": "name_1", "quantity": 1, "price": 10}, result)

    def test_get_product_by_name(self):
        # when
        result = get_product_by_name("name_1")
        # then
        self.assertEqual({"product_name": "name_1", "quantity": 1, "price": 10}, result)

    def test_create_product(self):
        # when
        create_product(
            product_name="new_product",
            quantity=1,
            price=10.00,
        )
        result = get_product_by_name("new_product")
        # then
        self.assertEqual(
            {"product_name": "new_product", "quantity": 1, "price": 10.00}, result
        )

    def test_update_product_name(self):
        # when
        update_product(pk=1, product_name="updated_name")
        result = get_product_by_id(1)
        # then
        self.assertEqual(
            {"product_name": "updated_name", "quantity": 1, "price": 10}, result
        )

        # teardown
        update_product(pk=1, product_name="name_1")

    def test_update_product_quantity(self):
        # when
        update_product(pk=1, quantity=2)
        result = get_product_by_id(1)
        # then
        self.assertEqual({"product_name": "name_1", "quantity": 2, "price": 10}, result)
        # teardown
        update_product(pk=1, quantity="1")

    def test_update_product_price(self):
        # when
        update_product(pk=2, price=2.0)
        result = get_product_by_id(2)
        # then
        self.assertEqual(
            {"product_name": "name_2", "quantity": 2, "price": 2.0}, result
        )

    def test_delete_product(self):
        delete_product(3)
        result = get_product_by_id(3)
        self.assertEqual("Opps, product not found", result)
