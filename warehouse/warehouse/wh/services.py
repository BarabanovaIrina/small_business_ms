from typing import List, Optional

from ..common.services import filter_objects, get_object_by_id_safe
from .data_models import ProductData
from .models import Item, Price, Quantity


def all_products() -> List[ProductData]:
    items = Item.objects.all()
    products = []
    if items.exists():
        # This ambiguous retrieving of all objects from Price
        # and Quantity is working under consideration that
        # all three tables are consistent.
        prices = Price.objects.all()
        quantities = Quantity.objects.all()
        for item, price, quantity in zip(items, prices, quantities):
            item_data = ProductData(
                id=item.id,
                name=item.name,
                description=item.description,
                country_of_origin=item.country_of_origin,
                price=float(price.price) if price else 0.0,
                quantity=quantity.quantity if quantity else 0,
            )
            products.append(item_data)
    return products


def get_product_by_id(pk: int) -> Optional[ProductData]:
    item = get_object_by_id_safe(objects=Item.objects, object_id=pk, model=Item)
    if item:
        price = Price.objects.get(item_id=pk)
        quantity = Quantity.objects.get(item_id=pk)
        return ProductData(
            id=item.id,
            name=item.name,
            description=item.description,
            country_of_origin=item.country_of_origin,
            price=float(price.price) if price else 0.0,
            quantity=quantity.quantity if quantity else 0,
        )

    return None


def get_product_by_name(name: str) -> Optional[ProductData]:
    item = filter_objects(Item.objects, {"name": name})
    if item:
        price = Price.objects.get(item.id)
        quantity = Quantity.objects.get(item.id)
        return ProductData(
            id=item.id,
            name=item.name,
            description=item.description,
            country_of_origin=item.country_of_origin,
            price=float(price.price) if price else 0.0,
            quantity=quantity.quantity if quantity else 0,
        )
    return None


def create_product(
    name: str,
    description: str = "",
    country_of_origin: str = "Not defined",
    quantity: int = 1,
    price: float = 0.00,
) -> int:
    item = Item.objects.create(
        name=name, description=description, country_of_origin=country_of_origin
    )
    Quantity.objects.create(item=item, quantity=quantity)
    Price.objects.create(item=item, price=price)

    return item.id


def update_product(
    pk: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    country_of_origin: Optional[str] = None,
    quantity: Optional[int] = None,
    price: Optional[float] = None,
) -> None:
    item = get_object_by_id_safe(objects=Item.objects, object_id=pk, model=Item)

    if not item:
        raise ValueError("Item not found")

    if name is not None:
        item.name = name

    if description is not None:
        item.description = description

    if country_of_origin is not None:
        item.country_of_origin = country_of_origin

    item.save()

    if quantity is not None:
        item_q = Quantity.objects.get(item_id=pk)
        item_q.quantity = quantity
        item_q.save()
    if price is not None:
        item_p = Price.objects.get(item_id=pk)
        item_p.price = price
        item_p.save()


def delete_product(
    pk: int,
):
    item = get_object_by_id_safe(objects=Item.objects, object_id=pk, model=Item)
    item.delete()
