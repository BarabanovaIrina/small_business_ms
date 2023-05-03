import json

from django.http import Http404, HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .services import (
    all_products,
    create_product,
    delete_product,
    get_product_by_id,
    update_product,
)


class ItemsList(View):
    def get(self, request):
        products = all_products()
        return HttpResponse(
            json.dumps([product.dict() for product in products]),
            content_type="application/json",
        )

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        name = data.get("name")
        description = data.get("description")
        country_of_origin = data.get("country_of_origin")
        quantity = data.get("quantity")
        price = data.get("price")
        product_id = create_product(
            name=name,
            description=description,
            country_of_origin=country_of_origin,
            quantity=quantity,
            price=price,
        )
        return HttpResponse(f"Product with id={product_id} created")


class ItemDetail(View):
    def get(self, request, pk: int):
        product = get_product_by_id(pk)
        if product is None:
            raise Http404("Opps, product not found")
        return JsonResponse(product.dict())

    @csrf_exempt
    def put(self, request, pk: int):
        data = json.loads(request.body)
        name = data.get("name")
        description = data.get("description")
        country_of_origin = data.get("country_of_origin")
        quantity = data.get("quantity")
        price = data.get("price")
        try:
            update_product(
                pk=pk,
                name=name,
                description=description,
                country_of_origin=country_of_origin,
                quantity=quantity,
                price=price,
            )
        except ValueError:
            raise Http404("Opps, product not found")
        return HttpResponse(f"Item {pk} updated")

    def delete(self, request, pk: int):
        delete_product(pk)
        return HttpResponse(f"Item {pk} deleted")
