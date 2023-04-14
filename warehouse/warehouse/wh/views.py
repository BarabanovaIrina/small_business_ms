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
        return JsonResponse(products)

    @csrf_exempt
    def post(self, request):
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        create_product(product_name=name, quantity=quantity, price=price)
        return HttpResponse("Product created")


class ItemDetail(View):
    def get(self, request, pk: int):
        product = get_product_by_id(pk)
        if product is None:
            raise Http404("Opps, product not found")
        return JsonResponse(product)

    @csrf_exempt
    def post(self, request, pk: int):
        name = request.POST.get("product_name")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        update_product(pk=pk, product_name=name, quantity=quantity, price=price)
        return HttpResponse(f"Item {pk} updated")

    def delete(self, request, pk: int):
        delete_product(pk)
        return HttpResponse(f"Item {pk} deleted")
