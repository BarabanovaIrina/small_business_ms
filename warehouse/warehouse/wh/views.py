from django.http import JsonResponse
from django.views import View


class ItemsView(View):
    def get(self, request):
        my_items = {
            "item_1": "1",
            "item_2": "2",
            "item_3": "3",
            "item_4": "4",
        }
        return JsonResponse(my_items)
