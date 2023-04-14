import json
import os
from pathlib import Path
from typing import Dict

from django.test import TestCase

from accounting.ac.services import all_transactions, get_transaction


class TestAccountingServices(TestCase):
    def setUp(self) -> None:
        self.cur_dir = Path(__file__).resolve().parent
        test_data_path = Path(
            os.path.join(self.cur_dir, "data/transactions_test_data.json")
        )
        temp_data: Dict = json.loads(test_data_path.read_text())
        # because json.loads converts int to str
        self.all_transactions_data = {
            int(key): value for key, value in temp_data.items()
        }

    def test_all_products(self):
        # when
        result = all_transactions()

        # then
        self.assertEqual(
            self.all_transactions_data,
            result,
        )

    def test_get_order(self):
        # when
        result = get_transaction(1)
        # then
        self.assertEqual(
            {
                "user_id": "user_1",
                "transaction_id": 1,
                "timestamp": "2023-04-13 14:53:47.479374",
                "total": 10,
            },
            result,
        )
