import json

from django.http import Http404, HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .services import (
    all_transactions,
    create_transaction,
    delete_transaction,
    get_transaction_by_id,
    update_transaction,
)


class TransactionsView(View):
    def get(self, request):
        transactions = all_transactions()
        return HttpResponse(
            json.dumps([transaction.dict() for transaction in transactions]),
            content_type="application/json",
        )

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        order_id = data.get("order_id")
        order_sum = data.get("order_sum")
        transaction_id = create_transaction(
            order_id=order_id,
            order_sum=order_sum,
        )
        return HttpResponse(f"Transaction with id={transaction_id} created")


class TransactionDetail(View):
    def get(self, request, pk: int):
        transaction = get_transaction_by_id(pk)
        if transaction is None:
            raise Http404("Opps, transaction not found")
        return JsonResponse(transaction.dict())

    @csrf_exempt
    def put(self, request, pk: int):
        data = json.loads(request.body)
        order_id = data.get("order_id")
        try:
            update_transaction(
                pk=pk,
                order_id=order_id,
            )
        except ValueError:
            raise Http404("Opps, transaction not found")
        return HttpResponse(f"Transaction {pk} updated")

    def delete(self, request, pk: int):
        delete_transaction(pk)
        return HttpResponse(f"Transaction {pk} deleted")
