import json

import requests
from django.http import Http404, HttpResponse, JsonResponse
from django.views import View

from .services import (
    all_orders,
    create_order,
    delete_order,
    get_order_by_id,
    update_order,
)


class OrdersView(View):
    def get(self, request):
        orders = all_orders()
        return HttpResponse(
            json.dumps([order.dict() for order in orders]),
            content_type="application/json",
        )

    def post(self, request):
        """
        Reqest Example:
        {
            "customer_id": 1,
            "items": [
                {
                    "id": 1,
                    "price": 10.0,
                    "quantity": 10
                }
            ]
        }
        """
        data = json.loads(request.body)
        customer_id = data.get("customer_id")
        # TODO add items data validation
        items = data.get("items")
        order_id = create_order(
            customer_id=customer_id,
            items=items,
        )
        return HttpResponse(f"Order with id={order_id} created")


class OrderDetail(View):
    def get(self, request, pk: int):
        product = get_order_by_id(pk)
        if product is None:
            raise Http404("Opps, order not found")
        return JsonResponse(product.dict())

    def put(self, request, pk: int):
        data = json.loads(request.body)
        customer_id = data.get("customer_id")
        try:
            update_order(
                pk=pk,
                customer_id=customer_id,
            )
        except ValueError:
            raise Http404("Opps, order not found")
        return HttpResponse(f"Order {pk} updated")

    def delete(self, request, pk: int):
        delete_order(pk)
        return HttpResponse(f"Order {pk} deleted")


class SoldItemsView(View):
    wh_url = "http://wh-service:5555/warehouse/items"

    def get(self, request):
        response = requests.get(self.wh_url)
        return JsonResponse(data=response.json())
