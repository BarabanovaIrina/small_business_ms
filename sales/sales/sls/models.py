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


class Order(Model):
    customer_id = IntegerField()
    date = DateTimeField(default=now())
    objects = SafeGetManager()

    def __repr__(self):
        return f"{self.id}, {self.date}"

    def __str__(self):
        return self.__repr__()


class OrderDetail(Model):
    class Meta:
        unique_together = (
            "order_id",
            "item_id",
        )

    order = ForeignKey(Order, on_delete=CASCADE)
    item_id = IntegerField()
    unit_price = DecimalField(max_digits=8, decimal_places=2, default=0.0)
    quantity = IntegerField(default=0)
    objects = SafeGetManager()

    def __repr__(self):
        return f"{self.order_id}, {self.item_id}, {self.quantity}"

    def __str__(self):
        return self.__repr__()
