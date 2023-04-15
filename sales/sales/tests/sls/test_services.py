from django.test import TestCase

from sales.sls.services import all_orders, get_order


class TestSalesServices(TestCase):
    def test_all_products(self):
        # when
        result = all_orders()

        # then
        self.assertEqual(
            {
                1: {"transaction_id": "transaction_1", "user_id": "user_1"},
                2: {"transaction_id": "transaction_2", "user_id": "user_2"},
                3: {"transaction_id": "transaction_3", "user_id": "user_3"},
                4: {"transaction_id": "transaction_4", "user_id": "user_4"},
                5: {"transaction_id": "transaction_5", "user_id": "user_5"},
                6: {"transaction_id": "transaction_6", "user_id": "user_6"},
                7: {"transaction_id": "transaction_7", "user_id": "user_7"},
                8: {"transaction_id": "transaction_8", "user_id": "user_8"},
                9: {"transaction_id": "transaction_9", "user_id": "user_9"},
                10: {"transaction_id": "transaction_10", "user_id": "user_10"},
            },
            result,
        )

    def test_get_order(self):
        # when
        result = get_order(1)
        # then
        self.assertEqual(
            {"transaction_id": "transaction_1", "user_id": "user_1"}, result
        )
