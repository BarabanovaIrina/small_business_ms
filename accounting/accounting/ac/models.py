from django.db.models import (
    CASCADE,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    Model,
)
from django.utils.timezone import now

from ..common.managers import SafeGetManager


class Transaction(Model):
    # In sake of simplicity random integer
    # is used for order_id
    order_id = IntegerField()
    objects = SafeGetManager()

    def __repr__(self):
        return f"order_id={self.order_id}"

    def __str__(self):
        return self.__repr__()


class TransactionDetail(Model):
    transaction = ForeignKey(Transaction, on_delete=CASCADE)
    sum = DecimalField(max_digits=8, decimal_places=2, default=0.0)
    date = DateTimeField(default=now())
    objects = SafeGetManager()

    def __repr__(self):
        return f"{self.transaction}, {self.sum}"

    def __str__(self):
        return self.__repr__()
