from django.urls import path

from .views import ItemDelete, ItemDetail, ItemsList

urlpatterns = [
    path("items", ItemsList.as_view()),
    path("items/<int:pk>", ItemDetail.as_view()),
    path("delete/<int:pk>", ItemDelete.as_view()),
]
