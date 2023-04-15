from django.urls import path

from .views import OrderDetail, OrdersView, SoldItemsView

urlpatterns = [
    path("orders", OrdersView.as_view()),
    path("orders/<int:pk>", OrderDetail.as_view()),
    path("sold_items", SoldItemsView.as_view()),
]
