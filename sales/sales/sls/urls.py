from django.urls import path

from .views import SoldItemsView

urlpatterns = [
    path("sold_items", SoldItemsView.as_view()),
]
