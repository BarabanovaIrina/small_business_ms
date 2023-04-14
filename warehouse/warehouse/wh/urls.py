from django.urls import path

from .views import ItemDetail, ItemsList

urlpatterns = [
    path("items", ItemsList.as_view()),
    path("items/<int:pk>", ItemDetail.as_view()),
]
