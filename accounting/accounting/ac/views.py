from django.http import JsonResponse
from django.views import View

from .services import all_transactions, get_transaction


class TransactionsView(View):
    def get(self, request):
        transactions = all_transactions()
        return JsonResponse(transactions)


class TransactionDetail(View):
    def get(self, request, pk: int):
        transaction = get_transaction(pk)
        return JsonResponse(transaction)
