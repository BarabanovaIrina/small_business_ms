from .models import ORDERS


def all_orders():
    return ORDERS


def get_order(pk: int):
    return ORDERS.get(pk)
