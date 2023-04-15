from .models import TRANSACTIONS


def all_transactions():
    return TRANSACTIONS


def get_transaction(pk: int):
    return TRANSACTIONS.get(pk)
