from django.db.models import (
    CASCADE,
    CharField,
    DecimalField,
    ForeignKey,
    IntegerField,
    Model,
    TextField,
)

from ..common.managers import SafeGetManager


class Item(Model):
    class Meta:
        unique_together = (
            "name",
            "country_of_origin",
        )

    name = CharField(max_length=200)
    description = TextField()
    country_of_origin = CharField(max_length=60)
    objects = SafeGetManager()

    def __repr__(self):
        return f"{self.name}, {self.country_of_origin}"

    def __str__(self):
        return self.__repr__()


class Price(Model):
    item = ForeignKey(Item, on_delete=CASCADE)
    price = DecimalField(max_digits=8, decimal_places=2, default=0.0)
    objects = SafeGetManager()

    def __repr__(self):
        return f"{self.item}, {self.price}"

    def __str__(self):
        return self.__repr__()


class Quantity(Model):
    item = ForeignKey(Item, on_delete=CASCADE)
    quantity = IntegerField(default=0)
    objects = SafeGetManager()

    def __repr__(self):
        return f"{self.item}, {self.quantity}"

    def __str__(self):
        return self.__repr__()
