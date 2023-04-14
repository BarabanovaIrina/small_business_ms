from typing import Dict, Optional

from .models import PRODUCTS


def all_products():
    return PRODUCTS


def get_product_by_id(pk: int) -> Optional[Dict]:
    return PRODUCTS.get(pk)


def get_product_by_name(name: str) -> Optional[Dict]:
    for product in PRODUCTS.values():
        if product["product_name"] == name:
            return product
    return None


def create_product(
    product_name: str,
    quantity: int = 1,
    price: float = 0.00,
):
    new_id = list(PRODUCTS.keys())[-1] + 1
    PRODUCTS[new_id] = {
        "product_name": product_name,
        "quantity": quantity,
        "price": price,
    }


def update_product(
    pk: int,
    product_name: Optional[str] = None,
    quantity: Optional[int] = None,
    price: Optional[float] = None,
):
    if product_name is not None:
        PRODUCTS[pk]["product_name"] = product_name
    if quantity is not None:
        PRODUCTS[pk]["quantity"] = quantity
    if price is not None:
        PRODUCTS[pk]["price"] = price


def delete_product(
    pk: int,
):
    del PRODUCTS[pk]
