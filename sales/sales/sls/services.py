from typing import Dict, List, Optional

from ..common.services import all_objects, filter_objects, get_object_by_id_safe
from .data_models import OrderData, OrderedItemData
from .models import Order, OrderDetail


def all_orders() -> List[OrderData]:
    orders = all_objects(Order.objects)
    all_orders = []
    for order in orders:
        order_items = filter_objects(OrderDetail.objects, {"order_id": order.id})
        all_orders.append(
            OrderData(
                id=order.id,
                customer_id=order.customer_id,
                date=order.date,
                items=[
                    OrderedItemData(
                        id=item.item_id,
                        price=float(item.unit_price),
                        quantity=item.quantity,
                    )
                    for item in order_items
                ],
            )
        )
    return all_orders


def get_order_by_id(pk: int) -> Optional[OrderData]:
    order = get_object_by_id_safe(objects=Order.objects, object_id=pk, model=Order)
    if order:
        order_items = filter_objects(OrderDetail.objects, order_id=order.id)
        return OrderData(
            id=order.id,
            customer_id=order.customer_id,
            date=order.date,
            items=[
                OrderedItemData(
                    id=item.item_id,
                    price=float(item.unit_price),
                    quantity=item.quantity,
                )
                for item in order_items
            ],
        )
    return None


def create_order(
    customer_id: int,
    items: List[Dict],
) -> int:
    order_created = Order.objects.create(customer_id=customer_id)

    for item in items:
        OrderDetail.objects.create(
            order=order_created,
            item_id=item["id"],
            unit_price=item["price"],
            quantity=item["quantity"],
        )
    return order_created.id


def update_order(
    pk: int,
    customer_id: int,
):
    order = get_object_by_id_safe(objects=Order.objects, object_id=pk, model=Order)
    order.customer_id = customer_id
    order.save()


def delete_order(pk: int):
    order = get_object_by_id_safe(objects=Order.objects, object_id=pk, model=Order)
    order.delete()
