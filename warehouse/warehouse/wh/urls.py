from django.urls import path

from .views import ItemDelete, ItemDetail, ItemsList

urlpatterns = [
    path("items", ItemsList.as_view()),
    path("<str:pk>/", ItemDetail.as_view()),
    path("update/<str:pk>", ItemDetail.as_view()),
    path("delete/<str:pk>", ItemDelete.as_view()),
]
