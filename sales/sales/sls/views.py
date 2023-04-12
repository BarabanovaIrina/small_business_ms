import requests
from django.http import JsonResponse
from django.views import View

from .services import all_orders, get_order


class OrdersView(View):
    def get(self, request):
        orders = all_orders()
        return JsonResponse(orders)


class OrderDetail(View):
    def get(self, request, pk: int):
        product = get_order(pk)
        return JsonResponse(product)


class SoldItemsView(View):
    wh_url = "http://wh-service:5555/warehouse/items"

    def get(self, request):
        response = requests.get(self.wh_url)
        return JsonResponse(data=response.json())
