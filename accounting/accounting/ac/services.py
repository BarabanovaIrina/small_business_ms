from datetime import datetime
from typing import List, Optional

from ..common.services import all_objects, get_object_by_id_safe
from .data_models import TransactionData
from .models import Transaction, TransactionDetail


def all_transactions() -> List[TransactionData]:
    transactions = all_objects(TransactionDetail.objects)
    all_tr = []
    for trans in transactions:
        all_tr.append(
            TransactionData(
                id=trans.transaction.id,
                order_id=trans.transaction.order_id,
                sum=float(trans.sum),
                date=trans.date,
            )
        )
    return all_tr


def get_transaction_by_id(pk: int) -> Optional[TransactionData]:
    transaction = get_object_by_id_safe(
        objects=Transaction.objects, object_id=pk, model=Transaction
    )
    if transaction:
        detail = TransactionDetail.objects.get(transaction_id=pk)
        return TransactionData(
            id=transaction.id,
            order_id=transaction.order_id,
            sum=float(detail.sum),
            date=detail.date,
        )

    return None


def create_transaction(
    order_id: int,
    order_sum: float,
) -> int:
    t_created = Transaction.objects.create(order_id=order_id)
    TransactionDetail.objects.create(
        transaction=t_created, sum=order_sum, date=datetime.now()
    )

    return t_created.id


def update_transaction(
    pk: int,
    order_id: int,
):
    transaction = get_object_by_id_safe(
        objects=Transaction.objects, object_id=pk, model=Transaction
    )
    transaction.order_id = order_id
    transaction.save()


def delete_transaction(
    pk: int,
):
    transaction = get_object_by_id_safe(
        objects=Transaction.objects, object_id=pk, model=Transaction
    )
    transaction.delete()
