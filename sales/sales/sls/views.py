import requests
from django.http import JsonResponse
from django.views import View


class SoldItemsView(View):
    wh_url = "http://wh-service:5555/warehouse/items"

    def get(self, request):
        response = requests.get(self.wh_url)
        return JsonResponse(data=response.json())
