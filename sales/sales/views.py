from django.views import View
from django.http import JsonResponse
import requests


class SoldItemsView(View):
    wh_url = "http://wh-service:8082/items"

    def get(self, request):
        response = requests.get(self.wh_url)
        return JsonResponse(data=response.json())
